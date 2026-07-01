# validate-debt.ps1
# Lightweight structural debt scan for tracked repo files.
#
# Usage:
#   pwsh -File validate-debt.ps1 [-TargetPath C:\work] [-IncludeDocs]
#   pwsh -File validate-debt.ps1 -TargetPath C:\work -Portfolio [-IncludeDocs]

param(
    [string]$TargetPath = ".",
    [switch]$IncludeDocs,
    [switch]$Portfolio,
    [string]$OutputJson
)

$generatedPatterns = @(
    '(^|/)(__pycache__|\.pytest_cache|node_modules|dist|build|coverage)(/|$)',
    '\.py[cod]$',
    '\.egg-info/',
    '(^|/)parser_debug.*\.txt$',
    '(^|/)enforcement_debug\.yaml$',
    '(^|/)null$'
)

$markerPattern = '(?i)\b(shim|compatibility shim|legacy shim|polyfill|deprecated|workaround|backcompat)\b'
$markerSkipPattern = '(^|/)(validate-debt\.ps1|package-lock\.json|pnpm-lock\.yaml|yarn\.lock)$'
$markerAllowedPathPatterns = @(
    '(^|/)CHANGELOG\.md$',
    '(^|/)schemas/',
    '(^|/)public/',
    '(^|/)content/',
    '(^|/)sources/',
    '(^|/)governance/(extension-registry|metadata-schema)\.yaml$',
    '^agent-dossier\.yaml$',
    '^agent-matrix\.yaml$',
    '^examples/mcp-enabled-matrix\.yaml$',
    '^models/dossier\.py$',
    '^ons\.yaml$',
    '^tools/(rules\.json|validate\.py)$',
    '^tests/test_validate\.py$',
    '^src/eco/micropython/(run|time_loc)\.py$',
    '^docs/debt-classification\.md$',
    '^GAP_ANALYSIS_ECORUNTIME\.md$',
    '^docs/architecture/mid-series/0061/legacy\.shims/',
    '^docs/governance/eco_documentation_standard\.md$',
    '^docs/specifications/(cockpit-ui-spec|devxtoolkit-ui-config-spec|ons-v1\.1)\.md$',
    '^spec/canon/canon\.metadata\.md$',
    '^governance/(soc2-mapping|zero-trust)\.yaml$',
    '^profiles/structural-debt-health/(README\.md|profile\.yml)$',
    '^registry/clusters\.yaml$'
)
$markerAllowedLinePatterns = @(
    'Debt validator',
    'validate-debt.*scans',
    'validate-debt\.ps1',
    'free of generated artifacts and legacy shim markers',
    'Generated artifacts and shim debt markers',
    'enum.*deprecated',
    'deprecated_since',
    'rule-catalog-deprecated',
    'rule-deprecated-since-invalid',
    'x-deprecated',
    'http-sse deprecated',
    'http-sse.*Deprecated',
    'deprecated.*sunset',
    'transport_config',
    '✅',
    'no longer tracked',
    'historical lineage',
    'status: canonical \| provisional \| deprecated \| legacy',
    'Spec status labels',
    'status lifecycle planned.*ready.*deprecated'
)

function Resolve-TargetRoot([string]$Path) {
    if (-not (Test-Path $Path)) {
        Write-Host "Target path does not exist: $Path" -ForegroundColor Red
        exit 1
    }

    return $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
}

function Get-RegisteredProjects([string]$RootPath) {
    $projectsFile = Join-Path $RootPath "projects.yaml"
    if (-not (Test-Path $projectsFile)) {
        Write-Host "Portfolio mode requires projects.yaml under: $RootPath" -ForegroundColor Red
        exit 1
    }

    $projects = @()
    $current = $null
    foreach ($line in Get-Content $projectsFile) {
        if ($line -match '^\s{2}- name:\s*(.+?)\s*$') {
            if ($current) { $projects += [pscustomobject]$current }
            $current = @{
                Name = $Matches[1].Trim(' "')
                Path = $null
                Status = $null
                Group = $null
            }
            continue
        }

        if (-not $current) { continue }

        if ($line -match '^\s{4}path:\s*(.+?)\s*$') {
            $current.Path = $Matches[1].Trim(' "')
        } elseif ($line -match '^\s{4}status:\s*(.+?)\s*$') {
            $current.Status = $Matches[1].Trim(' "')
        } elseif ($line -match '^\s{4}group:\s*(.+?)\s*$') {
            $current.Group = $Matches[1].Trim(' "')
        }
    }

    if ($current) { $projects += [pscustomobject]$current }
    return $projects
}

function Invoke-RepoDebtScan([string]$RepoPath, [string]$Label) {
    $gitTop = git -C $RepoPath rev-parse --show-toplevel 2>$null
    if (-not $gitTop) {
        return [pscustomobject]@{
            Label = $Label
            Checked = 0
            Failures = @("Not a git repo: $RepoPath")
            Warnings = @()
        }
    }

    $tracked = git -C $RepoPath ls-files
    $failures = @()
    $warnings = @()

    foreach ($path in $tracked) {
        foreach ($pattern in $generatedPatterns) {
            if ($path -match $pattern) {
                $failures += "${Label}: tracked generated/debug artifact: $path"
                break
            }
        }
    }

    $scanPaths = $tracked | Where-Object {
        $_ -match '\.(ps1|py|js|ts|tsx|jsx|mjs|cjs|json|yaml|yml|toml)$'
    }

    if ($IncludeDocs) {
        $scanPaths += ($tracked | Where-Object { $_ -match '\.(md|mdx|txt)$' })
        $scanPaths = $scanPaths | Select-Object -Unique
    }

    foreach ($path in $scanPaths) {
        $full = Join-Path $gitTop $path
        if (-not (Test-Path $full)) { continue }

        $lineNo = 0
        foreach ($line in Get-Content $full) {
            $lineNo++
            if ($line -notmatch $markerPattern) { continue }

            $normalized = $path -replace '\\', '/'
            if ($normalized -match $markerSkipPattern) {
                continue
            }

            if ($normalized -match '(^|/)(archive|docs/archive|docs/sources|passes|passchangelog)(/|$)') {
                continue
            }

            $allowed = $false
            foreach ($pattern in $markerAllowedPathPatterns) {
                if ($normalized -match $pattern) {
                    $allowed = $true
                    break
                }
            }

            if (-not $allowed) {
                foreach ($pattern in $markerAllowedLinePatterns) {
                    if ($line -match $pattern) {
                        $allowed = $true
                        break
                    }
                }
            }

            if ($allowed) {
                continue
            }

            $warnings += "${Label}: ${path}:${lineNo}: debt marker: $($line.Trim())"
        }
    }

    return [pscustomobject]@{
        Label = $Label
        Checked = $tracked.Count
        Failures = $failures
        Warnings = $warnings
    }
}

$root = Resolve-TargetRoot $TargetPath
$results = @()

if ($Portfolio) {
    $projects = Get-RegisteredProjects $root
    $scanProjects = $projects | Where-Object {
        $_.Path -and
        $_.Status -ne "archive" -and
        $_.Group -ne "archive" -and
        $_.Group -ne "vendor" -and
        $_.Path -notmatch '(^|/)(tools|_archive)(/|$)'
    }

    foreach ($project in $scanProjects) {
        $repoPath = Join-Path $root $project.Path
        if (-not (Test-Path $repoPath)) {
            $results += [pscustomobject]@{
                Label = $project.Name
                Checked = 0
                Failures = @("Registered path missing: $($project.Path)")
                Warnings = @()
            }
            continue
        }

        $gitTop = git -C $repoPath rev-parse --show-toplevel 2>$null
        if (-not $gitTop) { continue }

        $results += Invoke-RepoDebtScan $repoPath $project.Name
    }
} else {
    $gitTop = git -C $root rev-parse --show-toplevel 2>$null
    if (-not $gitTop) {
        Write-Host "Target path is not inside a git repo: $root" -ForegroundColor Red
        exit 1
    }

    $results += Invoke-RepoDebtScan $root "."
}

$failures = @($results | ForEach-Object { $_.Failures })
$warnings = @($results | ForEach-Object { $_.Warnings })
$checkedCount = ($results | Measure-Object -Property Checked -Sum).Sum
$status = if ($failures.Count -gt 0) {
    "fail"
} elseif ($warnings.Count -gt 0) {
    "warn"
} else {
    "pass"
}

$report = [pscustomobject]@{
    profile = "gc.profile.structural-debt-health"
    profile_version = "0.1.0"
    status = $status
    target_path = $root
    portfolio = [bool]$Portfolio
    include_docs = [bool]$IncludeDocs
    checked_repos = $results.Count
    checked_files = [int]$checkedCount
    failure_count = $failures.Count
    warning_count = $warnings.Count
    failures = @($failures)
    warnings = @($warnings)
    generated_artifact_policy = "fail"
    marker_policy = "warn"
}

if ($OutputJson) {
    $outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputJson)
    $outputParent = Split-Path -Parent $outputPath
    if ($outputParent -and -not (Test-Path $outputParent)) {
        New-Item -ItemType Directory -Path $outputParent -Force | Out-Null
    }
    $report | ConvertTo-Json -Depth 6 | Set-Content -Path $outputPath -Encoding UTF8
}

if ($failures.Count -gt 0) {
    Write-Host ""
    Write-Host "Debt validation failed:" -ForegroundColor Red
    $failures | ForEach-Object { Write-Host "  FAIL  $_" -ForegroundColor Yellow }
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Warnings:" -ForegroundColor DarkYellow
        $warnings | Select-Object -First 50 | ForEach-Object { Write-Host "  WARN  $_" -ForegroundColor DarkYellow }
        if ($warnings.Count -gt 50) {
            Write-Host "  WARN  ... $($warnings.Count - 50) more warnings omitted" -ForegroundColor DarkYellow
        }
    }
    Write-Host ""
    exit 1
}

Write-Host "Debt validation passed." -ForegroundColor Green
if ($Portfolio) {
    Write-Host "  registered repos checked: $($results.Count)" -ForegroundColor DarkGray
}
Write-Host "  tracked files checked: $checkedCount" -ForegroundColor DarkGray
if ($warnings.Count -gt 0) {
    Write-Host "  warnings: $($warnings.Count)" -ForegroundColor DarkYellow
    $warnings | Select-Object -First 50 | ForEach-Object { Write-Host "  WARN  $_" -ForegroundColor DarkYellow }
    if ($warnings.Count -gt 50) {
        Write-Host "  WARN  ... $($warnings.Count - 50) more warnings omitted" -ForegroundColor DarkYellow
    }
}
