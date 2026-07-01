# validate-review-grammar.ps1
# Checks that a repo has an adoptable review grammar and agent instructions point to it.
#
# Usage:
#   pwsh -File validate-review-grammar.ps1
#   pwsh -File validate-review-grammar.ps1 -TargetPath C:\work\repo

param(
    [string]$TargetPath = ".",
    [string]$GrammarPath = "",
    [switch]$AllowMissingAgentInstructions
)

$root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)

if (-not (Test-Path $root)) {
    Write-Host "Target path does not exist: $TargetPath" -ForegroundColor Red
    exit 1
}

$grammarCandidates = @()
if ($GrammarPath) {
    $grammarCandidates += $GrammarPath
} else {
    $grammarCandidates += "docs/REVIEW-GRAMMAR.md"
    $grammarCandidates += ".governance/review-grammar.md"
    $grammarCandidates += "REVIEW-GRAMMAR.md"
}

$grammarFile = $null
foreach ($candidate in $grammarCandidates) {
    $full = Join-Path $root $candidate
    if (Test-Path $full) {
        $grammarFile = $full
        break
    }
}

$failures = @()
$warnings = @()

function Find-PortfolioRoot([string]$start) {
    $cursor = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($start)
    while ($true) {
        if ((Test-Path (Join-Path $cursor "projects.yaml")) -and
            (Test-Path (Join-Path $cursor "docs\REVIEW-GRAMMAR.md"))) {
            return $cursor
        }
        $parent = Split-Path -Parent $cursor
        if (-not $parent -or $parent -eq $cursor) { return $null }
        $cursor = $parent
    }
}

function Resolve-GrammarContent([string]$file) {
    $text = Get-Content $file -Raw

    $requiredProbe = @("normalize", "validate", "de-stale", "next action")
    $hasCoreTerms = $true
    foreach ($probe in $requiredProbe) {
        if ($text -notmatch [regex]::Escape($probe)) {
            $hasCoreTerms = $false
            break
        }
    }
    if ($hasCoreTerms) {
        return [PSCustomObject]@{ Text = $text; Source = $file; Adapter = $false }
    }

    $linkMatches = [regex]::Matches($text, '(?i)(?:\]\(|`)([^)`]+REVIEW-GRAMMAR\.md)(?:\)|`)')
    foreach ($m in $linkMatches) {
        $candidate = $m.Groups[1].Value
        if ([System.IO.Path]::IsPathRooted($candidate)) {
            $resolved = $candidate
        } else {
            $resolved = Join-Path (Split-Path -Parent $file) $candidate
        }
        $full = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($resolved)
        if (-not (Test-Path $full)) { continue }

        $portfolioRoot = Find-PortfolioRoot $root
        if ($portfolioRoot) {
            $portfolioFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($portfolioRoot)
            $targetFull = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($full)
            if (-not $targetFull.StartsWith($portfolioFull, [System.StringComparison]::OrdinalIgnoreCase)) {
                $warnings += "Review grammar adapter points outside portfolio root: $candidate"
                continue
            }
        }

        return [PSCustomObject]@{ Text = (Get-Content $full -Raw); Source = $full; Adapter = $true }
    }

    return [PSCustomObject]@{ Text = $text; Source = $file; Adapter = $false }
}

if (-not $grammarFile) {
    $portfolioRoot = Find-PortfolioRoot $root
    if ($portfolioRoot) {
        $grammarFile = Join-Path $portfolioRoot "docs\REVIEW-GRAMMAR.md"
    }
}

if (-not $grammarFile) {
    $failures += "No review grammar file found. Expected one of: $($grammarCandidates -join ', ')"
} else {
    $resolvedGrammar = Resolve-GrammarContent $grammarFile
    $grammar = $resolvedGrammar.Text
    $requiredTerms = @(
        "normalize",
        "validate",
        "verify",
        "adversarial audit",
        "meta-audit",
        "trace",
        "authority audit",
        "registry audit",
        "close the loop",
        "de-stale",
        "first-order review",
        "second-order review",
        "third-order review",
        "open",
        "spec-complete",
        "release-complete",
        "runtime-complete",
        "scope",
        "findings",
        "evidence",
        "validation",
        "next action"
    )

    foreach ($term in $requiredTerms) {
        if ($grammar -notmatch [regex]::Escape($term)) {
            $failures += "Review grammar missing required term: $term"
        }
    }
}

$agentCandidates = @(
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    ".governance/agents.md"
)

$agentFiles = @()
foreach ($candidate in $agentCandidates) {
    $full = Join-Path $root $candidate
    if (Test-Path $full) {
        $agentFiles += $full
    }
}

if ($agentFiles.Count -eq 0) {
    if ($AllowMissingAgentInstructions) {
        $warnings += "No common agent instruction file found."
    } else {
        $failures += "No common agent instruction file found. Expected one of: $($agentCandidates -join ', ')"
    }
} else {
    $referencesGrammar = $false
    foreach ($agentFile in $agentFiles) {
        $text = Get-Content $agentFile -Raw
        if ($text -match "REVIEW-GRAMMAR" -or $text -match "review grammar" -or $text -match "DEV-ACCORD\.03") {
            $referencesGrammar = $true
            break
        }
    }

    if (-not $referencesGrammar) {
        $failures += "Agent instruction files exist but none reference REVIEW-GRAMMAR."
    }
}

if ($failures.Count -gt 0) {
    Write-Host ""
    Write-Host "Review grammar validation failed:" -ForegroundColor Red
    $failures | ForEach-Object { Write-Host "  FAIL  $_" -ForegroundColor Yellow }
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Warnings:" -ForegroundColor DarkYellow
        $warnings | ForEach-Object { Write-Host "  WARN  $_" -ForegroundColor DarkYellow }
    }
    Write-Host ""
    exit 1
}

Write-Host "Review grammar validation passed." -ForegroundColor Green
if ($grammarFile) {
    $display = Resolve-Path -Path $grammarFile -Relative
    Write-Host "  grammar: $display" -ForegroundColor DarkGray
    if ($resolvedGrammar -and $resolvedGrammar.Adapter) {
        $sourceDisplay = Resolve-Path -Path $resolvedGrammar.Source -Relative
        Write-Host "  canonical: $sourceDisplay" -ForegroundColor DarkGray
    }
}
if ($agentFiles.Count -gt 0) {
    Write-Host "  agent instruction files checked: $($agentFiles.Count)" -ForegroundColor DarkGray
}
if ($warnings.Count -gt 0) {
    $warnings | ForEach-Object { Write-Host "  WARN  $_" -ForegroundColor DarkYellow }
}
