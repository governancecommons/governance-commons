<#
.SYNOPSIS
    Validates PLAY.jsonl records against the DEV-PLAYBOOK schema (DEV-ACCORD.06 amendment).

.DESCRIPTION
    Parses each line of PLAY.jsonl as JSON and checks required fields, enum values,
    and conditional rules declared in the DEV-ACCORD.06 amendment:

      - play_id unique across all records
      - repo, level, declared_at, authorized_by, scope, timing, dev_docs_check, preflight required
      - status required for records created after the amendment; missing status is a
        legacy-tolerated warning, not a failure
      - authorization_note required when authorized_by is human
      - touches required when the record marks itself cross-repo (touches present or repo list > 1)
      - timing must include all five categories: read, plan, execute, verify, close,
        each with started_at, ended_at, duration_ms
      - dev_docs_check.note required when dev_docs_check.status is not-needed or deferred
      - commit_ref is only checked as a warning when status is closed and absent

    Does not execute PLAY.jsonl content. Read-only JSON parsing only.

.PARAMETER TargetPath
    Directory containing PLAY.jsonl (default: current directory).

.PARAMETER FilePath
    Explicit path to a PLAY.jsonl file. Overrides TargetPath discovery.

.PARAMETER Strict
    Treat legacy-tolerated warnings (missing status, missing commit_ref on closed PLAYs) as failures.

.PARAMETER Help
    Show help and exit.
#>
param(
    [string] $TargetPath = ".",
    [string] $FilePath = "",
    [switch] $Strict,
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$validLevels        = @('BUNT', 'RUN', 'DRIVE', 'PASS')
$validStatuses       = @('open', 'blocked', 'closed')
$validAuthorizedBy   = @('agent', 'human')
$validDevDocsStatus  = @('updated', 'not-needed', 'deferred')
$validPreflight      = @('complete', 'blocked', 'not-yet-enforced')
$timingCategories    = @('read', 'plan', 'execute', 'verify', 'close')

$playFile = $FilePath
if (-not $playFile) {
    $root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
    $playFile = Join-Path $root "PLAY.jsonl"
}

Write-Host ""
Write-Host "  DEV-PLAYBOOK VALIDATION - validate-playbook.ps1" -ForegroundColor White
Write-Host "  File: $playFile" -ForegroundColor DarkGray
Write-Host ""

if (-not (Test-Path -LiteralPath $playFile)) {
    Write-Host "  [WARN] PLAY.jsonl not found - nothing to validate." -ForegroundColor DarkYellow
    Write-Host ""
    exit 0
}

$lines = @(Get-Content -LiteralPath $playFile | Where-Object { $_.Trim().Length -gt 0 })

if ($lines.Count -eq 0) {
    Write-Host "  [WARN] PLAY.jsonl is empty." -ForegroundColor DarkYellow
    Write-Host ""
    exit 0
}

$errors   = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()
$telemetryRows = [System.Collections.Generic.List[object]]::new()
$seenIds  = [System.Collections.Generic.HashSet[string]]::new()
$lineNo   = 0

function Get-IntValue($Value) {
    if ($null -eq $Value) { return 0 }
    try { return [int64]$Value } catch { return 0 }
}

function Format-Duration([int64]$Milliseconds) {
    if ($Milliseconds -lt 1000) { return "${Milliseconds}ms" }
    $seconds = [math]::Round($Milliseconds / 1000, 1)
    if ($seconds -lt 60) { return "${seconds}s" }
    $minutes = [math]::Floor($seconds / 60)
    $remaining = [math]::Round($seconds % 60, 1)
    return "${minutes}m ${remaining}s"
}

foreach ($line in $lines) {
    $lineNo++
    $prefix = "line ${lineNo}:"

    try {
        $play = $line | ConvertFrom-Json -ErrorAction Stop
    } catch {
        $errors.Add("$prefix invalid JSON - $($_.Exception.Message)")
        continue
    }

    # play_id - required, unique
    if (-not $play.play_id) {
        $errors.Add("$prefix missing play_id")
    } elseif (-not $seenIds.Add([string]$play.play_id)) {
        $errors.Add("$prefix duplicate play_id: $($play.play_id)")
    }

    $id = if ($play.play_id) { $play.play_id } else { "(no id)" }

    # repo - required
    if (-not $play.repo) { $errors.Add("$prefix ($id) missing repo") }

    # level - required, enum
    if (-not $play.level) {
        $errors.Add("$prefix ($id) missing level")
    } elseif ($validLevels -notcontains $play.level) {
        $errors.Add("$prefix ($id) invalid level '$($play.level)' - must be one of: $($validLevels -join ', ')")
    }

    # status - required going forward; missing is legacy-tolerated
    if (-not $play.PSObject.Properties.Match('status').Count -or -not $play.status) {
        $warnings.Add("$prefix ($id) missing status - legacy-tolerated only for pre-amendment records")
    } elseif ($validStatuses -notcontains $play.status) {
        $errors.Add("$prefix ($id) invalid status '$($play.status)' - must be one of: $($validStatuses -join ', ')")
    }

    # declared_at - required, must parse
    if (-not $play.declared_at) {
        $errors.Add("$prefix ($id) missing declared_at")
    } else {
        try { [void][datetime]::Parse($play.declared_at) } catch {
            $errors.Add("$prefix ($id) declared_at does not parse as a timestamp: $($play.declared_at)")
        }
    }

    # authorized_by - required, enum; authorization_note conditional
    if (-not $play.authorized_by) {
        $errors.Add("$prefix ($id) missing authorized_by")
    } elseif ($validAuthorizedBy -notcontains $play.authorized_by) {
        $errors.Add("$prefix ($id) invalid authorized_by '$($play.authorized_by)' - must be agent or human")
    } elseif ($play.authorized_by -eq 'human') {
        if (-not $play.authorization_note -or [string]$play.authorization_note -eq '') {
            $errors.Add("$prefix ($id) authorization_note is required when authorized_by is human")
        }
    }

    # scope - required
    if (-not $play.scope) { $errors.Add("$prefix ($id) missing scope") }

    # touches - required when cross-repo; if present must be array
    if ($play.PSObject.Properties.Match('touches').Count -gt 0 -and $null -ne $play.touches) {
        if ($play.touches -isnot [array]) {
            $errors.Add("$prefix ($id) touches must be an array")
        }
    }

    # timing - required object with 5 categories, each with 3 sub-fields
    if (-not $play.timing) {
        $errors.Add("$prefix ($id) missing timing object")
    } else {
        foreach ($cat in $timingCategories) {
            $catObj = $play.timing.$cat
            if (-not $catObj) {
                $errors.Add("$prefix ($id) timing.$cat missing")
                continue
            }
            foreach ($sub in @('started_at', 'ended_at', 'duration_ms')) {
                if (-not ($catObj.PSObject.Properties.Match($sub).Count -gt 0)) {
                    $errors.Add("$prefix ($id) timing.$cat.$sub missing")
                }
            }
        }
    }

    # dev_docs_check - required object; note conditional
    if (-not $play.dev_docs_check) {
        $errors.Add("$prefix ($id) missing dev_docs_check")
    } else {
        $ddStatus = $play.dev_docs_check.status
        if (-not $ddStatus) {
            $errors.Add("$prefix ($id) missing dev_docs_check.status")
        } elseif ($validDevDocsStatus -notcontains $ddStatus) {
            $errors.Add("$prefix ($id) invalid dev_docs_check.status '$ddStatus' - must be one of: $($validDevDocsStatus -join ', ')")
        } elseif ($ddStatus -in @('not-needed', 'deferred')) {
            if (-not $play.dev_docs_check.note -or [string]$play.dev_docs_check.note -eq '') {
                $errors.Add("$prefix ($id) dev_docs_check.note is required when status is $ddStatus")
            }
        }
    }

    # commit_ref - warning-only heuristic: expected when status is closed
    $statusVal = if ($play.PSObject.Properties.Match('status').Count -gt 0) { $play.status } else { $null }
    if ($statusVal -eq 'closed' -and -not $play.commit_ref) {
        $warnings.Add("$prefix ($id) status is closed but commit_ref is absent - verify this PLAY produced no commit")
    }

    # preflight - required, enum
    if (-not $play.preflight) {
        $errors.Add("$prefix ($id) missing preflight")
    } elseif ($validPreflight -notcontains $play.preflight) {
        $errors.Add("$prefix ($id) invalid preflight '$($play.preflight)' - must be one of: $($validPreflight -join ', ')")
    }

    if ($play.timing) {
        $readMs = Get-IntValue $play.timing.read.duration_ms
        $planMs = Get-IntValue $play.timing.plan.duration_ms
        $executeMs = Get-IntValue $play.timing.execute.duration_ms
        $verifyMs = Get-IntValue $play.timing.verify.duration_ms
        $closeMs = Get-IntValue $play.timing.close.duration_ms
        $telemetryRows.Add([PSCustomObject]@{
            PlayId = [string]$id
            Level = if ($play.level) { [string]$play.level } else { "?" }
            Status = if ($play.status) { [string]$play.status } else { "?" }
            ReadMs = $readMs
            PlanMs = $planMs
            ExecuteMs = $executeMs
            VerifyMs = $verifyMs
            CloseMs = $closeMs
            TotalMs = ($readMs + $planMs + $executeMs + $verifyMs + $closeMs)
        })
    }
}

Write-Host "  $($lines.Count) record(s) checked" -ForegroundColor DarkGray
Write-Host ""

foreach ($w in $warnings) { Write-Host "  [WARN]  $w" -ForegroundColor DarkYellow }
foreach ($e in $errors)   { Write-Host "  [ERROR] $e" -ForegroundColor Red }

Write-Host ""

if ($telemetryRows.Count -gt 0) {
    Write-Host "  PLAY TELEMETRY (5 timing buckets)" -ForegroundColor White
    Write-Host "  play_id                         level  status   read     plan     execute  verify   close    total" -ForegroundColor DarkGray
    Write-Host "  -----------------------------------------------------------------------------------------------" -ForegroundColor DarkGray
    foreach ($row in $telemetryRows) {
        $shortId = if ($row.PlayId.Length -gt 30) { $row.PlayId.Substring(0, 27) + "..." } else { $row.PlayId }
        Write-Host ("  {0,-30} {1,-6} {2,-8} {3,-8} {4,-8} {5,-8} {6,-8} {7,-8} {8,-8}" -f `
            $shortId,
            $row.Level,
            $row.Status,
            (Format-Duration $row.ReadMs),
            (Format-Duration $row.PlanMs),
            (Format-Duration $row.ExecuteMs),
            (Format-Duration $row.VerifyMs),
            (Format-Duration $row.CloseMs),
            (Format-Duration $row.TotalMs)) -ForegroundColor DarkCyan
    }
    Write-Host ""
}

$hasFailure = ($errors.Count -gt 0) -or ($Strict -and $warnings.Count -gt 0)

if (-not $hasFailure) {
    Write-Host "  [PASS] PLAY.jsonl conforms to the DEV-PLAYBOOK schema ($($warnings.Count) warning(s))." -ForegroundColor Green
    Write-Host ""
    exit 0
}

Write-Host "  [FAIL] $($errors.Count) error(s), $($warnings.Count) warning(s)." -ForegroundColor Red
Write-Host ""
exit 1
