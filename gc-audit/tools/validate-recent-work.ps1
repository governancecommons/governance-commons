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
$exitFail = $false
$powerShellHost = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$isWindowsHost = ($env:OS -eq "Windows_NT")

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
    if (Test-Path (Join-Path $root ".git")) { $roots += $root }
    Get-ChildItem $root -Directory -Depth 2 -ErrorAction SilentlyContinue | ForEach-Object {
        if (Test-Path (Join-Path $_.FullName ".git")) { $roots += $_.FullName }
    }
    return $roots | Select-Object -Unique
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
    [PSCustomObject]@{ Name="DEV-PLAYBOOK records";             Script="validate-playbook.ps1";       PortfolioOnly=$false; RequiresFile="PLAY.jsonl" }
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
    $openPattern = "TODO|FIXME|TBD|\[ \]|PLACEHOLDER|STUB"
    $mdFiles = Get-ChildItem $root -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime -gt $since -and $_.FullName -notmatch '\\node_modules\\|\\\.git\\' }

    $markerHits = 0
    foreach ($f in $mdFiles) {
        $hits = Get-Content $f.FullName -ErrorAction SilentlyContinue |
            Select-String -Pattern $openPattern
        foreach ($h in $hits) {
            $markerHits++
            if (-not $Summary) {
                $rel = $f.FullName.Replace($root, "").TrimStart("\")
                Write-Find "${rel}:$($h.LineNumber)  $($h.Line.Trim())"
            }
        }
    }
    if ($markerHits -eq 0) {
        Write-Pass "no open markers (TODO/FIXME/TBD/STUB) in recently-touched markdown"
    } else {
        Write-Warn "$markerHits open marker(s) in recently-touched markdown"
    }

    # 3b. DEV-PLAN.md staleness: plan not touched but repo has new commits
    $planDocs = Get-ChildItem $root -Recurse -Filter "DEV-PLAN.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch '\\\.git\\' }

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
        Where-Object { $_.FullName -notmatch '\\\.git\\|\\node_modules\\' }

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

                # Filter to the Hours window
                if ($play.declared_at) {
                    try {
                        $playTime = [datetime]::Parse($play.declared_at)
                        if ($playTime -lt $since) { continue }
                    } catch { }
                }

                $playTotal++
                $id    = if ($play.play_id) { $play.play_id } else { "unknown" }
                $level = if ($play.level)   { $play.level }   else { "?" }
                $pre   = $play.preflight

                if (-not $pre) {
                    $playFail++
                    Write-Fail "PLAY missing preflight field: $id ($level)"
                } elseif ($pre -eq "not-yet-enforced") {
                    $playWarn++
                    Write-Warn "PLAY predates preflight enforcement: $id ($level)"
                } elseif ($pre -eq "complete" -or $pre -eq "blocked") {
                    $playPass++
                    if (-not $Summary) { Write-Info "PLAY preflight $pre : $id ($level)" }
                } else {
                    $playFail++
                    Write-Fail "PLAY has unrecognised preflight value '$pre': $id ($level)"
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

    # 4a. DEV-RELEASE.md pending items
    $releaseDocs = Get-ChildItem $root -Recurse -Filter "DEV-RELEASE.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch '\\\.git\\' }

    $pendingCount = 0
    foreach ($rd in $releaseDocs) {
        $c = Get-Content $rd.FullName -Raw -ErrorAction SilentlyContinue
        if ($c -match "(?i)(pending|blocked|not ready|tbd|todo)") {
            $rel = $rd.FullName.Replace($root, "").TrimStart("\")
            Write-Find "pending release items: $rel"
            $pendingCount++
        }
    }
    if ($pendingCount -eq 0) {
        Write-Pass "no pending items in DEV-RELEASE.md files"
    } else {
        Write-Warn "$pendingCount DEV-RELEASE.md file(s) with pending items"
    }

    # 4b. Open PASS gates
    $passDir = Join-Path $root "governance-commons\passes"
    if (Test-Path $passDir) {
        $openPasses = Get-ChildItem $passDir -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -notmatch '\\\.git\\' } |
            Where-Object {
                $c = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
                $c -match "(?i)status:\s*(open|draft|in.progress|pending)"
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
    } else {
        Write-Info "governance-commons/passes not found; PASS gate check skipped"
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
