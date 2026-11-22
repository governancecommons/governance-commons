BeforeAll {
  $tool = Join-Path $PSScriptRoot '..\tools\validate-playbook.ps1'
  function New-Record([string]$Id, [string[]]$Checks) {
    $bucket = @{ started_at = $null; ended_at = $null; duration_ms = 0 }
    return [ordered]@{
        play_id = $Id; repo = 'fixture'; level = 'RUN'; status = 'closed'
        declared_at = '2026-11-22T00:00:00Z'; authorized_by = 'agent'
        scope = 'Fixture record'; timing = @{ read=$bucket; plan=$bucket; execute=$bucket; verify=$bucket; close=$bucket }
        dev_docs_check = @{ status='not-needed'; note='Fixture only' }
        validation_profile = @{ profile='RUN'; checks=$Checks }
        commit_ref = 'fixture'; preflight = 'complete'
    }
  }
}

Describe 'append-only PLAY corrections' {
    It 'preserves a bad source line while disambiguating its ID and retracting an incomplete profile' {
        $first = (New-Record 'duplicate' @('dev-docs-check','gc-audit.playbook')) | ConvertTo-Json -Depth 9 -Compress
        $second = (New-Record 'duplicate' @('dev-docs-check')) | ConvertTo-Json -Depth 9 -Compress
        $hash = [Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData([System.Text.Encoding]::UTF8.GetBytes($second)))
        $repair = New-Record 'correction' @('dev-docs-check','gc-audit.playbook')
        $repair.corrections = @(
            @{ target_line=2; sha256=$hash; action='retract-incomplete-validation-profile'; reason='Missing check was not run.' },
            @{ target_line=2; sha256=$hash; action='disambiguate-play-id'; replacement_play_id='duplicate-2'; reason='Distinct PLAY reused the ID.' }
        )
        $file = Join-Path $TestDrive 'PLAY.jsonl'
        @($first,$second,($repair | ConvertTo-Json -Depth 9 -Compress)) | Set-Content -LiteralPath $file -Encoding utf8
        $result = (& pwsh -NoProfile -File $tool -FilePath $file -Json | ConvertFrom-Json)
        $LASTEXITCODE | Should -Be 0
        $result.status | Should -Be 'warn'
        $result.errors.Count | Should -Be 0
        $result.warnings.Count | Should -Be 2
        (Get-Content -LiteralPath $file)[1] | Should -Be $second
    }

    It 'rejects a correction whose hash no longer matches its target' {
        $bad = (New-Record 'bad' @('dev-docs-check')) | ConvertTo-Json -Depth 9 -Compress
        $repair = New-Record 'correction-2' @('dev-docs-check','gc-audit.playbook')
        $repair.corrections = @(@{ target_line=1; sha256=('0' * 64); action='retract-incomplete-validation-profile'; reason='Fixture mismatch' })
        $file = Join-Path $TestDrive 'bad-PLAY.jsonl'
        @($bad,($repair | ConvertTo-Json -Depth 9 -Compress)) | Set-Content -LiteralPath $file -Encoding utf8
        $result = (& pwsh -NoProfile -File $tool -FilePath $file -Json | ConvertFrom-Json)
        $LASTEXITCODE | Should -Be 1
        $result.errors -join ' ' | Should -Match 'SHA-256 does not match'
    }
}
