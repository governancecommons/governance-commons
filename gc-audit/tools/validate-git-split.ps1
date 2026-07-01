<#
.SYNOPSIS
    Audits git branch topology against DEV-ACCORD.10.

.DESCRIPTION
    Reports repositories that are currently off their remote default branch.
    This is a non-blocking warning by default because branches can be legitimate
    when explicitly authorized by the human.

    Use -Strict to treat warnings as failures.

.PARAMETER TargetPath
    Portfolio or repository root to scan (default current directory).

.PARAMETER Strict
    Treat branch-split warnings as failures.

.PARAMETER Help
    Show help and exit.
#>
param(
    [string] $TargetPath = ".",
    [switch] $Strict,
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$Warnings = 0
$Errors = 0

function Write-Finding([string]$level, [string]$path, [string]$message) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    if ($rel -eq $path) { $rel = "." }
    $color = "DarkYellow"
    if ($level -eq "ERROR") { $color = "Red" }
    if ($level -eq "PASS") { $color = "DarkGreen" }
    Write-Host "  [$level]" -NoNewline -ForegroundColor $color
    Write-Host " $rel" -NoNewline -ForegroundColor White
    Write-Host " - $message" -ForegroundColor $color
    if ($level -eq "ERROR") { $script:Errors++ }
    if ($level -eq "WARN") { $script:Warnings++ }
}

function Get-GitRoots {
    $roots = @()
    if (Test-Path (Join-Path $Root ".git")) { $roots += $Root }
    Get-ChildItem -Path $Root -Recurse -Depth 3 -Force -Directory -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -eq ".git" -and
            $_.FullName -notmatch '(?i)([\\/](node_modules|archive|_archive|remote|\.claude[\\/]worktrees|\.pytest_cache|dist|\.venv|\.eco)[\\/]|[\\/]state-snapshot)'
        } |
        ForEach-Object {
            $repoRoot = Split-Path $_.FullName -Parent
            if ($repoRoot -and ($repoRoot -notin $roots)) { $roots += $repoRoot }
        }
    return $roots | Select-Object -Unique
}

function Get-DefaultBranch([string]$repoRoot) {
    $originHead = (& git -C $repoRoot symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>$null) -join ""
    if ($originHead -match '^origin/(.+)$') { return $Matches[1] }

    foreach ($candidate in @("main", "master", "trunk")) {
        & git -C $repoRoot show-ref --verify --quiet "refs/heads/$candidate" 2>$null
        if ($LASTEXITCODE -eq 0) { return $candidate }
    }
    return ""
}

Write-Host ""
Write-Host "  DEV-ACCORD GIT SPLIT CHECK - validate-git-split.ps1" -ForegroundColor White
Write-Host "  Standard: GC:2018 / DEV-ACCORD.10" -ForegroundColor DarkGray
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  $Root" -ForegroundColor DarkGray
Write-Host ""

$repos = @(Get-GitRoots)
foreach ($repo in $repos) {
    $branch = (& git -C $repo rev-parse --abbrev-ref HEAD 2>$null) -join ""
    if (-not $branch) {
        Write-Finding "ERROR" $repo "unable to determine current branch"
        continue
    }
    if ($branch -eq "HEAD") {
        Write-Finding "WARN" $repo "detached HEAD; verify human authorization before publishing"
        continue
    }

    $defaultBranch = Get-DefaultBranch $repo
    if (-not $defaultBranch) {
        Write-Finding "WARN" $repo "current branch '$branch'; default branch unknown"
        continue
    }

    if ($branch -ne $defaultBranch) {
        Write-Finding "WARN" $repo "current branch '$branch' differs from default '$defaultBranch'; verify DEV-ACCORD.10 split authorization"
    } else {
        Write-Finding "PASS" $repo "current branch '$branch' matches default publish branch"
    }
}

Write-Host ""
if ($Errors -eq 0 -and $Warnings -eq 0) {
    Write-Host "  -- $($repos.Count) repos checked  |  all conformant  |  DEV-ACCORD.10 --" -ForegroundColor Green
} elseif ($Errors -eq 0) {
    Write-Host "  -- $($repos.Count) repos checked  |  0 errors  $Warnings warnings  |  DEV-ACCORD.10 --" -ForegroundColor DarkYellow
} else {
    Write-Host "  -- $($repos.Count) repos checked  |  $Errors errors  $Warnings warnings  |  DEV-ACCORD.10 --" -ForegroundColor Red
}
Write-Host ""

if ($Strict -and ($Errors -gt 0 -or $Warnings -gt 0)) { exit 1 }
if ($Errors -gt 0) { exit 1 }
exit 0
