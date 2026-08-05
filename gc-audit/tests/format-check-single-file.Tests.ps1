<#
.SYNOPSIS
    Regression fixture for GC-AUDIT.01.04 - marker and script signal quality.

.DESCRIPTION
    Real bug: validate-format.ps1 line 106 did
    `$scriptFiles = $scriptFiles | Select-Object -Unique`. When exactly one
    file survives, PowerShell's pipeline unwraps the result to a bare
    string; under this script's own `Set-StrictMode -Version Latest`,
    `.Count` on that bare string then threw PropertyNotFoundException,
    silently printing a blank count instead of a real one. Reproduced live
    against this exact fixture shape before the fix (`@(...)` around the
    pipeline).
#>

$toolPath = Join-Path $PSScriptRoot "..\tools\validate-format.ps1"

Describe "GC-AUDIT.01.04 - validate-format.ps1 reports a real count for exactly one matched script" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-format-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $fixtureRoot -Force | Out-Null
    'Write-Host "hello"' | Set-Content -LiteralPath (Join-Path $fixtureRoot "only-script.ps1") -Encoding utf8

    $output = & pwsh -NoProfile -File $toolPath -TargetPath $fixtureRoot 2>&1 | Out-String

    It "prints a real numeric count, not a blank one" {
        $output | Should Match "\[PASS\] 1 script\(s\) parse cleanly\."
    }

    It "does not raise PropertyNotFoundException" {
        $output | Should Not Match "PropertyNotFoundException"
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}
