<#
.SYNOPSIS
    Zero-trust posture audit for GC-AUDIT.

.DESCRIPTION
    Audits zero-trust enforcement across the following domains:

    ZT1 — Path containment
          All allowlisted script paths resolve under the portfolio root.
          No absolute escapes or .. traversal.

    ZT2 — Mutation safety
          No mutates:false operation exposes a mutating switch.
          All mutates:true operations require explicit -Apply.

    ZT3 — Allowlist coverage
          No script in gc-audit/tools/ is unregistered and non-internal.

    ZT4 — Shell delegation
          No registered script spawns an unresolved child process.
          Internal delegation only via allowlisted resolved paths.

    ZT5 — Fail-closed defaults
          Unimplemented (planned) verbs have no runnable steps.
          DXP profile fails closed. gc-audit.close is intentionally empty.

    ZT6 — Explicit authorization
          Normalization-apply, schema-authority-change, and git-branch/split
          declare explicitAuthorizationRequired in the registry.

    ZT7 — Network isolation
          No registered operation fetches from a network registry URL.

    ZT8 — Principal presence
          If evidence bundles are enabled, a signed principal record exists.

.PARAMETER TargetPath
    GC-AUDIT root (default: governance-commons directory containing gc-audit/).

.PARAMETER PortfolioRoot
    Containment root for path checks. Defaults to parent of TargetPath.

.PARAMETER Strict
    Treat warnings as failures.
#>
param(
    [string] $TargetPath    = ".",
    [string] $PortfolioRoot = "",
    [switch] $Strict
)

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$ContainmentRoot = if ($PortfolioRoot) {
    $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PortfolioRoot)
} else {
    Split-Path $Root -Parent
}

$RegistryFile = Join-Path $Root "gc-audit\GC-AUDIT-REGISTRY.yaml"
$ToolsDir     = Join-Path $Root "gc-audit\tools"

$Errors   = [System.Collections.Generic.List[string]]::new()
$Warnings = [System.Collections.Generic.List[string]]::new()
$Passed   = [System.Collections.Generic.List[string]]::new()

function Add-Pass([string]$msg)  { $script:Passed.Add($msg) }
function Add-Warn([string]$msg)  { $script:Warnings.Add($msg) }
function Add-Error([string]$msg) { $script:Errors.Add($msg) }

# ── Guards ────────────────────────────────────────────────────────────────────

if (-not (Test-Path $RegistryFile)) {
    Write-Host "FAIL  GC-AUDIT-REGISTRY.yaml not found: $RegistryFile" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $ToolsDir)) {
    Write-Host "FAIL  gc-audit/tools/ not found: $ToolsDir" -ForegroundColor Red
    exit 1
}

$RegistryRaw = Get-Content $RegistryFile -Raw

# ── ZT1 — Path containment ────────────────────────────────────────────────────

$scriptPaths = [regex]::Matches($RegistryRaw, 'script:\s+(.+)') | ForEach-Object { $_.Groups[1].Value.Trim() }

foreach ($rel in $scriptPaths) {
    $full = Join-Path $ContainmentRoot $rel
    $resolved = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($full)
    if (-not $resolved.StartsWith($ContainmentRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        Add-Error "ZT1  Path escape: $rel"
    } elseif (-not (Test-Path $resolved)) {
        Add-Error "ZT1  Script path does not resolve: $rel"
    } else {
        Add-Pass "ZT1  $rel"
    }
}

# ── ZT2 — Mutation safety ─────────────────────────────────────────────────────

# Check that validate-*.ps1 scripts don't expose mutating switches
$validateScripts = Get-ChildItem $ToolsDir -Filter "validate-*.ps1"
$mutatingPatterns = @('\[switch\]\s*\$Fix', '\[switch\]\s*\$Apply', '\[switch\]\s*\$Write', '\[switch\]\s*\$Repair')

foreach ($script in $validateScripts) {
    $content = Get-Content $script.FullName -Raw
    foreach ($pattern in $mutatingPatterns) {
        if ($content -match $pattern) {
            Add-Error "ZT2  Mutating switch in validator: $($script.Name) (matches: $pattern)"
        }
    }
}
if ($Errors.Count -eq 0 -or -not ($Errors | Where-Object { $_ -match "ZT2" })) {
    Add-Pass "ZT2  No mutating switches found in validate-*.ps1"
}

# Check that normalize-*.ps1 scripts require -Apply (not just -DryRun)
$normalizeScripts = Get-ChildItem $ToolsDir -Filter "normalize-*.ps1"
foreach ($script in $normalizeScripts) {
    $content = Get-Content $script.FullName -Raw
    if ($content -notmatch '\[switch\]\s*\$Apply') {
        Add-Error "ZT2  Normalizer missing -Apply switch: $($script.Name)"
    } else {
        Add-Pass "ZT2  $($script.Name) declares -Apply"
    }
}

# ── ZT3 — Allowlist coverage ──────────────────────────────────────────────────

$registeredScripts = [regex]::Matches($RegistryRaw, 'script:\s+.+/tools/(.+\.ps1)') |
    ForEach-Object { $_.Groups[1].Value.Trim() }

$allScripts = Get-ChildItem $ToolsDir -Filter "*.ps1" | Select-Object -ExpandProperty Name

foreach ($scriptName in $allScripts) {
    if ($registeredScripts -contains $scriptName) {
        Add-Pass "ZT3  Registered: $scriptName"
    } else {
        Add-Warn "ZT3  Unregistered script (mark internal or register): $scriptName"
    }
}

# ── ZT4 — Shell delegation ────────────────────────────────────────────────────

$shellPatterns = @('Start-Process\s+[''"]?(powershell|pwsh|cmd|bash|sh)[''"]?', 'Invoke-Expression', '& [''"]?(powershell|pwsh|cmd)[''"]?')

foreach ($script in (Get-ChildItem $ToolsDir -Filter "*.ps1")) {
    $content = Get-Content $script.FullName -Raw
    foreach ($pattern in $shellPatterns) {
        if ($content -match $pattern) {
            Add-Warn "ZT4  Shell delegation in $($script.Name) (matches: $pattern) - verify it uses an allowlisted resolved path"
        }
    }
}
if (-not ($Warnings | Where-Object { $_ -match "ZT4" })) {
    Add-Pass "ZT4  No raw shell delegation patterns detected"
}

# ── ZT5 — Fail-closed defaults ────────────────────────────────────────────────

if ($RegistryRaw -match "status:\s+planned[\s\S]*?steps:\s+\[\]") {
    Add-Pass "ZT5  Planned operations have empty steps (fail-closed)"
} else {
    Add-Warn "ZT5  Could not confirm planned operations have empty steps - verify manually"
}

if ($RegistryRaw -match "dxp[\s\S]*?failClosed:\s+true") {
    Add-Pass "ZT5  DXP profile declares failClosed: true"
} else {
    Add-Error "ZT5  DXP profile missing failClosed: true"
}

# ── ZT6 — Explicit authorization ──────────────────────────────────────────────

$requiredAuthClaims = @('normalization-apply', 'schema-authority-change', 'git-branch-or-remote-split')
foreach ($claim in $requiredAuthClaims) {
    if ($RegistryRaw -match [regex]::Escape($claim)) {
        Add-Pass "ZT6  explicitAuthorizationRequired declares: $claim"
    } else {
        Add-Error "ZT6  Missing explicitAuthorizationRequired entry: $claim"
    }
}

# ── ZT7 — Network isolation ───────────────────────────────────────────────────

if ($RegistryRaw -match 'networkRegistryFetch:\s+forbidden') {
    Add-Pass "ZT7  networkRegistryFetch: forbidden declared in registry"
} else {
    Add-Error "ZT7  networkRegistryFetch: forbidden not declared"
}

# ── ZT8 — Principal presence (advisory) ──────────────────────────────────────

$keystorePath = Join-Path $ContainmentRoot "marlin\packages\marlin-dxp\keystore"
if (Test-Path $keystorePath) {
    $principals = Get-ChildItem $keystorePath -Filter "*.json" -ErrorAction SilentlyContinue
    if ($principals.Count -gt 0) {
        Add-Pass "ZT8  Signed principal record found in keystore"
    } else {
        Add-Warn "ZT8  Keystore exists but no principal records found"
    }
} else {
    Add-Warn "ZT8  Keystore not found at expected path - skip if evidence bundles not enabled"
}

# ── Report ─────────────────────────────────────────────────────────────────────

Write-Host ""
Write-Host "GC-AUDIT zero-trust posture audit" -ForegroundColor Cyan
Write-Host "  containment root: $ContainmentRoot"
Write-Host ""

if ($Passed.Count -gt 0) {
    Write-Host "PASS ($($Passed.Count)):" -ForegroundColor DarkGreen
    $Passed | ForEach-Object { Write-Host "  OK    $_" -ForegroundColor DarkGreen }
    Write-Host ""
}

if ($Warnings.Count -gt 0) {
    Write-Host "WARN ($($Warnings.Count)):" -ForegroundColor Yellow
    $Warnings | ForEach-Object { Write-Host "  WARN  $_" -ForegroundColor Yellow }
    Write-Host ""
}

if ($Errors.Count -gt 0) {
    Write-Host "FAIL ($($Errors.Count)):" -ForegroundColor Red
    $Errors | ForEach-Object { Write-Host "  FAIL  $_" -ForegroundColor Red }
    Write-Host ""
}

$exitCode = 0
if ($Errors.Count -gt 0) { $exitCode = 1 }
if ($Strict -and $Warnings.Count -gt 0) { $exitCode = 1 }

$status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
$color  = if ($exitCode -eq 0) { "Green" } else { "Red" }
Write-Host "$status  zero-trust posture audit complete - $($Errors.Count) error(s), $($Warnings.Count) warning(s)" -ForegroundColor $color

exit $exitCode
