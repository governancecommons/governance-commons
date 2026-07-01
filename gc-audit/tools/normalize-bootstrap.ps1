<#
.SYNOPSIS
    Normalizes agent bootstrap files to DEV-ACCORD.04 conformance.

.DESCRIPTION
    Fixes two categories of drift detected by validate-bootstrap.ps1:

    W1 — Repo has planning docs but no AGENTS.md.
         Fix: create a minimal thin-adapter AGENTS.md pointing to DEV-ACCORD.03.

    E1 — AGENTS.md exists but does not reference DEV-ACCORD.03.
         Fix: prepend the canonical routing line.

    Use -DryRun to preview changes without writing anything.
    Run validate-bootstrap.ps1 after to confirm.

.PARAMETER DryRun
    Preview fixes; do not write any files.

.PARAMETER TargetPath
    Portfolio root (default: current directory).

.PARAMETER Project
    Normalize only a named repo path relative to TargetPath.
#>
param(
    [switch] $DryRun,
    [string] $TargetPath = ".",
    [string] $Project    = ""
)

$Root     = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$Accord03 = Join-Path $Root "governance-commons\passes\dev-accord\DEV-ACCORD.03.md"
$Fixed    = 0
$Skipped  = 0

function Write-Action([string]$verb, [string]$path, [string]$note = "") {
    $rel   = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    $color = if ($script:DryRun) { "Cyan" } else { "Green" }
    $tag   = if ($script:DryRun) { "WOULD" } else { "  FIX" }
    Write-Host "  $tag  $verb  $rel" -ForegroundColor $color
    if ($note) { Write-Host "        $note" -ForegroundColor DarkGray }
}

function Write-Skip([string]$path, [string]$reason) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  SKIP  $rel — $reason" -ForegroundColor DarkGray
    $script:Skipped++
}

function Write-Already([string]$path) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  OK    $rel" -ForegroundColor DarkGreen
}

function Get-RelativeAccordPath([string]$repoRoot) {
    # Compute a forward-slash relative path from $repoRoot to DEV-ACCORD.03.md
    $rel = [System.IO.Path]::GetRelativePath($repoRoot, $Accord03)
    return $rel.Replace("\", "/")
}

function New-ThinAdapter([string]$repoRoot) {
    $agents  = Join-Path $repoRoot "AGENTS.md"
    $relPath = Get-RelativeAccordPath $repoRoot

    $content = @"
# AGENTS.md — GC bootstrap

Read [$relPath]($relPath) before taking any action. That file is the canonical agent onboarding protocol for this portfolio.

This file is the GC cross-agent bootstrap for this repository. Some runtimes auto-discover it; others need a host, adapter, or explicit instruction to read it. Any agent claiming GC conformance must read it before acting.
"@

    Write-Action "CREATE" $agents "routing to: $relPath"
    if (-not $DryRun) {
        Set-Content -Path $agents -Value $content -Encoding UTF8
        $script:Fixed++
    }
}

function Add-RoutingLine([string]$agentsFile, [string]$repoRoot) {
    $relPath  = Get-RelativeAccordPath $repoRoot
    $existing = Get-Content -Raw -Encoding UTF8 $agentsFile
    $routing  = "Read [$relPath]($relPath) before taking any action. That file is the canonical agent onboarding protocol for this portfolio.`n`n"

    Write-Action "PREPEND" $agentsFile "add routing line: $relPath"
    if (-not $DryRun) {
        Set-Content -Path $agentsFile -Value ($routing + $existing) -Encoding UTF8
        $script:Fixed++
    }
}

function Test-PointsToBootstrapAuthority([string]$text) {
    return (
        $text -match 'DEV-ACCORD\.03' -or
        $text -match 'passes/dev-accord/DEV-ACCORD\.03\.md' -or
        $text -match 'passes\\dev-accord\\DEV-ACCORD\.03\.md'
    )
}

function Normalize-RepoBootstrap([string]$repoRoot) {
    $agents     = Join-Path $repoRoot "AGENTS.md"
    $hasPlanning = (Test-Path (Join-Path $repoRoot "DEV-PATH.md")) -or (Test-Path (Join-Path $repoRoot "DEV-PLAN.md"))
    $hasAgents   = Test-Path $agents

    if (-not $hasPlanning -and -not $hasAgents) { return }

    if ($hasPlanning -and -not $hasAgents) {
        # W1: planning exists, no bootstrap
        if (-not (Test-Path $Accord03)) {
            Write-Skip $repoRoot "DEV-ACCORD.03.md not found at expected path; cannot generate routing line"
            return
        }
        New-ThinAdapter $repoRoot
        return
    }

    if ($hasAgents) {
        $text = Get-Content -Raw -Encoding UTF8 $agents
        if (Test-PointsToBootstrapAuthority $text) {
            Write-Already $agents
        } else {
            # E1: exists but no routing
            if (-not (Test-Path $Accord03)) {
                Write-Skip $agents "DEV-ACCORD.03.md not found; cannot add routing line"
                return
            }
            Add-RoutingLine $agents $repoRoot
        }
    }
}

# ── discover repo roots (same logic as validate-bootstrap) ───────────────────

$RepoRoots = [System.Collections.Generic.List[string]]::new()

if ($Project) {
    $projectRoot = Join-Path $Root $Project
    if (-not (Test-Path $projectRoot)) {
        Write-Host "Project path not found: $projectRoot" -ForegroundColor Red
        exit 1
    }
    $RepoRoots.Add((Resolve-Path $projectRoot).Path)
} else {
    $RepoRoots.Add($Root)
    $gitMarkers = Get-ChildItem -Path $Root -Recurse -Depth 4 -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -eq ".git" -and
            $_.FullName -notmatch '(?i)([\\/](node_modules|archive|_archive|\.claude[\\/]worktrees|\.pytest_cache|dist|\.venv|\.eco)[\\/]|[\\/]state-snapshot)'
        }
    foreach ($marker in $gitMarkers) {
        $repoRoot = Split-Path $marker.FullName -Parent
        if (-not $RepoRoots.Contains($repoRoot)) { $RepoRoots.Add($repoRoot) }
    }
}

# ── run ───────────────────────────────────────────────────────────────────────

$dryTag = if ($DryRun) { " [DRY RUN — no files written]" } else { "" }
Write-Host ""
Write-Host "  normalize-bootstrap.ps1$dryTag" -ForegroundColor White
Write-Host "  Standard: DEV-ACCORD.04 (GC:2012)  |  $($RepoRoots.Count) roots  |  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray
Write-Host ""

foreach ($r in $RepoRoots) {
    Normalize-RepoBootstrap $r
}

Write-Host ""
if ($DryRun) {
    Write-Host "  Dry run complete. Re-run without -DryRun to apply." -ForegroundColor Cyan
} else {
    Write-Host "  $Fixed fix(es) applied. $Skipped skipped." -ForegroundColor $(if ($Fixed -gt 0) { "Green" } else { "DarkGray" })
    if ($Fixed -gt 0) {
        Write-Host "  Run validate-bootstrap.ps1 to confirm." -ForegroundColor DarkGray
    }
}
Write-Host ""
