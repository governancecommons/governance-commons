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
      - validation_profile required for records created after the validation_profile
        amendment; missing validation_profile is a legacy-tolerated warning, not a
        failure - when present, its shape and per-level minimum checks are still
        enforced as hard errors

    Does not execute PLAY.jsonl content. Read-only JSON parsing only.

.PARAMETER TargetPath
    Directory containing PLAY.jsonl (default: current directory).

.PARAMETER FilePath
    Explicit path to a PLAY.jsonl file. Overrides TargetPath discovery.

.PARAMETER Strict
    Treat legacy-tolerated warnings (missing status, missing commit_ref on closed PLAYs,
    missing validation_profile) as failures.

.PARAMETER Json
    Emit a machine-readable gc-audit.result.v1 JSON object.

.PARAMETER Help
    Show help and exit.
#>
param(
    [string] $TargetPath = ".",
    [string] $FilePath = "",
    [switch] $Strict,
    [switch] $Json,
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
$requiredProfileChecks = @{
    BUNT  = @('dev-docs-check')
    RUN   = @('dev-docs-check', 'gc-audit.playbook')
    DRIVE = @('dev-docs-update', 'gc-audit.validate', 'gc-audit.zerotrust')
    PASS  = @('dev-docs-update', 'gc-audit.validate', 'gc-audit.release', 'evidence-bundle')
}

$playFile = $FilePath
if (-not $playFile) {
    $root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
    $playFile = Join-Path $root "PLAY.jsonl"
}

function Write-Human([string]$Text = "", [string]$Color = "") {
    if ($Json) { return }
    if ($Color) {
        Write-Host $Text -ForegroundColor $Color
    } else {
        Write-Host $Text
    }
}

function Write-JsonResult([string]$Status, [string[]]$Errors, [string[]]$Warnings, [object[]]$Telemetry, [object]$Summary) {
    if (-not $Json) { return }
    [PSCustomObject]@{
        schema = "gc-audit.result.v1"
        tool = "validate-playbook.ps1"
        status = $Status
        target = $playFile
        errors = @($Errors)
        warnings = @($Warnings)
        summary = $Summary
        telemetry = @($Telemetry)
    } | ConvertTo-Json -Depth 8
}

Write-Human ""
Write-Human "  DEV-PLAYBOOK VALIDATION - validate-playbook.ps1" "White"
Write-Human "  File: $playFile" "DarkGray"
Write-Human ""

if (-not (Test-Path -LiteralPath $playFile)) {
    Write-Human "  [WARN] PLAY.jsonl not found - nothing to validate." "DarkYellow"
    Write-Human ""
    Write-JsonResult "skipped" @() @("PLAY.jsonl not found - nothing to validate.") @() ([PSCustomObject]@{ records_checked = 0 })
    exit 0
}

$lines = @(Get-Content -LiteralPath $playFile | Where-Object { $_.Trim().Length -gt 0 })

if ($lines.Count -eq 0) {
    Write-Human "  [WARN] PLAY.jsonl is empty." "DarkYellow"
    Write-Human ""
    Write-JsonResult "skipped" @() @("PLAY.jsonl is empty.") @() ([PSCustomObject]@{ records_checked = 0 })
    exit 0
}

$errors   = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()
$telemetryRows = [System.Collections.Generic.List[object]]::new()
$profileRows = [System.Collections.Generic.List[object]]::new()
$playSummaries = [System.Collections.Generic.List[object]]::new()
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

function Get-StringOrDefault($Value, [string]$Default = "") {
    if ($null -eq $Value) { return $Default }
    $text = [string]$Value
    if ($text.Trim().Length -eq 0) { return $Default }
    return $text
}

function Get-LatestPlaySummary([object[]]$Summaries) {
    if (-not $Summaries -or $Summaries.Count -eq 0) { return $null }
    return $Summaries |
        Sort-Object @{
            Expression = {
                try { [datetime]::Parse($_.declared_at) } catch { [datetime]::MinValue }
            }
        } |
        Select-Object -Last 1
}

function Get-NextRecommendedStep([bool]$HasFailure, [int]$WarningCount, [object]$LatestPlay) {
    if ($HasFailure) {
        return "Fix DEV-PLAYBOOK validation errors before starting another PLAY."
    }
    if ($WarningCount -gt 0) {
        return "Resolve DEV-PLAYBOOK warnings or explicitly document why they are acceptable before the next PLAY."
    }
    if (-not $LatestPlay) {
        return "Declare the next PLAY before starting new work."
    }
    if ($LatestPlay.status -eq "blocked") {
        return "Clear the blocker or get human authorization for the next move before continuing."
    }
    if ($LatestPlay.status -ne "closed") {
        return "Close the active PLAY with DEV-DOCS, validation, commit, and push before starting another PLAY."
    }
    if ($LatestPlay.dev_docs_status -ne "updated") {
        return "Update DEV-DOCS or record an explicit exemption before starting another PLAY."
    }
    if ($LatestPlay.level -eq "PASS") {
        return "Run release/evidence review, then proceed only with the next authorized PASS or app-development PLAY."
    }
    return "Proceed to the next user-authorized development PLAY; use the latest DEV-DOCS and GC-AUDIT contracts as the starting context."
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

    # validation_profile - required going forward; missing is legacy-tolerated (same
    # treatment as status, per the DEV-ACCORD.06 amendment that formally declared this
    # field). When present, its internal shape and per-level minimum checks are still
    # enforced as hard errors.
    if (-not $play.validation_profile) {
        $warnings.Add("$prefix ($id) missing validation_profile - legacy-tolerated only for records predating the validation_profile amendment")
    } else {
        $profile = $play.validation_profile.profile
        if (-not $profile) {
            $errors.Add("$prefix ($id) missing validation_profile.profile")
        } elseif ($validLevels -notcontains $profile) {
            $errors.Add("$prefix ($id) invalid validation_profile.profile '$profile' - must be one of: $($validLevels -join ', ')")
        } elseif ($play.level -and $profile -ne $play.level) {
            $errors.Add("$prefix ($id) validation_profile.profile '$profile' does not match level '$($play.level)'")
        }

        if (-not $play.validation_profile.checks) {
            $errors.Add("$prefix ($id) missing validation_profile.checks")
        } else {
            $checks = @($play.validation_profile.checks | ForEach-Object { [string]$_ })
            if ($checks.Count -eq 0) {
                $errors.Add("$prefix ($id) validation_profile.checks is empty")
            }
            if ($play.level -and $requiredProfileChecks.ContainsKey($play.level)) {
                foreach ($requiredCheck in $requiredProfileChecks[$play.level]) {
                    if ($checks -notcontains $requiredCheck) {
                        $errors.Add("$prefix ($id) validation_profile missing required check for $($play.level): $requiredCheck")
                    }
                }
            }
            if (($checks -contains 'dev-docs-update') -and $play.dev_docs_check -and $play.dev_docs_check.status -ne 'updated') {
                $errors.Add("$prefix ($id) validation_profile requires dev-docs-update but dev_docs_check.status is '$($play.dev_docs_check.status)'")
            }
            $profileRows.Add([PSCustomObject]@{
                play_id = [string]$id
                profile = if ($profile) { [string]$profile } else { "?" }
                checks = @($checks)
            })
        }
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

    $validationChecks = @()
    if ($play.validation_profile -and $play.validation_profile.checks) {
        $validationChecks = @($play.validation_profile.checks | ForEach-Object { [string]$_ })
    }
    $playSummaries.Add([PSCustomObject]@{
        play_id = [string]$id
        repo = Get-StringOrDefault $play.repo "?"
        level = Get-StringOrDefault $play.level "?"
        status = Get-StringOrDefault $play.status "?"
        declared_at = Get-StringOrDefault $play.declared_at ""
        scope = Get-StringOrDefault $play.scope ""
        dev_docs_status = if ($play.dev_docs_check) { Get-StringOrDefault $play.dev_docs_check.status "?" } else { "?" }
        commit_ref = Get-StringOrDefault $play.commit_ref ""
        validation_checks = @($validationChecks)
    })
}

Write-Human "  $($lines.Count) record(s) checked" "DarkGray"
Write-Human ""

foreach ($w in $warnings) { Write-Human "  [WARN]  $w" "DarkYellow" }
foreach ($e in $errors)   { Write-Human "  [ERROR] $e" "Red" }

Write-Human ""

if ($telemetryRows.Count -gt 0) {
    Write-Human "  PLAY TELEMETRY (5 timing buckets)" "White"
    Write-Human "  play_id                         level  status   read     plan     execute  verify   close    total" "DarkGray"
    Write-Human "  -----------------------------------------------------------------------------------------------" "DarkGray"
    foreach ($row in $telemetryRows) {
        $shortId = if ($row.PlayId.Length -gt 30) { $row.PlayId.Substring(0, 27) + "..." } else { $row.PlayId }
        Write-Human ("  {0,-30} {1,-6} {2,-8} {3,-8} {4,-8} {5,-8} {6,-8} {7,-8} {8,-8}" -f `
            $shortId,
            $row.Level,
            $row.Status,
            (Format-Duration $row.ReadMs),
            (Format-Duration $row.PlanMs),
            (Format-Duration $row.ExecuteMs),
            (Format-Duration $row.VerifyMs),
            (Format-Duration $row.CloseMs),
            (Format-Duration $row.TotalMs)) "DarkCyan"
    }
    Write-Human ""
}

$hasFailure = ($errors.Count -gt 0) -or ($Strict -and $warnings.Count -gt 0)
$latestPlay = Get-LatestPlaySummary @($playSummaries)
$nextRecommendedStep = Get-NextRecommendedStep $hasFailure $warnings.Count $latestPlay

if ($latestPlay) {
    Write-Human "  LATEST PLAY SUMMARY" "White"
    Write-Human ("  id:        {0}" -f $latestPlay.play_id) "DarkCyan"
    Write-Human ("  repo:      {0}" -f $latestPlay.repo) "DarkCyan"
    Write-Human ("  level:     {0}  status: {1}" -f $latestPlay.level, $latestPlay.status) "DarkCyan"
    Write-Human ("  scope:     {0}" -f $latestPlay.scope) "DarkCyan"
    Write-Human ("  dev-docs:  {0}  commit: {1}" -f $latestPlay.dev_docs_status, $latestPlay.commit_ref) "DarkCyan"
    Write-Human ("  checks:    {0}" -f (($latestPlay.validation_checks) -join ", ")) "DarkCyan"
    Write-Human ""
}

Write-Human "  NEXT RECOMMENDED STEP" "White"
Write-Human ("  {0}" -f $nextRecommendedStep) "DarkCyan"
Write-Human ""

$summary = [PSCustomObject]@{
    records_checked = $lines.Count
    warnings = $warnings.Count
    errors = $errors.Count
    strict = [bool]$Strict
    schema = "schemas/gc-play-record.schema.json"
    validation_profiles = @($profileRows)
    latest_play = $latestPlay
    next_recommended_step = $nextRecommendedStep
}

if (-not $hasFailure) {
    Write-Human "  [PASS] PLAY.jsonl conforms to the DEV-PLAYBOOK schema ($($warnings.Count) warning(s))." "Green"
    Write-Human ""
    $status = if ($warnings.Count -gt 0) { "warn" } else { "pass" }
    Write-JsonResult $status @($errors) @($warnings) @($telemetryRows) $summary
    exit 0
}

Write-Human "  [FAIL] $($errors.Count) error(s), $($warnings.Count) warning(s)." "Red"
Write-Human ""
Write-JsonResult "fail" @($errors) @($warnings) @($telemetryRows) $summary
exit 1
