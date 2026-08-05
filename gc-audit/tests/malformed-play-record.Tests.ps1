<#
.SYNOPSIS
    Regression fixture: malformed PLAY.jsonl records must warn, not crash.

.DESCRIPTION
    Locks in existing, already-correct behavior (validate-recent-work.ps1's
    Level 3c PLAY scan already wraps ConvertFrom-Json in try/catch) as a
    named regression test, per this PASS's required fixture categories -
    a future edit to that section should not silently remove the
    catch and start crashing the whole Level 3 run on one bad line.
#>

$toolPath = Join-Path $PSScriptRoot "..\tools\validate-recent-work.ps1"

function New-Fixture([string]$Root) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    $validPlay = @{
        play_id      = "fixture-play-1"
        repo         = "fixture"
        level        = "RUN"
        status       = "closed"
        declared_at  = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        preflight    = "complete"
    } | ConvertTo-Json -Compress

    @(
        "{ this is not valid json"
        $validPlay
    ) -join "`n" | Set-Content -LiteralPath (Join-Path $Root "PLAY.jsonl") -Encoding utf8
}

Describe "malformed PLAY.jsonl records warn instead of crashing the scan" {
    $fixtureRoot = Join-Path $env:TEMP ("gc-audit-fixture-play-" + [guid]::NewGuid().ToString("N"))
    New-Fixture $fixtureRoot

    $proc = Start-Process -FilePath "pwsh" -ArgumentList @(
        "-NoProfile", "-File", $toolPath, "-TargetPath", $fixtureRoot, "-Level", "3", "-Hours", "720"
    ) -NoNewWindow -PassThru -RedirectStandardOutput (Join-Path $fixtureRoot "out.txt") -Wait
    $output = Get-Content -LiteralPath (Join-Path $fixtureRoot "out.txt") -Raw

    It "does not throw a terminating parser error for the malformed line" {
        $output | Should Match "PLAY\.jsonl parse error"
    }

    It "still counts the valid record on the following line" {
        $output | Should Match "PLAY preflight coverage: 1 pass"
    }

    It "the process itself completes (does not hang or crash the host)" {
        $proc.ExitCode | Should Not Be $null
    }

    Remove-Item -LiteralPath $fixtureRoot -Recurse -Force -ErrorAction SilentlyContinue
}
