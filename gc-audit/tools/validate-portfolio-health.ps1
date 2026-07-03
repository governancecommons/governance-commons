<#
.SYNOPSIS
    One-pass health check across every repo registered in projects.yaml.

.DESCRIPTION
    Read-only diagnostic. Does not mutate any repo, install any hook, or push
    anything. For each project in projects.yaml that resolves to an actual git
    repo root, reports:

      - Git state: clean/dirty, ahead/behind origin (or diverged/no-upstream)
      - Repo visibility (public/private) via `gh repo view`, best-effort
      - Dev-docs conformance vs DEV-ACCORD.08: DEV-PATH.md/DEV-PLAN.md/
        DEV-RELEASE.md/DEV-TRACKS.md must be gitignored in PUBLIC repos
        (DEV-ACCORD-CI-20) and are expected tracked in PRIVATE repos. Flags
        the dangerous case (public + tracked = leak risk) as FAIL and the
        merely-inconsistent case (private + gitignored) as WARN.
      - PASS-ID registry health, if the repo has its own passes/passes.registry.json:
        shells out to validate-pass-citations.ps1 -Mode Files -Paths <dev docs>
        (explicit full-file scan, not just staged diff) so pre-existing drift
        surfaces here instead of only at the next unrelated commit.

    This exists because each of the checks above was independently discovered
    as a live incident in one session (2026-07-02/03): an unauthorized git
    hook install, a mis-cited PASS-ID that a per-commit gate couldn't see
    because the file was gitignored, and a public/private dev-docs policy
    violated across 9 repos in one sweep. None of those required inventing a
    new rule - the rules already existed. This just checks all of them in one
    place instead of one at a time, mid-task.

.PARAMETER PortfolioRoot
    Root containing projects.yaml. Defaults to the current directory.

.PARAMETER SkipGh
    Skip the `gh repo view` visibility check (e.g. no `gh` auth available).
    Dev-docs conformance check is skipped too when visibility is unknown,
    since it depends on knowing public vs private.

.PARAMETER Group
    Filter to one projects.yaml group.

.EXAMPLE
    pwsh governance-commons/gc-audit/tools/validate-portfolio-health.ps1 -PortfolioRoot C:\dev
#>

param(
    [string] $PortfolioRoot = ".",
    [switch] $SkipGh,
    [string] $Group = "",
    [switch] $Help
)

if ($Help) {
    Get-Help $PSCommandPath -Full
    exit 0
}

function Write-Line([string]$Text, [string]$Color = "Gray") {
    Write-Host $Text -ForegroundColor $Color
}

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PortfolioRoot)
$YamlFile = Join-Path $Root "projects.yaml"
if (-not (Test-Path $YamlFile)) {
    Write-Line "  [ERROR] Could not find projects.yaml at $YamlFile" "Red"
    exit 1
}
$RawYaml = Get-Content $YamlFile -Raw

# Same regex-based mini-parser as dev-status.ps1 (no external YAML module).
function Read-Projects([string]$content) {
    $blocks = [regex]::Split($content, '(?m)^  - (?=name:)') |
        Where-Object { $_.Trim() -ne '' -and $_ -notmatch '^version|^updated|^root|^projects|^#' }
    foreach ($block in $blocks) {
        $obj = [ordered]@{}
        foreach ($line in ($block -split "`n")) {
            if ($line -match '^\s{0,4}(\w[\w_-]*):\s*(.+)$') {
                $key = $Matches[1].Trim()
                $val = $Matches[2].Trim().Trim('"').Trim("'")
                if ($val -eq '~') { $val = $null }
                $obj[$key] = $val
            }
        }
        if ($obj['name']) { [PSCustomObject]$obj }
    }
}

$devDocFiles = @("DEV-PATH.md", "DEV-PLAN.md", "DEV-RELEASE.md", "DEV-TRACKS.md")
$citationsValidator = Join-Path $PSScriptRoot "validate-pass-citations.ps1"

function Get-RepoSlug([string]$fullPath) {
    $url = (git -C $fullPath remote get-url origin 2>$null)
    if (-not $url) { return $null }
    if ($url -match 'github\.com[:/]+([^/]+)/([^/.]+?)(\.git)?$') {
        return "$($Matches[1])/$($Matches[2])"
    }
    return $null
}

$projects = @(Read-Projects $RawYaml)
if ($Group) { $projects = @($projects | Where-Object { $_.group -eq $Group }) }

$rows = New-Object System.Collections.ArrayList
$failCount = 0
$warnCount = 0

foreach ($project in $projects) {
    $fullPath = Join-Path $Root $project.path
    if (-not (Test-Path $fullPath)) {
        [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = "SKIP"; Detail = "path not found: $($project.path)" })
        continue
    }

    Push-Location $fullPath
    try {
        $isRepo = (git rev-parse --is-inside-work-tree 2>$null)
        if ($isRepo -ne "true") {
            [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = "SKIP"; Detail = "not a git repo (likely a subdirectory of a parent repo)" })
            continue
        }
        $repoRoot = (git rev-parse --show-toplevel 2>$null)
        if ($repoRoot -and (Resolve-Path $repoRoot).Path -ne (Resolve-Path $fullPath).Path) {
            [void]$rows.Add([PSCustomObject]@{
                Name  = $project.name
                Level = "INFO"
                Detail = "nested inside a parent repo (root: $repoRoot) - checks below run against that parent's history, not a standalone repo"
            })
        }

        # --- Git cleanliness + ahead/behind ---
        $dirty = @(git status --porcelain 2>$null | Where-Object { $_ -ne "" })
        $gitLevel = if ($dirty.Count -gt 0) { "WARN" } else { "PASS" }
        $gitDetail = if ($dirty.Count -gt 0) { "$($dirty.Count) uncommitted change(s)" } else { "clean" }

        $hasUpstream = (git rev-parse --abbrev-ref "@{upstream}" 2>$null)
        if ($hasUpstream) {
            $ahead  = (git rev-list "@{upstream}..HEAD" --count 2>$null)
            $behind = (git rev-list "HEAD..@{upstream}" --count 2>$null)
            if ([int]$ahead -gt 0 -and [int]$behind -gt 0) {
                $gitLevel = "WARN"
                $gitDetail += "; diverged from upstream (+$ahead/-$behind, needs merge/rebase)"
            } elseif ([int]$ahead -gt 0) {
                $gitDetail += "; $ahead commit(s) unpushed"
            } elseif ([int]$behind -gt 0) {
                $gitLevel = "WARN"
                $gitDetail += "; $behind commit(s) behind origin"
            }
        } else {
            $gitDetail += "; no upstream tracking branch"
        }
        [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = $gitLevel; Detail = "git: $gitDetail" })

        # --- Visibility + dev-docs conformance ---
        $visibility = $null
        if (-not $SkipGh) {
            $slug = Get-RepoSlug $fullPath
            if ($slug) {
                $visibility = (gh repo view $slug --json visibility -q .visibility 2>$null)
            }
        }

        if ($visibility) {
            $trackedDevDocs = @($devDocFiles | Where-Object { (git ls-files -- $_ 2>$null) })
            $ignoredDevDocs = @($devDocFiles | Where-Object {
                if (-not (Test-Path $_)) { return $false }
                git check-ignore -q $_ 2>$null
                $LASTEXITCODE -eq 0
            })

            if ($visibility -eq "PUBLIC" -and $trackedDevDocs.Count -gt 0) {
                $failCount++
                [void]$rows.Add([PSCustomObject]@{
                    Name = $project.name; Level = "FAIL"
                    Detail = "PUBLIC repo tracks dev-docs ($($trackedDevDocs -join ', ')) - violates DEV-ACCORD-CI-20 (leak risk)"
                })
            } elseif ($visibility -eq "PRIVATE" -and $ignoredDevDocs.Count -gt 0) {
                $warnCount++
                [void]$rows.Add([PSCustomObject]@{
                    Name = $project.name; Level = "WARN"
                    Detail = "PRIVATE repo gitignores dev-docs ($($ignoredDevDocs -join ', ')) - inconsistent with the portfolio's private-repo default (track them)"
                })
            } else {
                [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = "PASS"; Detail = "dev-docs conformance OK ($visibility repo)" })
            }
        } else {
            [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = "INFO"; Detail = "visibility unknown (no gh/no GitHub remote) - dev-docs conformance not checked" })
        }

        # --- PASS-ID registry health (whole-file scan, not just staged diff) ---
        if (Test-Path "passes/passes.registry.json") {
            $scanTargets = @($devDocFiles + @("passchangelog.md") | Where-Object { Test-Path $_ })
            if ($scanTargets.Count -gt 0) {
                $output = & pwsh -NoProfile -File $citationsValidator -Mode Files -Paths $scanTargets -PortfolioRoot $fullPath 2>&1
                if ($LASTEXITCODE -ne 0) {
                    $failCount++
                    $errorLines = @($output | Where-Object { $_ -match '\[ERROR\]' })
                    [void]$rows.Add([PSCustomObject]@{
                        Name = $project.name; Level = "FAIL"
                        Detail = "$($errorLines.Count) unresolved PASS-ID citation(s) in dev-docs (see validate-pass-citations.ps1 -PortfolioRoot $($project.path) for detail)"
                    })
                } else {
                    [void]$rows.Add([PSCustomObject]@{ Name = $project.name; Level = "PASS"; Detail = "PASS-ID citations resolve cleanly" })
                }
            }
        }
    } finally {
        Pop-Location
    }
}

Write-Line ""
Write-Line "  PORTFOLIO HEALTH CHECK - validate-portfolio-health.ps1" "Cyan"
Write-Line "  Root: $Root" "Gray"
Write-Line "  Projects checked: $($projects.Count)" "Gray"
Write-Line ""

foreach ($row in $rows) {
    $color = switch ($row.Level) {
        "FAIL" { "Red" }
        "WARN" { "Yellow" }
        "PASS" { "Green" }
        "SKIP" { "DarkGray" }
        default { "Gray" }
    }
    Write-Line ("  [{0,-4}] {1,-24} {2}" -f $row.Level, $row.Name, $row.Detail) $color
}

Write-Line ""
if ($failCount -gt 0) {
    Write-Line "  [FAIL] $failCount issue(s) require attention; $warnCount warning(s)." "Red"
    exit 1
}
if ($warnCount -gt 0) {
    Write-Line "  [WARN] $warnCount warning(s); no blocking failures." "Yellow"
    exit 0
}
Write-Line "  [PASS] Portfolio health check clean." "Green"
exit 0
