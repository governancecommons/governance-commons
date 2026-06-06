<#
.SYNOPSIS
    Shows git status for all governance-commons sub-projects, driven by projects.yaml.

.PARAMETER Group
    Filter to a specific group: specs, runtime, sdk, sites

.PARAMETER DirtyOnly
    Show only repos with uncommitted changes.

.EXAMPLE
    .\tools\gc-status.ps1
    .\tools\gc-status.ps1 -DirtyOnly
    .\tools\gc-status.ps1 -Group specs
    .\tools\gc-status.ps1 -Group sites
#>
param(
    [string] $Group     = "",
    [switch] $DirtyOnly
)

$Root     = Split-Path $PSScriptRoot -Parent
$YamlFile = Join-Path $Root "projects.yaml"

# ── Parse projects.yaml (no external module needed) ──────────────────────────
function Read-Projects([string]$yamlPath) {
    $content = Get-Content $yamlPath -Raw
    $blocks  = [regex]::Split($content, '(?m)^  - (?=name:)') | Where-Object { $_.Trim() -ne '' -and $_ -notmatch '^version|^updated|^root|^projects|^#' }
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

# ── Group display config ──────────────────────────────────────────────────────
$GroupMeta = @{
    "specs"   = @{ Label = "SPECS";    Color = "Cyan"    }
    "runtime" = @{ Label = "RUNTIME";  Color = "Green"   }
    "sdk"     = @{ Label = "SDK";      Color = "Magenta" }
    "sites"   = @{ Label = "SITES";    Color = "Blue"    }
    "planned" = @{ Label = "PLANNED";  Color = "DarkGray"}
}

$GroupOrder = @("specs","runtime","sdk","sites","planned")

# ── Helpers ───────────────────────────────────────────────────────────────────
function Get-RelativeTime([datetime]$date) {
    $diff = (Get-Date) - $date
    if ($diff.TotalMinutes -lt 60)  { return "$([int]$diff.TotalMinutes)m ago" }
    if ($diff.TotalHours   -lt 24)  { return "$([int]$diff.TotalHours)h ago"   }
    if ($diff.TotalDays    -lt 30)  { return "$([int]$diff.TotalDays)d ago"    }
    if ($diff.TotalDays    -lt 365) { return "$([int]($diff.TotalDays/30))mo ago" }
    return "$([int]($diff.TotalDays/365))y ago"
}

function Get-StatusPath([string]$line) {
    if (-not $line -or $line.Length -lt 4) { return "" }
    $path = $line.Substring(3).Trim()
    if ($path -match " -> ") { $path = ($path -split " -> ")[-1] }
    return ($path -replace "\\", "/")
}

function Test-EnvironmentPath([string]$path) {
    return (
        $path -match "(^|/)\.vscode/settings\.json$" -or
        $path -match "(^|/)\.pytest_cache(/|$)" -or
        $path -match "(^|/)__pycache__(/|$)" -or
        $path -match "\.py[co]$" -or
        $path -match "(^|/)node_modules(/|$)" -or
        $path -match "(^|/)\.venv(/|$)"
    )
}

function Get-DirtyCounts([string]$fullPath) {
    $statusLines = @(git -C $fullPath status --porcelain 2>$null | Where-Object { $_ -ne "" })
    $envCount = 0; $workCount = 0
    foreach ($line in $statusLines) {
        $path = Get-StatusPath $line
        if (Test-EnvironmentPath $path) { $envCount++ } else { $workCount++ }
    }
    [PSCustomObject]@{ Total = $statusLines.Count; Work = $workCount; Env = $envCount }
}

function Show-ProjectRow($project, [string]$color) {
    $fullPath = Join-Path $Root $project.path
    $name     = $project.name

    if (-not $project.path -or -not (Test-Path $fullPath)) {
        if (-not $DirtyOnly) {
            $status = if (-not $project.path) { "no path (planned)" } else { "path not found: $($project.path)" }
            Write-Host ("  {0,-28} " -f $name) -NoNewline -ForegroundColor DarkGray
            Write-Host $status -ForegroundColor DarkGray
        }
        return $false
    }

    $hasGit = Test-Path (Join-Path $fullPath ".git")
    if (-not $hasGit) {
        if (-not $DirtyOnly) {
            Write-Host ("  {0,-28} " -f $name) -NoNewline -ForegroundColor DarkGray
            Write-Host "no git" -ForegroundColor DarkGray
        }
        return $false
    }

    $branch      = (git -C $fullPath branch --show-current 2>$null) -join ""
    $dirtyCounts = Get-DirtyCounts $fullPath
    $isDirty     = $dirtyCounts.Total -gt 0

    if ($DirtyOnly -and -not $isDirty) { return $false }

    $logRaw  = git -C $fullPath log -1 --format="%h|%s|%ci" 2>$null
    $hash    = ""; $msg = ""; $timeStr = ""
    if ($logRaw) {
        $parts   = $logRaw -split "\|", 3
        $hash    = $parts[0]
        $msg     = if ($parts[1].Length -gt 38) { $parts[1].Substring(0,35) + "..." } else { $parts[1] }
        try { $timeStr = Get-RelativeTime([datetime]::Parse($parts[2])) } catch {}
    }

    $upstream    = git -C $fullPath rev-parse --abbrev-ref "@{upstream}" 2>$null
    $aheadBehind = ""
    if ($upstream) {
        $ahead  = git -C $fullPath rev-list "@{upstream}..HEAD" --count 2>$null
        $behind = git -C $fullPath rev-list "HEAD..@{upstream}" --count 2>$null
        if ($ahead  -and [int]$ahead  -gt 0) { $aheadBehind += "+$ahead"  }
        if ($behind -and [int]$behind -gt 0) { $aheadBehind += "-$behind" }
    }

    Write-Host ("  {0,-28} " -f $name) -NoNewline -ForegroundColor $color
    Write-Host ("{0,-10} " -f $branch)  -NoNewline -ForegroundColor DarkCyan

    if ($dirtyCounts.Work -gt 0 -and $dirtyCounts.Env -gt 0) {
        Write-Host ("● {0} work + {1} env  " -f $dirtyCounts.Work, $dirtyCounts.Env) -NoNewline -ForegroundColor Red
    } elseif ($dirtyCounts.Work -gt 0) {
        Write-Host ("● {0,-3} work   " -f $dirtyCounts.Work) -NoNewline -ForegroundColor Red
    } elseif ($dirtyCounts.Env -gt 0) {
        Write-Host ("◇ {0,-3} env    " -f $dirtyCounts.Env) -NoNewline -ForegroundColor DarkYellow
    } else {
        Write-Host "✓ clean     " -NoNewline -ForegroundColor DarkGreen
    }

    if ($aheadBehind) {
        Write-Host ("{0,-6} " -f $aheadBehind) -NoNewline -ForegroundColor DarkYellow
    } else {
        Write-Host "       " -NoNewline
    }

    if ($hash) {
        Write-Host "$hash  " -NoNewline -ForegroundColor DarkGray
        Write-Host ("{0,-42} " -f $msg) -NoNewline -ForegroundColor Gray
        Write-Host $timeStr -ForegroundColor DarkGray
    } else {
        Write-Host "(no commits)" -ForegroundColor DarkGray
    }

    if ($isDirty -and $dirtyCounts.Work -gt 0) { $script:totalWorkDirty++ } elseif ($isDirty) { $script:totalEnvOnly++ }
    return $isDirty
}

# ── Load registry ─────────────────────────────────────────────────────────────
$allProjects = Read-Projects $YamlFile

if (-not $allProjects) {
    Write-Host "Could not parse $YamlFile" -ForegroundColor Red
    exit 1
}

# ── Validate group filter ─────────────────────────────────────────────────────
if ($Group -and -not $GroupMeta.ContainsKey($Group)) {
    Write-Host "Unknown group '$Group'. Valid: $($GroupOrder -join ', ')" -ForegroundColor Red
    exit 1
}

$scanGroups = if ($Group) { @($Group) } else { $GroupOrder | Where-Object { $_ -ne "planned" } }

# ── Header ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  governance-commons  " -ForegroundColor White -BackgroundColor DarkBlue -NoNewline
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  " -ForegroundColor DarkBlue
Write-Host ""

$totalRepos = 0
$totalDirty = 0
$totalWorkDirty = 0
$totalEnvOnly = 0

foreach ($key in $scanGroups) {
    $meta     = $GroupMeta[$key]
    $projects = $allProjects | Where-Object { $_.group -eq $key }
    if (-not $projects) { continue }

    if ($DirtyOnly) {
        $hasAnyDirty = $false
        foreach ($p in $projects) {
            if (-not $p.path) { continue }
            $fp = Join-Path $Root $p.path
            if (Test-Path (Join-Path $fp ".git")) {
                $dc = Get-DirtyCounts $fp
                if ($dc.Total -gt 0) { $hasAnyDirty = $true; break }
            }
        }
        if (-not $hasAnyDirty) { continue }
    }

    $bar = "─" * ([Math]::Max(2, 50 - $meta.Label.Length))
    Write-Host "  $($meta.Label) $bar" -ForegroundColor $meta.Color
    Write-Host ""

    foreach ($p in $projects) {
        if ($p.path -and (Test-Path (Join-Path $Root $p.path ".git"))) { $totalRepos++ }
        $wasDirty = Show-ProjectRow $p $meta.Color
        if ($wasDirty) { $totalDirty++ }
    }
    Write-Host ""
}

# ── Planned summary ───────────────────────────────────────────────────────────
if (-not $Group) {
    $plannedProjects = $allProjects | Where-Object { $_.group -eq "planned" -or $_.status -eq "planned" }
    if ($plannedProjects) {
        $names = ($plannedProjects | Select-Object -ExpandProperty name) -join ", "
        Write-Host "  PLANNED (aspirational, no repos yet) — $names" -ForegroundColor DarkGray
        Write-Host ""
    }
}

# ── Summary ───────────────────────────────────────────────────────────────────
$dirtyColor = if ($totalDirty -gt 0) { "Yellow" } else { "Green" }
Write-Host "  ── $totalRepos repos  │  " -NoNewline -ForegroundColor DarkGray
Write-Host "$totalDirty dirty" -NoNewline -ForegroundColor $dirtyColor
Write-Host " ($totalWorkDirty work, $totalEnvOnly env-only)" -NoNewline -ForegroundColor DarkGray
Write-Host "  │  source: projects.yaml  ──" -ForegroundColor DarkGray
Write-Host ""
