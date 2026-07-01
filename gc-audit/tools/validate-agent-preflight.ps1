<#
.SYNOPSIS
    Validates that a session note or first response contains a GC preflight stamp.

.DESCRIPTION
    Fails (exit code 1) when the required PREFLIGHT stamp is missing or malformed.
    Default mode validates the first non-empty line (first-response check).
    Session mode validates that at least one valid stamp appears anywhere in the file.

    The expected order token is read from AGENT-PREFLIGHT.md (the canonical source).
    When DEV-ACCORD.03 changes the agent-trail, update AGENT-PREFLIGHT.md only —
    this script updates automatically.

.PARAMETER FilePath
    Path to a session note or first-response file to validate.

.PARAMETER Text
    Raw text to validate inline (alternative to FilePath).

.PARAMETER Mode
    FirstResponse (default) — validates the first non-empty line.
    Session — validates that at least one stamp appears in the search window.

.PARAMETER SearchWindow
    Number of lines to inspect (default: 40).

.PARAMETER SpecPath
    Path to AGENT-PREFLIGHT.md. Defaults to the sibling directory of this script.
#>
param(
    [Parameter(ParameterSetName = 'File', Mandatory = $true)]
    [string]$FilePath,

    [Parameter(ParameterSetName = 'Text', Mandatory = $true)]
    [string]$Text,

    [ValidateSet('FirstResponse', 'Session')]
    [string]$Mode = 'FirstResponse',

    [int]$SearchWindow = 40,

    [string]$SpecPath = "",

    [switch]$Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

Set-StrictMode -Version Latest

# ── Locate AGENT-PREFLIGHT.md ─────────────────────────────────────────────────

if (-not $SpecPath) {
    $SpecPath = Join-Path (Split-Path $PSScriptRoot -Parent) "AGENT-PREFLIGHT.md"
}

if (-not (Test-Path -LiteralPath $SpecPath)) {
    Write-Host "FAIL: AGENT-PREFLIGHT.md not found at: $SpecPath" -ForegroundColor Red
    Write-Host "      Pass -SpecPath to specify its location." -ForegroundColor DarkGray
    exit 1
}

# ── Read canonical order token from spec ─────────────────────────────────────

$orderToken = $null
try {
    $specLines = Get-Content -LiteralPath $SpecPath -ErrorAction Stop
    $tokenLine = $specLines | Where-Object { $_ -match '^order-token:\s+(.+)$' } | Select-Object -First 1
    if ($tokenLine -match '^order-token:\s+(.+)$') {
        $orderToken = $Matches[1].Trim()
    }
} catch {
    Write-Host "FAIL: Could not read AGENT-PREFLIGHT.md — $_" -ForegroundColor Red
    exit 1
}

if (-not $orderToken) {
    Write-Host "FAIL: No 'order-token:' line found in AGENT-PREFLIGHT.md." -ForegroundColor Red
    Write-Host "      Add: order-token: AGENTS>03>..." -ForegroundColor DarkGray
    exit 1
}

$escapedOrder   = [regex]::Escape($orderToken)
$completePattern = "^PREFLIGHT:\s*complete\s*\|\s*project=.+\|\s*order=$escapedOrder\s*$"
$blockedPattern  = '^PREFLIGHT:\s*blocked\s*\|\s*missing=.+\|\s*action=read missing files first\s*$'

# ── Read input ────────────────────────────────────────────────────────────────

$lines = $null
try {
    if ($PSCmdlet.ParameterSetName -eq 'File') {
        if (-not (Test-Path -LiteralPath $FilePath)) {
            Write-Host "FAIL: File not found: $FilePath" -ForegroundColor Red
            exit 1
        }
        $lines = Get-Content -LiteralPath $FilePath -ErrorAction Stop
    } else {
        $lines = $Text -split "`r?`n"
    }
} catch {
    Write-Host "FAIL: Could not read input — $_" -ForegroundColor Red
    exit 1
}

if ($SearchWindow -lt 1) {
    Write-Host "FAIL: SearchWindow must be >= 1." -ForegroundColor Red
    exit 1
}

$windowLines = $lines | Select-Object -First $SearchWindow

# ── Validate ──────────────────────────────────────────────────────────────────

if ($Mode -eq 'FirstResponse') {
    $firstNonEmpty = $windowLines | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -First 1

    if (-not $firstNonEmpty) {
        Write-Host 'FAIL: No non-empty content found in the search window.' -ForegroundColor Red
        exit 1
    }

    if (($firstNonEmpty -match $completePattern) -or ($firstNonEmpty -match $blockedPattern)) {
        Write-Host 'PASS: First response line contains a valid PREFLIGHT stamp.' -ForegroundColor Green
        exit 0
    }

    Write-Host "FAIL: First non-empty line is not a valid PREFLIGHT stamp." -ForegroundColor Red
    Write-Host "      Got:      $firstNonEmpty" -ForegroundColor DarkGray
    Write-Host "      Expected: PREFLIGHT: complete | project=<path> | order=$orderToken" -ForegroundColor DarkGray
    exit 1
}

$matched = $windowLines | Where-Object {
    ($_ -match $completePattern) -or ($_ -match $blockedPattern)
} | Select-Object -First 1

if ($matched) {
    Write-Host 'PASS: Session contains a valid PREFLIGHT stamp.' -ForegroundColor Green
    exit 0
}

Write-Host "FAIL: No valid PREFLIGHT stamp found in the first $SearchWindow lines." -ForegroundColor Red
Write-Host "      Expected: PREFLIGHT: complete | project=<path> | order=$orderToken" -ForegroundColor DarkGray
exit 1
