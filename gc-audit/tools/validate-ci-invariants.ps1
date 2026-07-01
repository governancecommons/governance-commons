<#
.SYNOPSIS
    Validates DEV-ACCORD-CI invariant ID uniqueness across markdown definition lines.

.DESCRIPTION
    Scans markdown files under TargetPath and extracts invariant definition lines of the form:
      DEV-ACCORD-CI-<n> - ...
      DEV-ACCORD-CI-<n> <em dash> ...
      **DEV-ACCORD-CI-<n> - ...**
      **DEV-ACCORD-CI-<n> <em dash> ...**

    Reports duplicate IDs with file and line locations. Exits non-zero on duplicates.

.PARAMETER TargetPath
    Repository root to scan.

.PARAMETER Project
    Optional child project path relative to TargetPath.

.PARAMETER Help
    Show help and exit.
#>
param(
    [string]$TargetPath = ".",
    [string]$Project = "",
    [switch]$Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$ErrorActionPreference = 'Stop'

$root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
if ($Project) {
    $root = Join-Path $root $Project
}
if (-not (Test-Path -LiteralPath $root)) {
    Write-Host "[ERROR] Target path not found: $root" -ForegroundColor Red
    exit 1
}

$excludeRegex = '(?i)[\\/](\.git|node_modules|_archive|_tmp|dist|build|out|coverage|\.venv|\.pytest_cache)[\\/]'
$definitionRegex = '^\s*(?:\*\*)?DEV-ACCORD-CI-(?<id>\d+)(?!\s+(?:and|through)\b)(?:\*\*)?\s+\S'

$findings = [System.Collections.Generic.List[object]]::new()

Get-ChildItem -Path $root -Recurse -File -Filter *.md -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch $excludeRegex } |
    ForEach-Object {
        $file = $_.FullName
        $rel = $file.Replace($root + '\\', '').Replace($root + '/', '')
        $lineNo = 0
        Get-Content -LiteralPath $file | ForEach-Object {
            $lineNo++
            if ($_ -match $definitionRegex) {
                $findings.Add([PSCustomObject]@{
                    Id   = [int]$Matches['id']
                    File = $rel
                    Line = $lineNo
                    Text = $_.Trim()
                })
            }
        }
    }

Write-Host ""
Write-Host "  DEV-ACCORD CI UNIQUENESS CHECK - validate-ci-invariants.ps1" -ForegroundColor White
Write-Host "  Root: $root" -ForegroundColor DarkGray
Write-Host ""

if ($findings.Count -eq 0) {
    Write-Host "  [WARN] No DEV-ACCORD-CI definition lines found." -ForegroundColor DarkYellow
    Write-Host ""
    exit 0
}

$dups = $findings | Group-Object Id | Where-Object { $_.Count -gt 1 } | Sort-Object { [int]$_.Name }

if (-not $dups) {
    $ids = ($findings.Id | Sort-Object -Unique)
    Write-Host "  [PASS] Unique DEV-ACCORD-CI IDs. Count: $($ids.Count)" -ForegroundColor Green
    Write-Host "  IDs: $($ids -join ', ')" -ForegroundColor DarkGray
    Write-Host ""
    exit 0
}

foreach ($g in $dups) {
    Write-Host "  [ERROR] CI-$($g.Name) is duplicated ($($g.Count) definitions)" -ForegroundColor Red
    foreach ($row in $g.Group) {
        Write-Host "          $($row.File):$($row.Line)" -ForegroundColor DarkYellow
    }
}
Write-Host ""
exit 1
