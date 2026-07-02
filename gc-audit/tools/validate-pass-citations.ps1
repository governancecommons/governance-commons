<#
.SYNOPSIS
    Validates that PASS-shaped citations resolve to a real passes.registry.json entry.

.DESCRIPTION
    Catches the DEV-ACCORD-CI-41 failure mode: a working name that looks like a
    PASS alias (CLUSTER.NN) gets cited in a markdown heading, a "Pass-ID:" line
    inside a doc, or a commit message trailer, without ever being assigned a
    canonical ID or entered in passes/passes.registry.json. validate-registry.ps1
    does not catch this because it only cross-checks .md files that declare their
    own Canonical ID: header - a name used only in prose or a trailer is invisible
    to that check. This validator closes that gap.

    Two modes:
      -Mode Files      Scans only the ADDED lines of the staged diff (git diff
                        --cached -U0) for markdown files, by default, or -Paths
                        for an explicit full-file scan. Checking the diff rather
                        than whole-file content means pre-existing citations are
                        not retroactively flagged every time an unrelated edit
                        touches the same file - only new or changed citation
                        lines are gated. Looks for heading citations in either
                        convention used across the portfolio - trailing
                        parenthetical "## Amendment - ... (DEV-ACCORD.11)"
                        (governance-commons) or leading alias "## CKP.08.04
                        Closure - Title" (cockpit) - and "Pass-ID:" lines. Each
                        captured alias must resolve to passes.registry.json,
                        unless the line also contains the escape phrase "not
                        yet registered" or "working name" (DEV-ACCORD-CI-41
                        permits marking a name as pending registration).
                        GC-PASS-NNNN.NN tokens are never treated as aliases -
                        that format is a passchangelog row index, not a PASS
                        identity (DEV-ACCORD.02).
      -Mode CommitMsg   Reads a commit message file (-MessageFile) and checks any
                        "Pass-ID:" trailer line the same way. "standalone", "N/A",
                        and "none" (case-insensitive) are valid non-citation
                        values per the DEV-ACCORD.06 trailer schema.

    Does not execute file content. Read-only text scanning and JSON parsing only.

.PARAMETER Mode
    Files or CommitMsg. Default: Files.

.PARAMETER Paths
    Explicit list of markdown files to scan (Files mode). Defaults to the
    currently staged *.md files (git diff --cached --name-only --diff-filter=ACM)
    when omitted.

.PARAMETER MessageFile
    Path to a commit message file (CommitMsg mode).

.PARAMETER PortfolioRoot
    Root containing governance-commons/passes/passes.registry.json. Defaults to
    walking up from the current directory looking for governance-commons/.

.PARAMETER Help
    Show help and exit.
#>

param(
    [ValidateSet("Files", "CommitMsg")]
    [string] $Mode = "Files",
    [string[]] $Paths = @(),
    [string] $MessageFile = "",
    [string] $PortfolioRoot = "",
    [switch] $Help
)

if ($Help) {
    Get-Help $PSCommandPath -Full
    exit 0
}

function Write-Line([string]$Text, [string]$Color = "Gray") {
    Write-Host $Text -ForegroundColor $Color
}

# Locate passes.registry.json: prefer -PortfolioRoot, else walk up from CWD.
function Resolve-RegistryPath([string]$Root) {
    if ($Root) {
        $candidate = Join-Path $Root "governance-commons\passes\passes.registry.json"
        if (Test-Path $candidate) { return $candidate }
        $candidate = Join-Path $Root "passes\passes.registry.json"
        if (Test-Path $candidate) { return $candidate }
    }
    $dir = Get-Location
    for ($i = 0; $i -lt 6; $i++) {
        $candidate = Join-Path $dir "governance-commons\passes\passes.registry.json"
        if (Test-Path $candidate) { return $candidate }
        $candidate = Join-Path $dir "passes\passes.registry.json"
        if (Test-Path $candidate) { return $candidate }
        $parent = Split-Path $dir -Parent
        if (-not $parent -or $parent -eq $dir) { break }
        $dir = $parent
    }
    return $null
}

$registryPath = Resolve-RegistryPath $PortfolioRoot
if (-not $registryPath) {
    Write-Line "  [ERROR] Could not locate passes.registry.json under this tree or any parent." "Red"
    exit 1
}

try {
    $registry = Get-Content -Raw -Encoding UTF8 $registryPath | ConvertFrom-Json
} catch {
    Write-Line "  [ERROR] Failed to parse ${registryPath}: $($_.Exception.Message)" "Red"
    exit 1
}

$validAliases = @{}
foreach ($entry in $registry.entries) {
    if ($entry.alias) { $validAliases[$entry.alias] = $true }
}

# Values that are valid trailer content but are not PASS citations.
$exemptValues = @("standalone", "n/a", "none", "")

$errors = New-Object System.Collections.ArrayList
$checked = 0

# GC-PASS-NNNN.NN is a passchangelog row index, never a PASS alias (DEV-ACCORD.02).
# Template placeholders in schema-example lines (e.g. "<PASS ID - required when...>")
# are not citations either.
function Test-NotACitationShape([string]$Alias) {
    if ($Alias -match '^GC-PASS-\d+\.\d+$') { return $true }
    if ($Alias.StartsWith('<')) { return $true }
    return $false
}

function Test-Citation([string]$Alias, [string]$Line, [string]$Source) {
    if ($exemptValues -contains $Alias.ToLowerInvariant()) { return }
    if (Test-NotACitationShape $Alias) { return }
    if ($Line -match "(?i)not yet registered|working name") { return }
    if (-not $validAliases.ContainsKey($Alias)) {
        [void]$errors.Add("$Source cites '$Alias' but no entry with that alias exists in passes.registry.json (mark it 'working name, not yet registered' if intentional, or register it first)")
    }
}

# Two heading conventions are recognized across the portfolio:
# - trailing parenthetical, e.g. "## Amendment - ... (DEV-ACCORD.11)" (governance-commons)
# - leading alias, e.g. "## CKP.08.04 Closure - Title" (cockpit)
$headingRegex = '^#{1,6}\s.*\(([A-Z][A-Za-z0-9-]*\.\d{2})\)\s*$'
$leadingHeadingRegex = '^#{1,6}\s+([A-Z][A-Za-z0-9-]*\.\d{2}(?:\.\d{2})?)\b'
$passIdLineRegex = '^\*{0,2}Pass-ID:\*{0,2}\s*(\S+)'

if ($Mode -eq "Files") {
    if ($Paths.Count -eq 0) {
        # Default: scan only the added lines of the staged diff, not whole-file
        # content, so pre-existing citations are not retroactively flagged.
        $diffOutput = git diff --cached -U0 --diff-filter=ACM -- '*.md' 2>$null
        $currentFile = $null
        foreach ($diffLine in $diffOutput) {
            if ($diffLine -match '^\+\+\+ b/(.+)$') {
                $currentFile = $Matches[1]
                continue
            }
            if ($diffLine -match '^\+(?!\+\+)(.*)$' -and $currentFile) {
                $content = $Matches[1]
                $checked++
                if ($content -match $headingRegex) {
                    Test-Citation $Matches[1] $content "${currentFile} (staged)"
                } elseif ($content -match $leadingHeadingRegex) {
                    Test-Citation $Matches[1] $content "${currentFile} (staged)"
                }
                if ($content -match $passIdLineRegex) {
                    Test-Citation $Matches[1] $content "${currentFile} (staged)"
                }
            }
        }
        Write-Line "  PASS-ID CITATION CHECK - validate-pass-citations.ps1" "Cyan"
        Write-Line "  Registry: $registryPath"
        Write-Line "  Mode: staged diff (added lines only)  Lines checked: $checked"
        Write-Line ""
    } else {
        foreach ($path in $Paths) {
            if (-not (Test-Path $path)) { continue }
            $lines = Get-Content -Encoding UTF8 $path
            $lineNum = 0
            foreach ($line in $lines) {
                $lineNum++
                $checked++
                if ($line -match $headingRegex) {
                    Test-Citation $Matches[1] $line "${path}:${lineNum}"
                } elseif ($line -match $leadingHeadingRegex) {
                    Test-Citation $Matches[1] $line "${path}:${lineNum}"
                }
                if ($line -match $passIdLineRegex) {
                    Test-Citation $Matches[1] $line "${path}:${lineNum}"
                }
            }
        }
        Write-Line "  PASS-ID CITATION CHECK - validate-pass-citations.ps1" "Cyan"
        Write-Line "  Registry: $registryPath"
        Write-Line "  Mode: explicit full-file scan  Files scanned: $($Paths.Count)  Lines checked: $checked"
        Write-Line ""
    }
} else {
    if (-not $MessageFile -or -not (Test-Path $MessageFile)) {
        Write-Line "  [ERROR] -MessageFile is required and must exist in CommitMsg mode." "Red"
        exit 1
    }
    # Only scan the trailing trailer block (the last blank-line-separated
    # paragraph, if every non-empty line in it looks like "Key: value"). This
    # avoids matching prose that happens to line-wrap starting with "Pass-ID:"
    # elsewhere in the commit body - the same false-positive class the
    # DEV-ACCORD-CI invariant checker hit twice earlier this session.
    $allLines = @(Get-Content -Encoding UTF8 $MessageFile)
    $paragraphs = New-Object System.Collections.ArrayList
    $current = New-Object System.Collections.ArrayList
    foreach ($line in $allLines) {
        if ($line.Trim() -eq "") {
            if ($current.Count -gt 0) {
                [void]$paragraphs.Add(@($current))
                $current.Clear()
            }
        } else {
            [void]$current.Add($line)
        }
    }
    if ($current.Count -gt 0) { [void]$paragraphs.Add(@($current)) }

    # Merge trailing paragraphs that are each entirely "Key: value" shaped -
    # this repo's convention puts a blank line before "Co-Authored-By:", so
    # the real trailer block can span more than one blank-line-separated
    # paragraph. Walk backwards and stop at the first paragraph containing
    # any non-trailer-shaped (prose) line.
    $trailerKeyRegex = '^[A-Za-z][A-Za-z-]*:\s'
    $trailerLines = New-Object System.Collections.ArrayList
    for ($i = $paragraphs.Count - 1; $i -ge 0; $i--) {
        $para = $paragraphs[$i]
        $looksLikeTrailerBlock = ($para.Count -gt 0) -and (-not ($para | Where-Object { $_ -notmatch $trailerKeyRegex }))
        if (-not $looksLikeTrailerBlock) { break }
        foreach ($line in $para) { [void]$trailerLines.Add($line) }
    }
    foreach ($line in $trailerLines) {
        if ($line -match $passIdLineRegex) {
            Test-Citation $Matches[1] $line "commit message trailer"
        }
    }
    Write-Line "  PASS-ID CITATION CHECK (commit message) - validate-pass-citations.ps1" "Cyan"
    Write-Line "  Registry: $registryPath"
    Write-Line ""
}

if ($errors.Count -gt 0) {
    foreach ($e in $errors) {
        Write-Line "  [ERROR] $e" "Red"
    }
    Write-Line ""
    Write-Line "  [FAIL] $($errors.Count) unresolved PASS-ID citation(s)." "Red"
    exit 1
}

Write-Line "  [PASS] All PASS-ID citations resolve to passes.registry.json." "Green"
exit 0
