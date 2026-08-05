<#
.SYNOPSIS
    Portfolio diagnostic check for recent work across a target root.

.DESCRIPTION
    Runs health checks and commit analysis at increasing depth.

    Level 1 - Quick health: run all validators, report pass/fail.
    Level 2 - Recent-work review: adds dirty repos, commit log, changed files.
    Level 3 - Adversarial audit: adds TODO/TBD scan, planning doc staleness.
    Level 4 - Release readiness: adds PASS gate and DEV-RELEASE pending checks.

.PARAMETER Hours
    How far back to look for recent work (default 24).

.PARAMETER Level
    Diagnostic depth 1-4 (default 1).

.PARAMETER TargetPath
    Portfolio root (default current directory).

.PARAMETER Summary
    Print compact summary only; suppress per-item detail.
#>
param(
    [int]    $Hours      = 24,
    [ValidateRange(1,4)]
    [int]    $Level      = 1,
    [string] $TargetPath = ".",
    [switch] $Summary
)

$root     = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$toolRoot = $PSScriptRoot
$since    = (Get-Date).AddHours(-$Hours)
$sinceStr = $since.ToString("yyyy-MM-dd HH:mm:ss")
$sinceUtc = $since.ToUniversalTime()
$exitFail = $false
$powerShellHost = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$isWindowsHost = ($env:OS -eq "Windows_NT")

# Same exclusion convention already standard across this tool family
# (validate-format.ps1, validate-bootstrap.ps1, validate-ci-invariants.ps1,
# etc.) - this script was the one exception, scanning node_modules/.venv/
# dist/build scratch trees that every sibling script already skips.
#
# The last alternative additionally matches a whole segment ending in
# "_archive"/"-archive" (lasso_archive, lasso-mvp_archive, ...), whether it
# is a bare directory name with no trailing separator (Get-GitRoots'
# top-level scan) or a segment nested inside a longer path
# (...\lasso_archive\DEV-PLAN.md) - checked via a following separator or
# end-of-string, so a file merely containing "-archive" mid-name (e.g.
# "archive-notes.md") is not falsely excluded.
$excludeRegex = '(?i)[\\/](\.git|node_modules|_tmp|dist|build|out|coverage|\.venv|\.pytest_cache|[^\\/]*[_-]archive)(?:[\\/]|$)'

$levelNames = @{ 1="Quick Health"; 2="Recent-Work Review"; 3="Adversarial Audit"; 4="Release Readiness" }

function Write-Header([string]$text) {
    Write-Host ""
    Write-Host "-- $text" -ForegroundColor Cyan
}
function Write-Pass([string]$msg)  { Write-Host "  PASS  $msg" -ForegroundColor Green }
function Write-Fail([string]$msg)  { Write-Host "  FAIL  $msg" -ForegroundColor Red; $script:exitFail = $true }
function Write-Warn([string]$msg)  { Write-Host "  WARN  $msg" -ForegroundColor Yellow }
function Write-Info([string]$msg)  { Write-Host "  INFO  $msg" -ForegroundColor DarkGray }
function Write-Find([string]$msg)  { Write-Host "  FIND  $msg" -ForegroundColor Magenta }

function Invoke-ReadOnlyValidator([string]$ScriptPath, [string]$TargetRoot) {
    $args = @("-NoProfile")
    if ($isWindowsHost) {
        $args += @("-ExecutionPolicy", "Bypass")
    }
    $args += @("-File", $ScriptPath, "-TargetPath", $TargetRoot)
    return & $powerShellHost @args 2>&1
}

function Get-GitRoots {
    $roots = @()
    if ((Test-Path (Join-Path $root ".git")) -and $root -notmatch $excludeRegex) { $roots += $root }
    Get-ChildItem $root -Directory -Depth 2 -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.FullName -match $excludeRegex) { return }
        if (Test-Path (Join-Path $_.FullName ".git")) { $roots += $_.FullName }
    }
    return @($roots | Select-Object -Unique)
}

function Get-PassStatus([string]$FilePath) {
    # Reads only the authoritative PASS metadata field - a line-anchored
    # **Status:** (DEV-ACCORD style) or NP-METADATA "- Status:" (CANON
    # style) declaration - never prose that merely contains the word
    # "status" elsewhere in the body. Real example: CANON.02.md's own
    # header says "Status: ACCEPTED", but its body also discusses registry
    # *entry* statuses in passing ("a binding entry (status: draft,
    # accepted, sealed, or reserved)") - a whole-file substring match
    # cannot tell those apart; a line-anchored field read can.
    $lines = Get-Content -LiteralPath $FilePath -ErrorAction SilentlyContinue
    foreach ($line in $lines) {
        if ($line -match '^\*\*Status:\*\*\s*(.+?)\s*$') { return $Matches[1].Trim() }
        if ($line -match '^-\s*Status:\s*(.+?)\s*$') { return $Matches[1].Trim() }
    }
    return $null
}

function Get-ActiveReleaseVersion([string[]]$Lines) {
    # The active release candidate is the Release Table row whose status
    # cell contains "in progress" - the convention already in real use
    # across this portfolio's DEV-RELEASE.md files (cockpit, marlin). Rows
    # marked Done, planned, open, or bare unchecked are historical or
    # future work, not this repo's current gate.
    foreach ($line in $Lines) {
        if ($line -notmatch '^\s*\|') { continue }
        $cells = $line.Trim().Trim('|') -split '\|' | ForEach-Object { $_.Trim() }
        if ($cells.Count -lt 2) { continue }
        $versionCell = $cells[0]
        $statusCell  = $cells[-1]
        if ($versionCell -notmatch '^v?\d+(\.\d+)+') { continue }
        if ($statusCell -match '(?i)in.?progress') { return $versionCell }
    }
    return $null
}

function Get-ActiveReleaseGaps([string]$FilePath) {
    # Counts real unchecked "- [ ]" items, scoped to the active release
    # candidate's own section only (a heading naming that version). A
    # future or historical release's unchecked entry conditions are not
    # this version's gate and must not be reported as one.
    $lines = Get-Content -LiteralPath $FilePath -ErrorAction SilentlyContinue
    if (-not $lines) { return @() }

    $activeVersion = Get-ActiveReleaseVersion $lines
    if (-not $activeVersion) { return @() }

    $escaped   = [regex]::Escape($activeVersion)
    $gaps      = @()
    $inSection = $false
    foreach ($line in $lines) {
        if ($line -match ('^#{1,4}\s.*' + $escaped + '\b')) {
            $inSection = $true
            continue
        }
        if ($inSection -and $line -match '^#{1,4}\s') {
            $inSection = $false
        }
        if ($inSection -and $line -match '^\s*-\s*\[\s\]\s*(.+?)\s*$') {
            $gaps += $Matches[1]
        }
    }
    return @($gaps)
}

# header

Write-Host ""
Write-Host ("validate-recent-work  |  Level {0} - {1}  |  window: last {2} h  |  since: {3}" -f `
    $Level, $levelNames[$Level], $Hours, $sinceStr) -ForegroundColor White
Write-Host "portfolio root: $root" -ForegroundColor DarkGray
Write-Host "-------------------------------------------------------------" -ForegroundColor DarkGray

# LEVEL 1 - VALIDATOR HEALTH

Write-Header "Level 1 - Validator Health"

$validators = @(
    [PSCustomObject]@{ Name="bootstrap (DEV-ACCORD.04)";      Script="validate-bootstrap.ps1";      PortfolioOnly=$false }
    [PSCustomObject]@{ Name="planning docs (DEV-ACCORD.00)";  Script="validate-planning.ps1";       PortfolioOnly=$false }
    [PSCustomObject]@{ Name="pointers (projects.yaml)";       Script="validate-pointers.ps1";       PortfolioOnly=$true  }
    [PSCustomObject]@{ Name="review grammar";                 Script="validate-review-grammar.ps1"; PortfolioOnly=$false }
    [PSCustomObject]@{ Name="debt registry";                  Script="validate-debt.ps1";           PortfolioOnly=$false }
    [PSCustomObject]@{ Name="git split authorization";         Script="validate-git-split.ps1";      PortfolioOnly=$false }
    [PSCustomObject]@{ Name="CI invariant uniqueness";         Script="validate-ci-invariants.ps1";  PortfolioOnly=$false }
    [PSCustomObject]@{ Name="script format providers";          Script="validate-format.ps1";         PortfolioOnly=$false }
    [PSCustomObject]@{ Name="DEV-PLAYBOOK records";             Script="validate-playbook.ps1";       PortfolioOnly=$false; RequiresFile="PLAY.jsonl"; ShowOutputOnPass=$true }
)

foreach ($v in $validators) {
    if ($v.PortfolioOnly -and -not (Test-Path (Join-Path $root "projects.yaml"))) {
        Write-Info "$($v.Name) - portfolio-only, skipped for project target"
        continue
    }
    if ($v.PSObject.Properties.Match("RequiresFile").Count -gt 0 -and $v.RequiresFile) {
        $requiredPath = Join-Path $root $v.RequiresFile
        if (-not (Test-Path -LiteralPath $requiredPath)) {
            Write-Info "$($v.Name) - $($v.RequiresFile) not found, skipped"
            continue
        }
    }
    if (-not (Test-Path -LiteralPath $root)) {
        Write-Fail "target path not found: $root"
        continue
    }
    $scriptPath = Join-Path $toolRoot $v.Script
    if (-not (Test-Path $scriptPath)) {
        Write-Info "$($v.Name) - script not found, skipped"
        continue
    }
    $out = Invoke-ReadOnlyValidator -ScriptPath $scriptPath -TargetRoot $root
    if ($LASTEXITCODE -eq 0) {
        Write-Pass $v.Name
        if (-not $Summary -and $v.PSObject.Properties.Match("ShowOutputOnPass").Count -gt 0 -and $v.ShowOutputOnPass) {
            $out | ForEach-Object { Write-Host "        $_" -ForegroundColor DarkGray }
        }
    } else {
        Write-Fail $v.Name
        if (-not $Summary) {
            $out | ForEach-Object { Write-Host "        $_" -ForegroundColor Yellow }
        }
    }
}

# LEVEL 2 - RECENT-WORK REVIEW

if ($Level -ge 2) {
    Write-Header "Level 2 - Recent-Work Review (last $Hours h)"

    $gitRoots      = Get-GitRoots
    $dirtyRepos    = @()
    $recentCommits = @()
    $changedFiles  = [System.Collections.Generic.HashSet[string]]::new()

    foreach ($repo in $gitRoots) {
        $repoName = Split-Path $repo -Leaf

        $dirty = & git -C $repo status --short 2>$null
        if ($dirty) { $dirtyRepos += $repoName }

        $log = & git -C $repo log "--since=$sinceStr" --oneline 2>$null
        foreach ($line in $log) {
            if ($line) { $recentCommits += "$repoName  $line" }
        }

        $files = & git -C $repo diff --name-only "HEAD@{$sinceStr}" HEAD 2>$null
        foreach ($f in $files) {
            if ($f) { [void]$changedFiles.Add("$repoName/$f") }
        }
    }

    if ($dirtyRepos.Count -eq 0) {
        Write-Pass "all $($gitRoots.Count) repos clean"
    } else {
        foreach ($d in $dirtyRepos) { Write-Warn "dirty: $d" }
        Write-Info "$($gitRoots.Count - $dirtyRepos.Count) of $($gitRoots.Count) repos clean"
    }

    if ($recentCommits.Count -eq 0) {
        Write-Info "no commits found in the last $Hours h"
    } else {
        Write-Pass "$($recentCommits.Count) commit(s) in the last $Hours h"
        if (-not $Summary) {
            $recentCommits | ForEach-Object { Write-Host "        $_" -ForegroundColor DarkGray }
        }
    }

    if ($changedFiles.Count -gt 0 -and -not $Summary) {
        Write-Info "$($changedFiles.Count) file(s) in diff window:"
        $changedFiles | Select-Object -First 30 | ForEach-Object { Write-Host "        $_" -ForegroundColor DarkGray }
        if ($changedFiles.Count -gt 30) { Write-Info "  ... and $($changedFiles.Count - 30) more" }
    }
}

# LEVEL 3 - ADVERSARIAL AUDIT

if ($Level -ge 3) {
    Write-Header "Level 3 - Adversarial Audit (last $Hours h)"

    # 3a. Open markers in recently-touched markdown
    #
    # Real false positives found live against this portfolio, fixed here:
    #   - "[ ]" matched every markdown checkbox, including DEV-RELEASE.md's
    #     legitimate, intentional entry-condition checklists - already
    #     counted correctly (scoped to the active release only) by 4a's
    #     Get-ActiveReleaseGaps. Removed from this pattern entirely; this
    #     scan is for stray debt markers, not planning checklists.
    #   - Case-insensitive matching caught ordinary prose using these words
    #     normally ("a footer placeholder", "leave it stubbed") - genuine
    #     markers in this portfolio are conventionally shouted (TODO,
    #     STUB, PLACEHOLDER); requiring exact case removes the prose hits
    #     without losing a real marker anyone actually writes that way.
    #   - Quoted mentions ("TBD" as the subject of a sentence prohibiting
    #     its use, not TBD used as a live marker) are excluded via
    #     lookaround - a marker is never wrapped in quotes on both sides.
    $openPattern = '(?<!["''`])\b(TODO|FIXME|TBD|PLACEHOLDER|STUB)\b(?!["''`])'
    $mdFiles = Get-ChildItem $root -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -gt $since -and $_.FullName -notmatch $excludeRegex }

    $markerHits = 0
    foreach ($f in $mdFiles) {
        $hits = Get-Content $f.FullName -ErrorAction SilentlyContinue |
            Select-String -Pattern $openPattern -CaseSensitive
        foreach ($h in $hits) {
            $markerHits++
            if (-not $Summary) {
                $rel = $f.FullName.Replace($root, "").TrimStart("\")
                Write-Find "${rel}:$($h.LineNumber)  $($h.Line.Trim())"
            }
        }
    }
    if ($markerHits -eq 0) {
        Write-Pass "no open markers (TODO/FIXME/TBD/STUB/PLACEHOLDER) in recently-touched markdown"
    } else {
        Write-Warn "$markerHits open marker(s) in recently-touched markdown"
    }

    # 3b. DEV-PLAN.md staleness: plan not touched but repo has new commits
    $planDocs = Get-ChildItem $root -Recurse -Filter "DEV-PLAN.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch $excludeRegex }

    $staleCount = 0
    foreach ($pd in $planDocs) {
        if ($pd.LastWriteTime -lt $since) {
            $repoDir  = Split-Path $pd.FullName -Parent
            $log = & git -C $repoDir log "--since=$sinceStr" --oneline 2>$null
            if ($log) {
                $staleCount++
                $rel = $pd.FullName.Replace($root, "").TrimStart("\")
                Write-Find "planning doc not updated but $($log.Count) new commit(s): $rel"
            }
        }
    }
    if ($staleCount -eq 0) {
        Write-Pass "DEV-PLAN.md files are current relative to recent commits"
    }

    # 3c. PLAY.jsonl preflight coverage
    $playFiles = Get-ChildItem $root -Recurse -Filter "PLAY.jsonl" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch $excludeRegex }

    if ($playFiles.Count -eq 0) {
        Write-Warn "no PLAY.jsonl found under $root - PLAY preflight coverage unknown"
    } else {
        $playTotal   = 0
        $playFail    = 0
        $playWarn    = 0
        $playPass    = 0

        foreach ($pf in $playFiles) {
            $lines = Get-Content $pf.FullName -ErrorAction SilentlyContinue
            foreach ($line in $lines) {
                $line = $line.Trim()
                if (-not $line) { continue }
                try {
                    $play = $line | ConvertFrom-Json -ErrorAction Stop
                } catch {
                    Write-Warn "PLAY.jsonl parse error in $($pf.FullName): $line"
                    continue
                }

                # Filter to the Hours window. declared_at may already be a [datetime] with
                # Kind Utc or Local (ConvertFrom-Json auto-converts ISO 8601 strings on some
                # PowerShell versions) or still a raw string. Normalize to UTC before comparing
                # against $sinceUtc so a Z-suffixed timestamp is not silently treated as naive
                # local time - see the validate-registry.ps1 timestamp fix for the same bug class.
                if ($play.declared_at) {
                    try {
                        if ($play.declared_at -is [datetime]) {
                            $playTime = if ($play.declared_at.Kind -eq [System.DateTimeKind]::Utc) { $play.declared_at } else { $play.declared_at.ToUniversalTime() }
                        } else {
                            $styles = [System.Globalization.DateTimeStyles]::AdjustToUniversal -bor [System.Globalization.DateTimeStyles]::AssumeUniversal
                            $playTime = [datetime]::Parse([string]$play.declared_at, [System.Globalization.CultureInfo]::InvariantCulture, $styles)
                        }
                        if ($playTime -lt $sinceUtc) { continue }
                    } catch { }
                }

                $playTotal++
                $id        = if ($play.play_id) { $play.play_id } else { "unknown" }
                $playLevel = if ($play.level)   { $play.level }   else { "?" }
                $pre       = $play.preflight

                if (-not $pre) {
                    $playFail++
                    Write-Fail "PLAY missing preflight field: $id ($playLevel)"
                } elseif ($pre -eq "not-yet-enforced") {
                    $playWarn++
                    Write-Warn "PLAY predates preflight enforcement: $id ($playLevel)"
                } elseif ($pre -eq "complete" -or $pre -eq "blocked") {
                    $playPass++
                    if (-not $Summary) { Write-Info "PLAY preflight $pre : $id ($playLevel)" }
                } else {
                    $playFail++
                    Write-Fail "PLAY has unrecognised preflight value '$pre': $id ($playLevel)"
                }

                # DEV-DOCS deferred is a warning
                if ($play.dev_docs_check -and $play.dev_docs_check.status -eq "deferred") {
                    Write-Warn "PLAY has deferred DEV-DOCS check: $id - $($play.dev_docs_check.note)"
                }
            }
        }

        if ($playTotal -eq 0) {
            Write-Info "PLAY.jsonl found but no plays in the last $Hours h"
        } elseif ($playFail -eq 0) {
            Write-Pass "PLAY preflight coverage: $playPass pass, $playWarn warn, 0 fail of $playTotal play(s)"
        } else {
            Write-Fail "PLAY preflight gaps: $playFail fail, $playWarn warn of $playTotal play(s)"
        }
    }
}

# LEVEL 4 - RELEASE READINESS

if ($Level -ge 4) {
    Write-Header "Level 4 - Release Readiness"

    # 4a. DEV-RELEASE.md real unchecked gates - structural, scoped to the
    # active release candidate (Get-ActiveReleaseVersion / -Gaps above),
    # not a keyword scan of the whole file. A future release's own
    # unchecked entry conditions (e.g. cockpit's v1.1.0/v2.0.0 rows) are
    # not this repo's current gate and must not be reported as one; a
    # real open gate in the *active* release (cockpit's real, unfinished
    # v1.0.0 checklist) must still be caught.
    $releaseDocs = Get-ChildItem $root -Recurse -Filter "DEV-RELEASE.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch $excludeRegex }

    $pendingCount = 0
    foreach ($rd in $releaseDocs) {
        $gaps = Get-ActiveReleaseGaps $rd.FullName
        if ($gaps.Count -gt 0) {
            $rel = $rd.FullName.Replace($root, "").TrimStart("\")
            Write-Find "$($gaps.Count) unchecked gate(s) in the active release: $rel"
            if (-not $Summary) {
                foreach ($g in $gaps) { Write-Host "        - [ ] $g" -ForegroundColor DarkYellow }
            }
            $pendingCount++
        }
    }
    if ($pendingCount -eq 0) {
        Write-Pass "no unchecked gates in any active release candidate"
    } else {
        Write-Warn "$pendingCount DEV-RELEASE.md file(s) with unchecked gates in their active release"
    }

    # 4b. Open PASS gates - reads each file's own authoritative Status
    # field (Get-PassStatus above), never a whole-file substring match,
    # which false-positives on prose that merely mentions the word inside
    # an example (CANON.02's real Status is ACCEPTED; its body separately
    # discusses registry *entry* statuses, unrelated to its own).
    $passDir = Join-Path $root "passes"
    if (-not (Test-Path $passDir)) {
        $passDir = Join-Path $root "governance-commons\passes"
    }
    if (Test-Path $passDir) {
        $openPasses    = @()
        $unknownStatus = @()
        Get-ChildItem $passDir -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch $excludeRegex } |
            ForEach-Object {
                $status = Get-PassStatus $_.FullName
                if ($null -eq $status) {
                    $unknownStatus += $_
                } elseif ($status -match "(?i)(open|draft|in.progress|pending)") {
                    $openPasses += $_
                }
            }
        if ($openPasses.Count -eq 0) {
            Write-Pass "no open PASS gates"
        } else {
            Write-Warn "$($openPasses.Count) open PASS gate(s):"
            if (-not $Summary) {
                foreach ($p in $openPasses) {
                    Write-Find $p.FullName.Replace($root, "").TrimStart("\")
                }
            }
        }
        if ($unknownStatus.Count -gt 0 -and -not $Summary) {
            foreach ($p in $unknownStatus) {
                Write-Info "no recognized Status field: $($p.FullName.Replace($root, '').TrimStart('\'))"
            }
        }
    } else {
        Write-Info "passes directory not found; PASS gate check skipped"
    }
}

# footer

Write-Host ""
Write-Host "-------------------------------------------------------------" -ForegroundColor DarkGray
if ($exitFail) {
    Write-Host "Result: FAIL - one or more checks did not pass at Level $Level." -ForegroundColor Red
    exit 1
} else {
    Write-Host "Result: PASS - all checks clean at Level $Level (last $Hours h)." -ForegroundColor Green
    exit 0
}
