<#
.SYNOPSIS
    Normalizes broken file pointers in projects.yaml.

.DESCRIPTION
    Reads every file pointer in projects.yaml, checks whether it resolves on
    disk, and attempts to fix broken ones using common rename heuristics:

      TRACKS.md  -> DEV-TRACKS.md   (same directory)
      Tracks.md  -> DEV-TRACKS.md   (same directory)
      dev_plan.md -> DEV-PLAN.md    (case/separator normalization)
      dev_path.md -> DEV-PATH.md
      dev-plan.md -> DEV-PLAN.md    (lowercase -> upper)
      dev-path.md -> DEV-PATH.md

    Pointers that are broken and have no fixable candidate are reported as
    UNFIXABLE and left unchanged; resolve them manually.

    Use -DryRun to preview changes without modifying projects.yaml.
    Run validate-pointers.ps1 after to confirm.

.PARAMETER DryRun
    Preview fixes; do not write projects.yaml.

.PARAMETER TargetPath
    Portfolio root (default: current directory).
#>
param(
    [switch] $DryRun,
    [string] $TargetPath = "."
)

$Root         = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$ProjectsFile = Join-Path $Root "projects.yaml"

if (-not (Test-Path $ProjectsFile)) {
    Write-Host "projects.yaml not found: $ProjectsFile" -ForegroundColor Red
    exit 1
}

# Heuristic rename map: old leaf name -> new leaf name
# Keys are matched case-insensitively at lookup time; one entry per canonical target.
$RenameMap = [ordered]@{
    "TRACKS.md"   = "DEV-TRACKS.md"
    "DEV_TRACKS.md" = "DEV-TRACKS.md"
    "dev-tracks.md" = "DEV-TRACKS.md"
    "DEV_PLAN.md" = "DEV-PLAN.md"
    "dev-plan.md" = "DEV-PLAN.md"
    "DEV_PATH.md" = "DEV-PATH.md"
    "dev-path.md" = "DEV-PATH.md"
}

$yaml    = Get-Content $ProjectsFile -Raw
$updated = $yaml

$fileKeys = 'canonical|path|tracks|roadmap|implementation_plan|domain_plan|project|changelog|alternate_status|review_grammar|track'
$matches  = [regex]::Matches($yaml, "(?m)^\s+($fileKeys):\s+(.+)$")

$fixed     = 0
$unfixable = 0
$ok        = 0

$dryTag = if ($DryRun) { " [DRY RUN — no files written]" } else { "" }
Write-Host ""
Write-Host "  normalize-pointers.ps1$dryTag" -ForegroundColor White
Write-Host "  source: $ProjectsFile  |  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray
Write-Host ""

foreach ($m in $matches) {
    $pointer = $m.Groups[2].Value.Trim().Trim('"')
    if ($pointer -match '^https?://' -or $pointer -match '^#') { continue }

    $full = Join-Path $Root $pointer
    if (Test-Path $full) {
        $ok++
        continue
    }

    # broken — try heuristics
    $dir      = Split-Path $pointer -Parent
    $leaf     = Split-Path $pointer -Leaf
    $fixed_p  = $null

    $matchKey = $RenameMap.Keys | Where-Object { $_ -ieq $leaf } | Select-Object -First 1
    if ($matchKey) {
        $candidate = if ($dir) { "$dir/$($RenameMap[$matchKey])" } else { $RenameMap[$matchKey] }
        $candidateFull = Join-Path $Root $candidate
        if (Test-Path $candidateFull) {
            $fixed_p = $candidate
        }
    }

    if ($fixed_p) {
        Write-Host "  FIX   $pointer" -ForegroundColor $(if ($DryRun) { "Cyan" } else { "Green" })
        Write-Host "     -> $fixed_p" -ForegroundColor $(if ($DryRun) { "Cyan" } else { "Green" })
        if (-not $DryRun) {
            $updated = $updated.Replace($pointer, $fixed_p)
        }
        $fixed++
    } else {
        Write-Host "  MISS  $pointer  (no fixable candidate found)" -ForegroundColor Yellow
        $unfixable++
    }
}

Write-Host ""

if ($fixed -eq 0 -and $unfixable -eq 0) {
    Write-Host "  All $ok pointer(s) already resolve. Nothing to fix." -ForegroundColor Green
} else {
    if (-not $DryRun -and $fixed -gt 0) {
        Set-Content -Path $ProjectsFile -Value $updated -Encoding UTF8 -NoNewline
    }
    $color = if ($unfixable -gt 0) { "Yellow" } else { "Green" }
    Write-Host "  $fixed fix(es) applied. $unfixable unfixable (manual). $ok already OK." -ForegroundColor $color
    if ($DryRun -and $fixed -gt 0) {
        Write-Host "  Re-run without -DryRun to apply." -ForegroundColor Cyan
    } elseif ($fixed -gt 0) {
        Write-Host "  Run validate-pointers.ps1 to confirm." -ForegroundColor DarkGray
    }
    if ($unfixable -gt 0) { exit 1 }
}

Write-Host ""
