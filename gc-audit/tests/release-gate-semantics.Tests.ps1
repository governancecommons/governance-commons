<#
.SYNOPSIS
    Regression fixture for GC-AUDIT.01.02 - release-readiness semantics.

.DESCRIPTION
    Real bug: validate-recent-work.ps1's Level 4 DEV-RELEASE.md check only
    grepped the whole file for the literal words pending/blocked/not
    ready/tbd/todo. Confirmed live against cockpit/DEV-RELEASE.md: reported
    "no pending items" despite real unchecked "- [ ] " entry-condition
    gates, because those gates use checkbox syntax and a "In progress"
    status cell, none of which are in that word list.

    This fixture mirrors cockpit's real Release Table shape (a Done
    version, an "In progress" active version with real open gates, and a
    bare-unchecked future version with its own unstarted gates) and proves
    two things structurally, not by keyword:
      1. The active version's real open gates ARE reported (genuine gap).
      2. The future version's unstarted gates are NOT reported (must not
         falsely close future work, but must not falsely gate it either).
#>

$toolPath = Join-Path $PSScriptRoot "..\tools\validate-recent-work.ps1"

function New-Fixture([string]$Root) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    @"
# DEV-RELEASE - Fixture

## Release Table

| Version | Name | Description | Status |
| --- | --- | --- | --- |
| v0.1.0 | Foundation | done | Done |
| v1.0.0 | Active Slice | the version under active development | In progress |
| v1.1.0 | Future Slice | not started yet | Planned |

## v1.0.0 Entry Conditions

- [ ] real open gate one
- [ ] real open gate two
- [x] already done

## v1.1.0 Entry Conditions

- [ ] future gate, not started, not a current blocker
- [ ] another future gate
"@ | Set-Content -LiteralPath (Join-Path $Root "DEV-RELEASE.md") -Encoding utf8
}

Describe "GC-AUDIT.01.02 - active-release gates are reported structurally, future releases are not gated" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-release-" + [guid]::NewGuid().ToString("N"))
    New-Fixture $fixtureRoot
    $output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot -Level 4 2>&1 | Out-String
    $exitCode = $LASTEXITCODE

    It "reports the active (In progress) release's real unchecked gates" {
        $output | Should Match "2 unchecked gate\(s\) in the active release"
        $output | Should Match "real open gate one"
        $output | Should Match "real open gate two"
    }

    It "does not count the already-checked item as a gap" {
        $output | Should Not Match "already done"
    }

    It "does not report the future (Planned) release's unstarted gates as a current blocker" {
        $output | Should Not Match "future gate, not started"
        $output | Should Not Match "another future gate"
    }

    It "fails release readiness while the active release has unchecked gates" {
        $exitCode | Should Be 1
        $output | Should Match "Result: FAIL"
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}

function New-SectionMetadataFixture([string]$Root) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    @"
# DEV-RELEASE - Section Metadata Fixture

## Release v1.2.0 - Public Release

**Status:** In progress - publication remaining

### What ships

- packages

### Admission criteria

- [ ] real section-metadata gate
- [x] completed section gate

## Release v1.3.0 - Future Release

**Status:** Planned

### Admission criteria

- [ ] future section gate
"@ | Set-Content -LiteralPath (Join-Path $Root "DEV-RELEASE.md") -Encoding utf8
}

Describe "GC-AUDIT.01.02 - section-scoped release metadata is authoritative" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-release-section-" + [guid]::NewGuid().ToString("N"))
    New-SectionMetadataFixture $fixtureRoot
    $output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot -Level 4 2>&1 | Out-String
    $exitCode = $LASTEXITCODE

    It "finds gates nested below subheadings in the active version section" {
        $output | Should Match "1 unchecked gate\(s\) in the active release"
        $output | Should Match "real section-metadata gate"
    }

    It "does not cross the peer release heading into future gates" {
        $output | Should Not Match "future section gate"
    }

    It "returns a failing release-readiness exit code" {
        $exitCode | Should Be 1
        $output | Should Match "Result: FAIL"
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}
