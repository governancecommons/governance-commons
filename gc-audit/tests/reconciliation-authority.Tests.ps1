BeforeAll {
    $tools = Join-Path $PSScriptRoot '..\tools'
    function New-Fixture {
        $fixture = Join-Path $TestDrive ([guid]::NewGuid().ToString('N'))
        New-Item -ItemType Directory -Path $fixture -Force | Out-Null
        return $fixture
    }
    function Put-Fixture($root, $relative, $content) {
        $file = Join-Path $root $relative
        New-Item -ItemType Directory -Path (Split-Path $file) -Force | Out-Null
        [IO.File]::WriteAllText($file, $content)
    }
    function Check-Fixture($tool, $root, $project='') {
        $args = @('-NoProfile','-File',(Join-Path $tools $tool),'-TargetPath',$root)
        if ($project) { $args += @('-Project',$project) }
        $result = & pwsh @args 2>&1 | Out-String
        return @{ Code=$LASTEXITCODE; Output=$result }
    }
    $validDoc = "# DEV-PLAN $([char]0x2014) Example`n`n**AUTHORITY LEVEL:** AL:1`n**Status:** Active`n"
    $registry = "projects:`n  - name: example`n    path: example`n    planning:`n      canonical: example/DEV-PLAN.md`n"
}

Describe 'Planning ownership preserves history without hiding active failures' {
    It 'selects the registered owner and retains duplicate private copies' {
        $root = New-Fixture
        Put-Fixture $root 'projects.yaml' $registry
        Put-Fixture $root 'example/DEV-PLAN.md' $validDoc
        Put-Fixture $root 'dev-docs/example/DEV-PLAN.md' $validDoc
        $result = Check-Fixture 'validate-planning.ps1' $root
        $result.Code | Should -Be 0
        $result.Output | Should -Match 'Non-canonical copy retained'
        (Get-Content (Join-Path $root 'dev-docs/example/DEV-PLAN.md') -Raw) | Should -Be $validDoc
    }
    It 'does not treat ignored reconciliation draft archives as active plans' {
        $root = New-Fixture
        Put-Fixture $root 'example/DEV-PLAN.md' $validDoc
        Put-Fixture $root 'example/.reconciliation/local-parity-draft/DEV-PLAN.md' $validDoc
        (Check-Fixture 'validate-planning.ps1' $root).Code | Should -Be 0
    }
    It 'fails for a missing explicit owner' {
        $root = New-Fixture
        Put-Fixture $root 'projects.yaml' $registry
        (Check-Fixture 'validate-planning.ps1' $root).Code | Should -Be 1
    }
    It 'rejects pointers outside the portfolio' {
        $root = New-Fixture
        Put-Fixture $root 'projects.yaml' ($registry.Replace('example/DEV-PLAN.md','../DEV-PLAN.md'))
        $result = Check-Fixture 'validate-planning.ps1' $root
        $result.Code | Should -Be 1
        $result.Output | Should -Match 'escapes portfolio'
    }
    It 'still rejects two active unregistered documents sharing a heading' {
        $root = New-Fixture
        Put-Fixture $root 'one/DEV-PLAN.md' $validDoc
        Put-Fixture $root 'two/DEV-PLAN.md' $validDoc
        (Check-Fixture 'validate-planning.ps1' $root).Code | Should -Be 1
    }
    It 'does not hide malformed nested child documents behind an umbrella owner' {
        $root = New-Fixture
        Put-Fixture $root 'projects.yaml' $registry
        Put-Fixture $root 'example/DEV-PLAN.md' $validDoc
        Put-Fixture $root 'example/child/DEV-PLAN.md' '# Wrong heading'
        (Check-Fixture 'validate-planning.ps1' $root).Code | Should -Be 1
    }
    It 'lets an explicit project scan inspect malformed preserved copies' {
        $root = New-Fixture
        Put-Fixture $root 'projects.yaml' $registry
        Put-Fixture $root 'example/DEV-PLAN.md' $validDoc
        Put-Fixture $root 'dev-docs/example/DEV-PLAN.md' '# Wrong heading'
        (Check-Fixture 'validate-planning.ps1' $root 'dev-docs/example').Code | Should -Be 1
    }
}

Describe 'Bootstrap accepts existing authority patterns and rejects broken pointers' {
    It 'accepts a public safe stub without private paths' {
        $root = New-Fixture
        Put-Fixture $root 'repo/AGENTS.md' "# AGENTS.md - public stub`n`nRead [README](README.md). Private instructions are external. Ask the owner for bootstrap context."
        (Check-Fixture 'validate-bootstrap.ps1' $root 'repo').Code | Should -Be 0
    }
    It 'accepts an existing local onboarding authority' {
        $root = New-Fixture
        Put-Fixture $root 'repo/AGENTS.md' 'Read [guidance](docs/agent-guidance/local-agent-guidance.md) before acting.'
        Put-Fixture $root 'repo/docs/agent-guidance/local-agent-guidance.md' '# Local authority'
        (Check-Fixture 'validate-bootstrap.ps1' $root 'repo').Code | Should -Be 0
    }
    It 'rejects a missing local onboarding authority' {
        $root = New-Fixture
        Put-Fixture $root 'repo/AGENTS.md' 'Read [guidance](docs/agent-guidance/missing.md) before acting.'
        (Check-Fixture 'validate-bootstrap.ps1' $root 'repo').Code | Should -Be 1
    }
    It 'rejects an escaping local authority pointer' {
        $root = New-Fixture
        Put-Fixture $root 'outside/agent-guidance.md' '# Outside authority'
        Put-Fixture $root 'repo/AGENTS.md' 'Read [guidance](../outside/agent-guidance.md) before acting.'
        (Check-Fixture 'validate-bootstrap.ps1' $root 'repo').Code | Should -Be 1
    }
    It 'still rejects universal automatic reading claims' {
        $root = New-Fixture
        Put-Fixture $root 'repo/AGENTS.md' 'Read DEV-ACCORD.03. All agents automatically read this file.'
        (Check-Fixture 'validate-bootstrap.ps1' $root 'repo').Code | Should -Be 1
    }
    It 'rejects an empty bootstrap without throwing an indexing exception' {
        $root = New-Fixture
        Put-Fixture $root 'repo/AGENTS.md' ''
        $result = Check-Fixture 'validate-bootstrap.ps1' $root 'repo'
        $result.Code | Should -Be 1
        $result.Output | Should -Not -Match 'Index was outside'
    }
}
