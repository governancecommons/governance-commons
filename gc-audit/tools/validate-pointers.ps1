# validate-pointers.ps1
# Checks that all planning file pointers in projects.yaml resolve on disk.
# Run manually or add to CI.
#
# Usage: pwsh -File validate-pointers.ps1 [-TargetPath C:\work] [-FixNotes]
#   --fix-notes  Report projects with only a notes: pointer (no file to verify)

param(
    [string]$TargetPath = ".",
    [switch]$FixNotes
)

$root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$projectsFile = Join-Path $root "projects.yaml"

if (-not (Test-Path $root)) {
    Write-Host "Target path does not exist: $TargetPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $projectsFile)) {
    Write-Host "projects.yaml not found in target path: $root" -ForegroundColor Red
    exit 1
}

$yaml = Get-Content $projectsFile -Raw

$broken = @()
$ok = @()
$noteOnly = @()

# Extract all path-like values under planning: blocks
# Matches lines like:  canonical: some/path.md
$fileKeys = 'canonical|path|tracks|roadmap|implementation_plan|domain_plan|project|changelog|alternate_status|review_grammar'
$matches = [regex]::Matches($yaml, "(?m)^\s+($fileKeys):\s+(.+)$")

foreach ($m in $matches) {
    $pointer = $m.Groups[2].Value.Trim().Trim('"')
    # Skip if it looks like a URL or inline note
    if ($pointer -match '^https?://' -or $pointer -match '^#') { continue }
    $full = Join-Path $root $pointer
    if (Test-Path $full) {
        $ok += $pointer
    } else {
        $broken += $pointer
    }
}

# Report
if ($broken.Count -eq 0) {
    Write-Host "All $($ok.Count) planning pointers resolve." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "BROKEN ($($broken.Count) of $($ok.Count + $broken.Count) pointers):" -ForegroundColor Red
    $broken | ForEach-Object { Write-Host "  MISS  $_" -ForegroundColor Yellow }
    Write-Host ""
    Write-Host "OK ($($ok.Count)):" -ForegroundColor DarkGray
    $ok | ForEach-Object { Write-Host "  OK    $_" -ForegroundColor DarkGray }
    Write-Host ""
    exit 1
}

if ($FixNotes) {
    # Find projects with only notes: under planning (no file pointers)
    $noteMatches = [regex]::Matches($yaml, "(?ms)planning:\s*\n(\s+notes:[^\n]+\n)(?!\s+($fileKeys):)")
    Write-Host "`nProjects with notes-only planning ($($noteMatches.Count)):" -ForegroundColor Cyan
    $noteMatches | ForEach-Object { Write-Host "  " $_.Groups[1].Value.Trim() }
}
