<#
.SYNOPSIS
    Validates agent bootstrap conformance against DEV-ACCORD.04 (GC:2012).

.DESCRIPTION
    Checks repository bootstrap files for the DEV-ACCORD.04 separation between
    normative GC requirements and runtime platform behavior.

    ERRORS (exit code 1):
      E1 — AGENTS.md exists but does not point to DEV-ACCORD.03 or AGENTS.md target authority
      E2 — Bootstrap file contains a universal auto-discovery overclaim

    WARNINGS (exit code 0; exit code 1 with -Strict):
      W1 — Repository has DEV-ACCORD planning docs but no AGENTS.md
      W2 — Runtime adapter exists but does not point to AGENTS.md or DEV-ACCORD.03
      W3 — Runtime adapter appears to contain substantial governance doctrine

.PARAMETER Strict
    Treat warnings as errors.

.PARAMETER Project
    Check only a named repository path relative to TargetPath.

.PARAMETER TargetPath
    Portfolio or repository root to scan (default current directory).

.PARAMETER Help
    Show help and exit.
#>
param(
    [switch] $Strict,
    [string] $Project = "",
    [string] $TargetPath = ".",
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$Errors = 0
$Warnings = 0

function Write-Finding([string]$level, [string]$code, [string]$path, [string]$message) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    $color = "DarkYellow"
    if ($level -eq "ERROR") { $color = "Red" }
    Write-Host "  [$level $code]" -NoNewline -ForegroundColor $color
    Write-Host " $rel" -NoNewline -ForegroundColor White
    Write-Host " — $message" -ForegroundColor $color
    if ($level -eq "ERROR") { $script:Errors++ } else { $script:Warnings++ }
}

function Write-Pass([string]$path) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  [PASS     ]" -NoNewline -ForegroundColor DarkGreen
    Write-Host " $rel" -ForegroundColor Gray
}

function Get-Text([string]$path) {
    if (-not (Test-Path $path)) { return "" }
    return Get-Content -Raw -Encoding UTF8 $path
}

function Test-PointsToBootstrapAuthority([string]$text, [switch]$AllowAgentsPointer) {
    $pointsToCanonical = (
        $text -match 'DEV-ACCORD\.03' -or
        $text -match 'passes/dev-accord/DEV-ACCORD\.03\.md' -or
        $text -match 'passes\\dev-accord\\DEV-ACCORD\.03\.md'
    )
    if ($pointsToCanonical) { return $true }
    if (-not $AllowAgentsPointer) { return $false }
    return (
        $text -match '(?i)(read|see|points? to|bootstrap).*AGENTS\.md' -or
        $text -match '(?i)AGENTS\.md.*(read|see|points? to|bootstrap)'
    )
}

function Test-PublicSafeStub([string]$text) {
    # DEV-ACCORD.08 permits public stubs without private onboarding pointers.
    $first = @($text -split '\r?\n' | Where-Object { $_.Trim() })[0]
    return ($first -match '(?i)^#.*public[- ](?:safe[- ])?stub' -and
        $text -match '(?i)\[[^\]]+\]\((?:README|CONTRIBUTING)\.md\)' -and
        $text -match '(?i)private' -and
        $text -match '(?is)ask.{0,80}(?:owner|maintainer).{0,80}(?:context|bootstrap|instruction)')
}

function Test-LocalOnboardingPointer([string]$text, [string]$repoRoot) {
    # DEV-ACCORD.04 names DEV-ACCORD.03 as an example, not the only authority.
    $links = [regex]::Matches($text, '(?im)^Read\s+\[[^\]]+\]\(([^)]+)\)')
    foreach ($link in $links) {
        $relative = $link.Groups[1].Value
        if ([IO.Path]::IsPathRooted($relative) -or $relative -match '^[a-z]+:') { continue }
        $candidate = [IO.Path]::GetFullPath((Join-Path $repoRoot $relative))
        $boundary = [IO.Path]::GetFullPath($repoRoot).TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
        if ($candidate.StartsWith($boundary, [StringComparison]::OrdinalIgnoreCase) -and
            (Test-Path -LiteralPath $candidate -PathType Leaf) -and
            $relative -match '(?i)(agent[-_]guidance|onboarding|instructions|CONTRIBUTING\.md)') { return $true }
    }
    return $false
}

function Test-UniversalAutoReadClaim([string]$text) {
    $patterns = @(
        '(?i)all agents .*auto(?:matically)?[- ]?read',
        '(?i)every agent .*auto(?:matically)?[- ]?read',
        '(?i)all agent platforms .*auto(?:matically)?[- ]?read',
        '(?i)everyone else reads this automatically',
        '(?i)ChatGPT.*auto(?:matically)?[- ]?read',
        '(?i)Copilot.*auto(?:matically)?[- ]?read',
        '(?i)Gemini.*auto(?:matically)?[- ]?read'
    )
    foreach ($p in $patterns) {
        if ($text -match $p) { return $true }
    }
    return $false
}

function Test-SubstantialDoctrine([string]$text) {
    $lines = @($text -split '\r?\n' | Where-Object { $_.Trim() -ne "" })
    $hasCanonicalSections = $text -match '(?im)^##\s+(Canonical|Read|Workflow|Rules|Non-Negotiable|Definition|Testing|Architecture|Scope)'
    return ($lines.Count -gt 30 -and $hasCanonicalSections)
}

function Test-RepoBootstrap([string]$repoRoot) {
    $agents = Join-Path $repoRoot "AGENTS.md"
    $claude = Join-Path $repoRoot "CLAUDE.md"
    $chatgpt = Join-Path $repoRoot "CHATGPT.md"
    $codex = Join-Path $repoRoot "CODEX.md"
    $copilot = Join-Path $repoRoot ".github\copilot-instructions.md"
    $cursor = Join-Path $repoRoot ".cursorrules"

    $hasPlanning = (Test-Path (Join-Path $repoRoot "DEV-PATH.md")) -or (Test-Path (Join-Path $repoRoot "DEV-PLAN.md"))
    $hasAgents = Test-Path $agents

    if ($hasPlanning -and -not $hasAgents) {
        Write-Finding "WARN" "W1" $repoRoot "planning docs found but no AGENTS.md bootstrap"
    }

    if ($hasAgents) {
        $text = Get-Text $agents
        if (-not ((Test-PointsToBootstrapAuthority $text) -or (Test-PublicSafeStub $text) -or (Test-LocalOnboardingPointer $text $repoRoot))) {
            Write-Finding "ERROR" "E1" $agents "AGENTS.md does not point to AGENTS.md authority or DEV-ACCORD.03"
        }
        if (Test-UniversalAutoReadClaim $text) {
            Write-Finding "ERROR" "E2" $agents "contains universal auto-discovery overclaim"
        }
        if (Test-SubstantialDoctrine $text) {
            Write-Finding "WARN" "W3" $agents "contains substantial governance doctrine; DEV-ACCORD.04 prefers pointer-only bootstrap"
        }
        if ($Errors -eq 0) { Write-Pass $agents }
    }

    foreach ($adapter in @($claude, $chatgpt, $codex, $copilot, $cursor)) {
        if (-not (Test-Path $adapter)) { continue }
        $text = Get-Text $adapter
        if (-not (Test-PointsToBootstrapAuthority $text -AllowAgentsPointer)) {
            Write-Finding "WARN" "W2" $adapter "adapter does not point to AGENTS.md or DEV-ACCORD.03"
        }
        if (Test-UniversalAutoReadClaim $text) {
            Write-Finding "ERROR" "E2" $adapter "contains universal auto-discovery overclaim"
        }
        if (Test-SubstantialDoctrine $text) {
            Write-Finding "WARN" "W3" $adapter "contains substantial governance doctrine; adapter should be thin"
        }
    }
}

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

    # DEV-ACCORD.04 is a repository bootstrap standard. Check repository roots,
    # not every folder that happens to contain a planning doc or template.
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

Write-Host ""
Write-Host "  DEV-ACCORD BOOTSTRAP CHECK — validate-bootstrap.ps1" -ForegroundColor White
Write-Host "  Standard: GC:2012 / DEV-ACCORD.04" -ForegroundColor DarkGray
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  $Root" -ForegroundColor DarkGray
Write-Host ""

foreach ($r in $RepoRoots) {
    Test-RepoBootstrap $r
}

Write-Host ""
if ($Errors -eq 0 -and $Warnings -eq 0) {
    Write-Host "  ── $($RepoRoots.Count) roots checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "all conformant" -NoNewline -ForegroundColor Green
    Write-Host "  │  DEV-ACCORD.04 ──" -ForegroundColor DarkGray
} elseif ($Errors -eq 0) {
    Write-Host "  ── $($RepoRoots.Count) roots checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "0 errors" -NoNewline -ForegroundColor Green
    Write-Host "  $Warnings warnings" -NoNewline -ForegroundColor DarkYellow
    Write-Host "  │  DEV-ACCORD.04 ──" -ForegroundColor DarkGray
} else {
    Write-Host "  ── $($RepoRoots.Count) roots checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "$Errors errors" -NoNewline -ForegroundColor Red
    Write-Host "  $Warnings warnings" -NoNewline -ForegroundColor DarkYellow
    Write-Host "  │  DEV-ACCORD.04 ──" -ForegroundColor DarkGray
}
Write-Host ""

if ($Strict -and ($Errors -gt 0 -or $Warnings -gt 0)) { exit 1 }
if ($Errors -gt 0) { exit 1 }
exit 0
