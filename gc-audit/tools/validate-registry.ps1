<#
.SYNOPSIS
    Validate GC-AUDIT registry profiles.

.DESCRIPTION
    Validates registry truth for GC, DCP, and DXP profiles.

    Profile gc validates CANON registry files under passes/.
    Profile dcp delegates projects.yaml pointer truth to validate-pointers.ps1.
    Profile dxp fails closed until the DXP/Marlin registry schema is defined.

.PARAMETER Profile
    Registry profile to validate: gc, dcp, or dxp.

.PARAMETER TargetPath
    Registry root path. For gc, this is the governance-commons repo root.
    For dcp, this is the DCP/portfolio root.

.PARAMETER PortfolioRoot
    Optional containment root for cross-repo registry paths. Defaults to the
    parent of TargetPath for gc and to TargetPath for dcp.

.PARAMETER ResolveExternal
    Resolve cross-namespace dependencies through external_registries entries.

.PARAMETER Strict
    Treat warnings as failures.
#>
param(
    [ValidateSet("gc", "dcp", "dxp")]
    [string] $Profile = "gc",
    [string] $TargetPath = ".",
    [string] $PortfolioRoot,
    [switch] $ResolveExternal,
    [switch] $Strict,
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$ContainmentRoot = $null
if ($PortfolioRoot) {
    $ContainmentRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PortfolioRoot)
} elseif ($Profile -eq "dcp") {
    $ContainmentRoot = $Root
} else {
    $ContainmentRoot = Split-Path -Parent $Root
}
$Errors = 0
$Warnings = 0

function Write-Finding([string]$level, [string]$path, [string]$message) {
    $display = $path
    if ($path) {
        $display = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    }
    if (-not $display) { $display = "." }
    $color = "DarkGray"
    if ($level -eq "PASS") { $color = "DarkGreen" }
    if ($level -eq "WARN") { $color = "DarkYellow" }
    if ($level -eq "ERROR") { $color = "Red" }
    Write-Host "  [$level]" -NoNewline -ForegroundColor $color
    Write-Host " $display" -NoNewline -ForegroundColor White
    Write-Host " - $message" -ForegroundColor $color
    if ($level -eq "ERROR") { $script:Errors++ }
    if ($level -eq "WARN") { $script:Warnings++ }
}

function Get-TextOrEmpty([string]$path) {
    if (-not (Test-Path $path)) { return "" }
    return Get-Content -Raw -Encoding UTF8 $path
}

function Resolve-RelativePathWithin([string]$basePath, [string]$candidate, [string]$containmentRoot, [string]$label) {
    if ([string]::IsNullOrWhiteSpace($candidate)) {
        Write-Finding "ERROR" "." "$label path is empty"
        return $null
    }
    if ($candidate -match "^[A-Za-z][A-Za-z0-9+.-]*://") {
        Write-Finding "ERROR" $candidate "$label must be a local relative path; network registry resolution is not allowed"
        return $null
    }
    if ([System.IO.Path]::IsPathRooted($candidate)) {
        Write-Finding "ERROR" $candidate "$label must be relative, not absolute"
        return $null
    }

    $resolved = [System.IO.Path]::GetFullPath((Join-Path $basePath $candidate))
    $contained = [System.IO.Path]::GetFullPath($containmentRoot)
    $separator = [System.IO.Path]::DirectorySeparatorChar
    $containedPrefix = $contained
    if (-not $containedPrefix.EndsWith($separator)) {
        $containedPrefix = $containedPrefix + $separator
    }

    if (($resolved -ne $contained) -and (-not $resolved.StartsWith($containedPrefix, [System.StringComparison]::OrdinalIgnoreCase))) {
        Write-Finding "ERROR" $candidate "$label escapes allowed root '$contained'"
        return $null
    }
    return $resolved
}

function Get-YamlScalar([string]$text, [string]$key) {
    $match = [regex]::Match($text, "(?m)^$([regex]::Escape($key)):\s+(.+?)\s*$")
    if (-not $match.Success) { return "" }
    return $match.Groups[1].Value.Trim().Trim('"')
}

function Get-LayerNames([string]$text) {
    $names = @()
    foreach ($match in [regex]::Matches($text, "(?m)^\s+name:\s+(.+?)\s*$")) {
        $names += $match.Groups[1].Value.Trim().Trim('"')
    }
    return $names
}

function Get-HeaderValue([string]$text, [string]$label) {
    $pattern = "(?m)^\*\*$([regex]::Escape($label)):\*\*\s*(.+?)\s*$"
    $match = [regex]::Match($text, $pattern)
    if (-not $match.Success) { return "" }
    return $match.Groups[1].Value.Trim()
}

function Normalize-Status([string]$status) {
    return $status.Trim().ToLowerInvariant()
}

function Extract-DependsIds([string]$dependsHeader) {
    if (-not $dependsHeader) { return @() }
    $ids = @()
    foreach ($match in [regex]::Matches($dependsHeader, "(GC|ECO):\d{4}")) {
        $ids += $match.Value
    }
    return $ids | Select-Object -Unique
}

function Validate-DcpRegistry {
    $scriptPath = Resolve-RelativePathWithin $PSScriptRoot "validate-pointers.ps1" $PSScriptRoot "delegated validator"
    if (-not $scriptPath) { return }
    if (-not (Test-Path $scriptPath)) {
        Write-Finding "ERROR" $scriptPath "validate-pointers.ps1 not found"
        return
    }
    & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath -TargetPath $Root
    if ($LASTEXITCODE -ne 0) {
        Write-Finding "ERROR" "projects.yaml" "DCP projects.yaml pointer validation failed"
    } else {
        Write-Finding "PASS" "projects.yaml" "DCP projects.yaml pointer validation passed"
    }
}

function Validate-DxpRegistry {
    Write-Finding "ERROR" "." "DXP registry profile is planned but blocked: DXP/Marlin package registry schema is not defined"
}

function Validate-GcRegistry {
    $registryPath = Join-Path $Root "passes\passes.registry.json"
    $changelogPath = Join-Path $Root "passes\passes.registry.changelog.jsonl"
    $namespacePath = Join-Path $Root "passes\namespace.yaml"
    $layersPath = Join-Path $Root "passes\layers.yaml"

    foreach ($required in @($registryPath, $changelogPath, $namespacePath, $layersPath)) {
        if (-not (Test-Path $required)) {
            Write-Finding "ERROR" $required "required GC registry file missing"
        }
    }
    if ($Errors -gt 0) { return }

    try {
        $registry = Get-Content -Raw -Encoding UTF8 $registryPath | ConvertFrom-Json
        Write-Finding "PASS" $registryPath "registry JSON parses"
    } catch {
        Write-Finding "ERROR" $registryPath "registry JSON failed to parse: $($_.Exception.Message)"
        return
    }

    $namespaceText = Get-TextOrEmpty $namespacePath
    $layersText = Get-TextOrEmpty $layersPath
    $namespacePrefix = Get-YamlScalar $namespaceText "prefix"
    $layerNames = @(Get-LayerNames $layersText)

    if ($registry.namespace -ne $namespacePrefix) {
        Write-Finding "ERROR" $registryPath "registry namespace '$($registry.namespace)' does not match namespace.yaml prefix '$namespacePrefix'"
    } else {
        Write-Finding "PASS" $registryPath "registry namespace matches namespace.yaml"
    }

    $entries = @($registry.entries)
    $entriesById = @{}
    $entriesByAlias = @{}
    foreach ($entry in $entries) {
        if ($entriesById.ContainsKey($entry.id)) {
            Write-Finding "ERROR" $registryPath "duplicate registry id: $($entry.id)"
        } else {
            $entriesById[$entry.id] = $entry
        }
        if ($entriesByAlias.ContainsKey($entry.alias)) {
            Write-Finding "ERROR" $registryPath "duplicate registry alias: $($entry.alias)"
        } else {
            $entriesByAlias[$entry.alias] = $entry
        }
        if ($entry.id -notmatch "^$([regex]::Escape($namespacePrefix)):\d{4}$") {
            Write-Finding "ERROR" $registryPath "entry id '$($entry.id)' does not match namespace '$namespacePrefix'"
        }
        if ($entry.layer -notin $layerNames) {
            Write-Finding "ERROR" $registryPath "entry '$($entry.id)' uses unknown layer '$($entry.layer)'"
        }
        if ($entry.path) {
            $entryPath = Resolve-RelativePathWithin $Root $entry.path $ContainmentRoot "registry entry path for $($entry.id)"
            if (-not $entryPath) { continue }
            if (-not (Test-Path $entryPath)) {
                Write-Finding "ERROR" $entry.path "registry path for $($entry.id) does not resolve"
            }
        }
    }

    $passFiles = Get-ChildItem -Path (Join-Path $Root "passes") -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue
    foreach ($file in $passFiles) {
        $text = Get-TextOrEmpty $file.FullName
        $canonicalId = Get-HeaderValue $text "Canonical ID"
        if (-not $canonicalId) { continue }

        if (-not $entriesById.ContainsKey($canonicalId)) {
            Write-Finding "ERROR" $file.FullName "PASS file declares Canonical ID '$canonicalId' but registry has no entry"
            continue
        }

        $entry = $entriesById[$canonicalId]
        $passId = Get-HeaderValue $text "PASS ID"
        $cluster = Get-HeaderValue $text "Cluster"
        $status = Get-HeaderValue $text "Status"
        $timestamp = Get-HeaderValue $text "Timestamp"
        $dependsHeader = Get-HeaderValue $text "Depends on"
        $dependsIds = @(Extract-DependsIds $dependsHeader)
        $registryDepends = @($entry.depends_on)

        if ($passId -and $entry.alias -ne $passId) {
            Write-Finding "ERROR" $file.FullName "PASS ID '$passId' does not match registry alias '$($entry.alias)'"
        }
        if ($cluster -and $entry.cluster -ne $cluster) {
            Write-Finding "ERROR" $file.FullName "Cluster '$cluster' does not match registry cluster '$($entry.cluster)'"
        }
        if ($status -and (Normalize-Status $status) -ne $entry.status) {
            Write-Finding "ERROR" $file.FullName "Status '$status' does not match registry status '$($entry.status)'"
        }
        if ($timestamp -and $entry.timestamp -ne $timestamp) {
            Write-Finding "ERROR" $file.FullName "Timestamp '$timestamp' does not match registry timestamp '$($entry.timestamp)'"
        }
        foreach ($dep in $dependsIds) {
            if ($dep -notin $registryDepends) {
                Write-Finding "ERROR" $file.FullName "Depends on '$dep' missing from registry depends_on for $canonicalId"
            }
        }
    }

    foreach ($entry in $entries) {
        foreach ($dep in @($entry.depends_on)) {
            if ($dep -match "^$([regex]::Escape($namespacePrefix)):" -and -not $entriesById.ContainsKey($dep)) {
                Write-Finding "ERROR" $registryPath "entry '$($entry.id)' depends on missing local id '$dep'"
            } elseif ($dep -notmatch "^$([regex]::Escape($namespacePrefix)):") {
                if ($ResolveExternal) {
                    Resolve-ExternalDependency $registry $dep
                } else {
                    Write-Finding "WARN" $registryPath "entry '$($entry.id)' has external dependency '$dep' not resolved without -ResolveExternal"
                }
            }
        }
    }

    $changelogIds = @{}
    $lineNumber = 0
    foreach ($line in Get-Content -Encoding UTF8 $changelogPath) {
        $lineNumber++
        if (-not $line.Trim()) { continue }
        try {
            $row = $line | ConvertFrom-Json
            if ($row.id) { $changelogIds[$row.id] = $true }
        } catch {
            Write-Finding "ERROR" $changelogPath "changelog JSONL parse failed on line ${lineNumber}: $($_.Exception.Message)"
        }
    }
    if ($Errors -eq 0) {
        Write-Finding "PASS" $changelogPath "registry changelog JSONL parses"
    }
    foreach ($entry in $entries) {
        if (-not $changelogIds.ContainsKey($entry.id)) {
            Write-Finding "ERROR" $changelogPath "no registry changelog row found for $($entry.id)"
        }
    }

    if ($Errors -eq 0) {
        Write-Finding "PASS" $registryPath "GC registry profile validation passed"
    }
}

function Resolve-ExternalDependency($registry, [string]$dependencyId) {
    $namespace = ($dependencyId -split ":", 2)[0]
    $external = @($registry.meta.external_registries) | Where-Object { $_.namespace -eq $namespace } | Select-Object -First 1
    if (-not $external) {
        Write-Finding "ERROR" "passes/passes.registry.json" "no external registry configured for dependency '$dependencyId'"
        return
    }
    $externalPath = Resolve-RelativePathWithin $Root $external.registry_url $ContainmentRoot "external registry for '$namespace'"
    if (-not $externalPath) { return }
    if (-not (Test-Path $externalPath)) {
        Write-Finding "ERROR" $external.registry_url "external registry for '$namespace' does not resolve"
        return
    }
    try {
        $externalRegistry = Get-Content -Raw -Encoding UTF8 $externalPath | ConvertFrom-Json
    } catch {
        Write-Finding "ERROR" $external.registry_url "external registry failed to parse: $($_.Exception.Message)"
        return
    }
    $found = @($externalRegistry.entries) | Where-Object { $_.id -eq $dependencyId } | Select-Object -First 1
    if (-not $found) {
        Write-Finding "ERROR" $external.registry_url "external dependency '$dependencyId' not found"
    }
}

Write-Host ""
Write-Host "  GC-AUDIT REGISTRY VALIDATION - validate-registry.ps1" -ForegroundColor White
Write-Host "  Profile: $Profile  Root: $Root" -ForegroundColor DarkGray
Write-Host "  Containment root: $ContainmentRoot" -ForegroundColor DarkGray
Write-Host ""

if ($Profile -eq "gc") { Validate-GcRegistry }
if ($Profile -eq "dcp") { Validate-DcpRegistry }
if ($Profile -eq "dxp") { Validate-DxpRegistry }

Write-Host ""
if ($Errors -eq 0 -and $Warnings -eq 0) {
    Write-Host "  -- registry profile '$Profile' passed --" -ForegroundColor Green
} elseif ($Errors -eq 0) {
    Write-Host "  -- registry profile '$Profile' passed with $Warnings warnings --" -ForegroundColor DarkYellow
} else {
    Write-Host "  -- registry profile '$Profile' failed with $Errors errors and $Warnings warnings --" -ForegroundColor Red
}
Write-Host ""

if ($Strict -and ($Errors -gt 0 -or $Warnings -gt 0)) { exit 1 }
if ($Errors -gt 0) { exit 1 }
exit 0
