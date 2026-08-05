<#
.SYNOPSIS
    Regression fixture for GC-AUDIT.01.01 - PASS-status parsing.

.DESCRIPTION
    Real bug: validate-recent-work.ps1's Level 4 "open PASS gates" check
    used a whole-file substring match against "status:\s*(open|draft|...)"
    instead of reading a PASS file's own authoritative Status field. A real
    file (CANON.02.md) with Status: ACCEPTED was flagged as open because
    its body separately discusses registry *entry* statuses in passing
    ("a binding entry (status: draft, accepted, sealed, or reserved)").

    Brownfield black-box: builds a real minimal fixture directory (a
    passes/ folder with one .md file shaped exactly like the real
    CANON.02 case) and asserts on the real script's stdout, not internals.
#>

$toolPath = Join-Path $PSScriptRoot "..\tools\validate-recent-work.ps1"

function New-Fixture([string]$Root) {
    $passesDir = Join-Path $Root "passes"
    New-Item -ItemType Directory -Path $passesDir -Force | Out-Null

    # Shaped exactly like the real CANON.02.md false-positive: a real
    # ACCEPTED status header, plus prose elsewhere that happens to contain
    # the substring "status: draft" describing an unrelated concept
    # (registry *entry* status, not this PASS's own status).
    @"
PASS EXAMPLE.01 - Metadata Example Regression Fixture

[NP-METADATA]
- PASS ID: EXAMPLE.01
- Status: ACCEPTED

## Body

This PASS's own status is fixed above. Elsewhere, for illustration only,
a registry entry may be proposed (status: proposed) without a PASS; a
binding entry (status: draft, accepted, sealed, or reserved) requires one.
None of that describes this PASS's own status.
"@ | Set-Content -LiteralPath (Join-Path $passesDir "EXAMPLE.01.md") -Encoding utf8
}

Describe "GC-AUDIT.01.01 - PASS-status parsing reads the metadata field, not prose examples" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-status-" + [guid]::NewGuid().ToString("N"))
    New-Fixture $fixtureRoot

    It "does not flag a PASS with a real ACCEPTED status as an open gate, despite an embedded 'status: draft' example in its body" {
        $output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot -Level 4 2>&1 | Out-String
        $output | Should Match "no open PASS gates"
        $output | Should Not Match "open PASS gate\(s\)"
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}
