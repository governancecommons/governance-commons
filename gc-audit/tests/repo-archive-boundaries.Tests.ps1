<#
.SYNOPSIS
    Regression fixture for GC-AUDIT.01.03 - repository and archive boundaries.

.DESCRIPTION
    Real bug: validate-recent-work.ps1's own Get-GitRoots had no exclusion
    filter, unlike every sibling script in this tool family
    (validate-format.ps1, validate-bootstrap.ps1, validate-ci-invariants.ps1,
    ...), which all already exclude _archive/node_modules/.venv/dist/etc.
    Confirmed live: lasso_archive and lasso-mvp_archive are real git repos
    at the portfolio root with no archive marker recognized by the old
    filter, so a portfolio-root run mixed them into "dirty repos" and
    "recent commits" as if they were active work.

    Brownfield black-box: builds two REAL git repos on disk (git init +
    a real commit + a real uncommitted dirty file) - one ordinary, one
    named like a portfolio archive repo (*_archive) - and asserts the
    archived one never appears in Level 2's dirty-repo output while the
    active one does.
#>

$toolPath = Join-Path $PSScriptRoot "..\tools\validate-recent-work.ps1"

function New-GitRepo([string]$Path) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
    Push-Location $Path
    try {
        git init --quiet 2>&1 | Out-Null
        git config user.email "fixture@example.com" 2>&1 | Out-Null
        git config user.name "Fixture" 2>&1 | Out-Null
        "seed" | Set-Content -LiteralPath (Join-Path $Path "README.md") -Encoding utf8
        git add -A 2>&1 | Out-Null
        git commit -m "seed" --quiet 2>&1 | Out-Null
        # Now make it dirty, on purpose, so Level 2 has something to report.
        "dirty" | Set-Content -LiteralPath (Join-Path $Path "dirty.txt") -Encoding utf8
    } finally {
        Pop-Location
    }
}

Describe "GC-AUDIT.01.03 - archived repos are excluded from active-repo scanning" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-archive-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $fixtureRoot -Force | Out-Null
    New-GitRepo (Join-Path $fixtureRoot "active-repo")
    New-GitRepo (Join-Path $fixtureRoot "some-product_archive")
    New-GitRepo (Join-Path $fixtureRoot ".pytest-tmp-provider")
    New-GitRepo (Join-Path $fixtureRoot ".test-tmp-bridge")
    "{ malformed fixture json" | Set-Content -LiteralPath (Join-Path $fixtureRoot ".pytest-tmp-provider\PLAY.jsonl") -Encoding utf8
    "{ malformed fixture json" | Set-Content -LiteralPath (Join-Path $fixtureRoot ".test-tmp-bridge\PLAY.jsonl") -Encoding utf8

    $output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot -Level 2 -Hours 720 2>&1 | Out-String
    $level3Output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot -Level 3 -Hours 720 2>&1 | Out-String

    It "reports the active repo as dirty" {
        $output | Should Match "dirty: active-repo"
    }

    It "does not scan the archived repo at all" {
        $output | Should Not Match "some-product_archive"
    }

    It "does not scan custom pytest or test scratch repositories" {
        $output | Should Not Match "\.pytest-tmp-provider"
        $output | Should Not Match "\.test-tmp-bridge"
    }

    It "does not parse PLAY fixtures inside custom scratch trees" {
        $level3Output | Should Not Match "PLAY\.jsonl parse error"
        $level3Output | Should Not Match "\.pytest-tmp-provider"
        $level3Output | Should Not Match "\.test-tmp-bridge"
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}
