<#
.SYNOPSIS
    Adversarial closing review for the last 24 hours of portfolio work.

.DESCRIPTION
    Runs validate-recent-work.ps1 at Level 2 (or higher with -Deep) and
    formats the output as a human-readable closing-ritual report.

    Use this at the end of a work session to confirm everything landed cleanly.

.PARAMETER Hours
    Review window in hours (default 24).

.PARAMETER Deep
    Run Level 3 (adversarial). Use -Deeper for Level 4 (release readiness).

.PARAMETER Deeper
    Run Level 4 (release readiness). Implies -Deep.

.PARAMETER Summary
    Pass --summary to validate-recent-work (compact output).
#>
param(
    [int]    $Hours   = 24,
    [string] $TargetPath = ".",
    [switch] $Deep,
    [switch] $Deeper,
    [switch] $Summary
)

$root     = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$toolRoot = $PSScriptRoot
$level    = 2
if ($Deep)   { $level = 3 }
if ($Deeper) { $level = 4 }

$levelLabel = @{ 2="Recent-Work Review"; 3="Adversarial Audit"; 4="Release Readiness" }

$border = "═" * 65

Write-Host ""
Write-Host $border -ForegroundColor Cyan
Write-Host "  REVIEW — LAST $Hours H  |  Level $level – $($levelLabel[$level])" -ForegroundColor White
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  |  $env:COMPUTERNAME" -ForegroundColor DarkGray
Write-Host $border -ForegroundColor Cyan

$script  = Join-Path $toolRoot "validate-recent-work.ps1"
$args    = @("-Hours", $Hours, "-Level", $level, "-TargetPath", $root)
if ($Summary) { $args += "-Summary" }

& pwsh -NoProfile -File $script @args
$rc = $LASTEXITCODE

Write-Host $border -ForegroundColor Cyan
if ($rc -eq 0) {
    Write-Host "  SESSION CLOSED CLEAN" -ForegroundColor Green
} else {
    Write-Host "  SESSION CLOSED WITH FINDINGS — review items above before pushing" -ForegroundColor Red
}
Write-Host $border -ForegroundColor Cyan
Write-Host ""

exit $rc
