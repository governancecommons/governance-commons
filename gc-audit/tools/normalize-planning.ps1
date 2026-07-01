<#
.SYNOPSIS
    Normalizes planning doc file names to DEV-ACCORD.00 conventions.

.DESCRIPTION
    Finds planning documents with non-standard names and renames them using
    git mv so history is preserved. Also updates any references to the old
    names in projects.yaml.

    Handled renames:
      TRACKS.md / Tracks.md / tracks.md -> DEV-TRACKS.md
      DEV_PLAN.md / dev-plan.md / dev_plan.md -> DEV-PLAN.md
      DEV_PATH.md / dev-path.md / dev_path.md -> DEV-PATH.md
      DEV_RELEASE.md / dev-release.md        -> DEV-RELEASE.md
      DEV_TRACKS.md  / dev-tracks.md         -> DEV-TRACKS.md

    Skips files already at the canonical name, and skips repos where the
    target canonical name already exists (no destructive overwrite).

    Use -DryRun to preview without changing any files.
    Run validate-planning.ps1 after to confirm.

.PARAMETER DryRun
    Preview renames; do not modify files.

.PARAMETER TargetPath
    Portfolio root (default: current directory).
#>
param(
    [switch] $DryRun,
    [string] $TargetPath = "."
)

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)

# Map: non-canonical name pattern (case-insensitive leaf) -> canonical name
# Keys are matched case-insensitively at lookup time; only one entry per target needed.
$Canonicals = [ordered]@{
    "TRACKS.md"      = "DEV-TRACKS.md"
    "DEV_TRACKS.md"  = "DEV-TRACKS.md"
    "dev-tracks.md"  = "DEV-TRACKS.md"
    "DEV_PLAN.md"    = "DEV-PLAN.md"
    "dev-plan.md"    = "DEV-PLAN.md"
    "DEV_PATH.md"    = "DEV-PATH.md"
    "dev-path.md"    = "DEV-PATH.md"
    "DEV_RELEASE.md" = "DEV-RELEASE.md"
    "dev-release.md" = "DEV-RELEASE.md"
}

$Renamed   = 0
$Skipped   = 0
$Conflicts = 0

$dryTag = if ($DryRun) { " [DRY RUN — no files written]" } else { "" }
Write-Host ""
Write-Host "  normalize-planning.ps1$dryTag" -ForegroundColor White
Write-Host "  Standard: DEV-ACCORD.00 (GC:2008)  |  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor DarkGray
Write-Host ""

# Collect candidate files to rename
$candidates = Get-ChildItem $Root -Recurse -Filter "*.md" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch '\\\.git\\|\\node_modules\\|\\\.claude\\|\\_archive\\|\\\.venv\\|\\\.eco\\|\\state-snapshots\\'
    } |
    Where-Object {
        $n = $_.Name
        $key = $Canonicals.Keys | Where-Object { $_ -ieq $n } | Select-Object -First 1
        # Only flag files whose name differs from the canonical (case-sensitive)
        $key -and ($Canonicals[$key] -cne $n)
    }

if ($candidates.Count -eq 0) {
    Write-Host "  No non-standard planning doc names found." -ForegroundColor Green
    Write-Host ""
    exit 0
}

foreach ($f in $candidates) {
    $matchKey     = $Canonicals.Keys | Where-Object { $_ -ieq $f.Name } | Select-Object -First 1
    $canonical    = $Canonicals[$matchKey]
    $dir          = $f.DirectoryName
    $targetPath   = Join-Path $dir $canonical

    if (Test-Path $targetPath) {
        $relTarget = $targetPath.Replace($Root + "\", "")
        $relSource = $f.FullName.Replace($Root + "\", "")
        Write-Host "  SKIP  $relSource -> $canonical (target already exists: $relTarget)" -ForegroundColor Yellow
        $Skipped++
        $Conflicts++
        continue
    }

    $relSource = $f.FullName.Replace($Root + "\", "")
    $color     = if ($DryRun) { "Cyan" } else { "Green" }
    $tag       = if ($DryRun) { "WOULD" } else { "  FIX" }
    Write-Host "  $tag  git mv  $relSource -> $canonical" -ForegroundColor $color

    if (-not $DryRun) {
        # Use git mv to preserve history; fall back to plain rename if not in a git repo
        $gitRoot = & git -C $dir rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $gitRoot) {
            $relFromGit  = $f.FullName.Replace($gitRoot.TrimEnd('\') + "\", "").Replace("\", "/")
            $dirFromGit  = Split-Path $relFromGit -Parent
            $destFromGit = if ($dirFromGit) { "$dirFromGit/$canonical" } else { $canonical }
            & git -C $gitRoot mv $relFromGit $destFromGit 2>$null
            if ($LASTEXITCODE -ne 0) {
                # git mv failed (file not tracked); fall back to plain rename
                Rename-Item -Path $f.FullName -NewName $canonical
            }
        } else {
            Rename-Item -Path $f.FullName -NewName $canonical
        }
        $Renamed++
    }
}

# Update projects.yaml: replace only full path values that end with the old leaf name.
# Anchors on "/" + old leaf + end-of-value to avoid partial matches (e.g. TRACKS.md inside DEV-TRACKS.md).
if (-not $DryRun -and $Renamed -gt 0) {
    $pf = Join-Path $Root "projects.yaml"
    if (Test-Path $pf) {
        $yaml    = Get-Content $pf -Raw
        $changed = $false
        foreach ($old in $Canonicals.Keys) {
            $new     = $Canonicals[$old]
            # Match: /OLD_LEAF at end of a yaml value line (not inside DEV- prefix)
            $pattern = "(?<=/)" + [regex]::Escape($old) + "(?=\s*$)"
            if ($yaml -match $pattern) {
                $yaml    = [regex]::Replace($yaml, $pattern, $new, [System.Text.RegularExpressions.RegexOptions]::Multiline)
                $changed = $true
            }
        }
        if ($changed) {
            Set-Content -Path $pf -Value $yaml -Encoding UTF8 -NoNewline
            Write-Host ""
            Write-Host "  Updated references in projects.yaml." -ForegroundColor DarkGray
        }
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "  Dry run complete. Re-run without -DryRun to apply." -ForegroundColor Cyan
} else {
    $color = if ($Conflicts -gt 0) { "Yellow" } else { "Green" }
    Write-Host "  $Renamed rename(s) applied. $Skipped skipped ($Conflicts conflict(s))." -ForegroundColor $color
    if ($Renamed -gt 0) {
        Write-Host "  Run validate-planning.ps1 to confirm." -ForegroundColor DarkGray
    }
}
Write-Host ""

if ($Conflicts -gt 0) { exit 1 }
