<#
.SYNOPSIS
    Provider-based format/syntax validation for GC-AUDIT scripts.

.DESCRIPTION
    Provider-based validation surface for repository format checks. Phase 1 has
    one active provider: powershell-script-parse. It validates that every .ps1 file
    under the target scope parses cleanly using the PowerShell language parser.
    This is a parse-only check: no script is executed, dot-sourced, or invoked.
    It catches broken syntax before a script is registered in GC-AUDIT-REGISTRY.yaml
    or relied on by validate-recent-work.ps1.

    Scope: script paths registered in GC-AUDIT-REGISTRY.yaml plus *.ps1 files
    directly under TargetPath (root compatibility adapters), excluding common
    non-source directories. If no registry is present, the provider falls back to
    TargetPath\gc-audit\tools when present.

.PARAMETER TargetPath
    Root to scan (default: current directory).

.PARAMETER Help
    Show help and exit.
#>
param(
    [string] $TargetPath = ".",
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

Set-StrictMode -Version Latest

$root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)

if (-not (Test-Path -LiteralPath $root)) {
    Write-Host "[ERROR] Target path not found: $root" -ForegroundColor Red
    exit 1
}

$excludeRegex = '(?i)[\\/](\.git|node_modules|_archive|_tmp|dist|build|out|coverage|\.venv|\.pytest_cache)[\\/]'

$activeProviders = @(
    [PSCustomObject]@{
        Id = "powershell-script-parse"
        Pattern = "*.ps1"
        Mutates = $false
        ExecutesTarget = $false
    }
)

$scriptFiles = [System.Collections.Generic.List[string]]::new()

function Add-ScriptFile([string]$PathValue) {
    if (-not $PathValue) { return }
    if ((Test-Path -LiteralPath $PathValue) -and ($PathValue -notmatch $excludeRegex)) {
        $scriptFiles.Add($PathValue)
    }
}

function Resolve-RegistryScriptPath([string]$ScriptRef) {
    $candidate = Join-Path $root $ScriptRef
    if (Test-Path -LiteralPath $candidate) { return $candidate }

    $normalized = $ScriptRef -replace '/', '\'
    $prefix = "governance-commons\"
    if ($normalized.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $stripped = $normalized.Substring($prefix.Length)
        $candidate = Join-Path $root $stripped
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }

    return $null
}

$registryCandidates = @(
    (Join-Path $root "gc-audit\GC-AUDIT-REGISTRY.yaml"),
    (Join-Path $root "governance-commons\gc-audit\GC-AUDIT-REGISTRY.yaml")
)

$registryFile = $registryCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1

if ($registryFile) {
    $registryLines = Get-Content -LiteralPath $registryFile -ErrorAction SilentlyContinue
    foreach ($line in $registryLines) {
        if ($line -match '^\s*-\s+script:\s+(.+?)\s*$') {
            $scriptRef = $Matches[1].Trim().Trim('"').Trim("'")
            Add-ScriptFile (Resolve-RegistryScriptPath $scriptRef)
        }
    }
}

$toolsDir = Join-Path $root "gc-audit\tools"
if (-not $registryFile -and (Test-Path -LiteralPath $toolsDir)) {
    Get-ChildItem -Path $toolsDir -Filter *.ps1 -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch $excludeRegex } |
        ForEach-Object { $scriptFiles.Add($_.FullName) }
}

Get-ChildItem -Path $root -Filter *.ps1 -File -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch $excludeRegex } |
    ForEach-Object { $scriptFiles.Add($_.FullName) }

$scriptFiles = $scriptFiles | Select-Object -Unique

Write-Host ""
Write-Host "  GC-AUDIT FORMAT CHECK (provider-based, parse-only) - validate-format.ps1" -ForegroundColor White
Write-Host "  Root: $root" -ForegroundColor DarkGray
Write-Host "  Active provider(s): $($activeProviders.Id -join ', ')" -ForegroundColor DarkGray
Write-Host ""

if ($scriptFiles.Count -eq 0) {
    Write-Host "  [WARN] No .ps1 files found to check." -ForegroundColor DarkYellow
    Write-Host ""
    exit 0
}

$failures = [System.Collections.Generic.List[string]]::new()

foreach ($file in $scriptFiles) {
    $rel = $file.Replace($root + '\', '').Replace($root + '/', '')
    $tokens = $null
    $parseErrors = $null
    try {
        [void][System.Management.Automation.Language.Parser]::ParseFile($file, [ref]$tokens, [ref]$parseErrors)
    } catch {
        $failures.Add("$rel - parser threw: $($_.Exception.Message)")
        continue
    }

    if ($parseErrors -and $parseErrors.Count -gt 0) {
        foreach ($err in $parseErrors) {
            $failures.Add("${rel}:$($err.Extent.StartLineNumber) - $($err.Message)")
        }
    } else {
        Write-Host "  [PASS] $rel" -ForegroundColor DarkGreen
    }
}

Write-Host ""

if ($failures.Count -eq 0) {
    Write-Host "  [PASS] $($scriptFiles.Count) script(s) parse cleanly." -ForegroundColor Green
    Write-Host ""
    exit 0
}

foreach ($f in $failures) {
    Write-Host "  [ERROR] $f" -ForegroundColor Red
}
Write-Host ""
Write-Host "  [FAIL] $($failures.Count) parse error(s) across $($scriptFiles.Count) script(s)." -ForegroundColor Red
Write-Host ""
exit 1
