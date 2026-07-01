<#
.SYNOPSIS
    Shows git status for all projects listed in projects.yaml.

.PARAMETER Group
    Filter to a specific project group from projects.yaml.

.PARAMETER DirtyOnly
    Show only repos with uncommitted changes.

.PARAMETER Help
    Show help and exit.

.EXAMPLE
    .\dev-status.ps1
    .\dev-status.ps1 -DirtyOnly
    .\dev-status.ps1 -Group apps
    .\dev-status.ps1 -Group archive
    .\dev-status.ps1 -Help
#>
param(
    [string] $Group     = "",
    [string] $TargetPath = ".",
    [switch] $DirtyOnly,
    [switch] $Help
)

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)

if ($Help) {
    Write-Host ""
    Write-Host "  dev-status.ps1 — DevX Control Plane portfolio dashboard" -ForegroundColor White
    Write-Host ""
    Write-Host "  USAGE" -ForegroundColor Cyan
    Write-Host "    .\dev-status.ps1 [flags]"
    Write-Host ""
    Write-Host "  FLAGS" -ForegroundColor Cyan
    Write-Host "    -Group <name>    Filter to one group (see groups below)"
    Write-Host "    -DirtyOnly       Show only repos with uncommitted changes"
    Write-Host "    -Help            Show this help"
    Write-Host ""
    Write-Host "  GROUPS" -ForegroundColor Cyan
    if (Test-Path (Join-Path $Root "projects.yaml")) {
        $helpYaml = Get-Content (Join-Path $Root "projects.yaml") -Raw
        $helpGroups = [regex]::Matches($helpYaml, '(?m)^\s+group:\s+(.+)$') |
            ForEach-Object { $_.Groups[1].Value.Trim().Trim('"').Trim("'") } |
            Where-Object { $_ } |
            Select-Object -Unique
        Write-Host "    $($helpGroups -join '    ')"
    } else {
        Write-Host "    Defined by projects.yaml"
    }
    Write-Host ""
    Write-Host "  COLUMNS" -ForegroundColor Cyan
    Write-Host "    name        Project name (from projects.yaml)"
    Write-Host "    status      active | wip | scaffold | stable  (project lifecycle)"
    Write-Host "    branch      Current git branch"
    Write-Host "    dirty       ✓ clean | ● N work | ◇ N env  (working tree state)"
    Write-Host "    plan        plan = file-based docs  notes = notes-only  blank = none"
    Write-Host "    +N/-N       Commits ahead/behind upstream"
    Write-Host "    hash        Last commit short hash"
    Write-Host "    msg         Last commit message (truncated)"
    Write-Host "    time        Time since last commit"
    Write-Host ""
    Write-Host "  RELATED TOOLS" -ForegroundColor Cyan
    Write-Host "    .\validate-pointers.ps1     Verify all planning pointers resolve on disk"
    Write-Host "    .\protect-sources.ps1       Run source corpus integrity check manually"
    Write-Host ""
    Write-Host "  DOCS" -ForegroundColor Cyan
    Write-Host "    README.md                   Portfolio overview and quick start"
    Write-Host "    DEV-CONTROL-PLANE.md        Boundary doctrine — what lives where"
    Write-Host "    docs/planning-normalization.md  Planning standard and vocabulary"
    Write-Host ""
    exit 0
}

# ── Parse projects.yaml (no external module needed) ──────────────────────────
function Read-Projects([string]$yamlPath) {
    $content = Get-Content $yamlPath -Raw
    # Split on list items: lines starting with "  - name:"
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

$YamlFile = Join-Path $Root "projects.yaml"
$RawYaml  = Get-Content $YamlFile -Raw
$RootDisplay = try { (Resolve-Path $Root).Path } catch { $Root }

# ── Group display config ──────────────────────────────────────────────────────
$GroupMeta = @{
    "control-plane" = @{ Label = "CONTROL PLANE"; Color = "Green"   }
    "apps"          = @{ Label = "APPS";          Color = "Blue"    }
    "libraries"     = @{ Label = "LIBRARIES";     Color = "Cyan"    }
    "services"      = @{ Label = "SERVICES";      Color = "Yellow"  }
    "dev-tools"     = @{ Label = "DEV TOOLS";     Color = "Magenta" }
    "docs"          = @{ Label = "DOCS";          Color = "DarkCyan"}
    "archive"       = @{ Label = "ARCHIVES";      Color = "DarkGray"}
}
$FallbackColors = @("Green", "Cyan", "Yellow", "Magenta", "Blue", "DarkCyan", "Gray")

# ── Helpers ──────────────────────────────────────────────────────────────────
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

function Test-EnvironmentStatusPath([string]$path) {
    return (
        $path -eq ".vscode/settings.json" -or
        $path -eq ".vscode/" -or
        $path -match "(^|/)\.vscode/settings\.json$" -or
        $path -match "(^|/)\.pytest_cache(/|$)" -or
        $path -match "(^|/)__pycache__(/|$)" -or
        $path -match "\.py[co]$"
    )
}

function Get-DirtyCounts([string]$fullPath) {
    $statusLines = @(git -C $fullPath status --porcelain 2>$null | Where-Object { $_ -ne "" })
    $envCount = 0
    $workCount = 0

    foreach ($line in $statusLines) {
        $path = Get-StatusPath $line
        if (Test-EnvironmentStatusPath $path) {
            $envCount++
        } else {
            $workCount++
        }
    }

    [PSCustomObject]@{
        Total = $statusLines.Count
        Work  = $workCount
        Env   = $envCount
    }
}

function Get-PlanHealth([string]$projectName) {
    $fileKeys = 'canonical|path|tracks|roadmap|implementation_plan|domain_plan|project|changelog|alternate_status|onboarding'
    $blocks   = [regex]::Split($RawYaml, '(?m)^  - (?=name:)')
    $block    = $blocks | Where-Object { $_ -match "^name:\s+[`"']?$([regex]::Escape($projectName))[`"']?" } | Select-Object -First 1
    if (-not $block -or $block -notmatch 'planning:') { return "none" }
    # Extract only the planning sub-block (lines indented 6+ spaces under planning:)
    $planMatch = [regex]::Match($block, '(?ms)^\s{4}planning:\s*\n((?:\s{6,}[^\n]*\n?)*)')
    if (-not $planMatch.Success) { return "none" }
    $planBlock = $planMatch.Groups[1].Value
    if ($planBlock -match "(?m)^\s+($fileKeys):\s+\S") { return "plan" }
    return "notes"
}

function Show-ProjectRow($project, [string]$color, [bool]$CountTotals = $true) {
    $fullPath = Join-Path $Root $project.path
    $name     = $project.name

    $statusLabel = $project.status
    $statusColor = switch ($project.status) {
        "active"   { "Green"    }
        "stable"   { "Cyan"     }
        "wip"      { "Yellow"   }
        "scaffold" { "DarkGray" }
        default    { "DarkGray" }
    }

    if (-not (Test-Path $fullPath)) {
        if (-not $DirtyOnly) {
            Write-Host ("  {0,-24} " -f $name) -NoNewline -ForegroundColor DarkGray
            Write-Host ("{0,-8} " -f $statusLabel) -NoNewline -ForegroundColor $statusColor
            Write-Host "path not found: $($project.path)" -ForegroundColor DarkRed
        }
        return $false
    }

    $hasGit = Test-Path (Join-Path $fullPath ".git")
    if (-not $hasGit) {
        if (-not $DirtyOnly) {
            Write-Host ("  {0,-24} " -f $name) -NoNewline -ForegroundColor DarkGray
            Write-Host ("{0,-8} " -f $statusLabel) -NoNewline -ForegroundColor $statusColor
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

    $planHealth = Get-PlanHealth $name

    Write-Host ("  {0,-24} " -f $name) -NoNewline -ForegroundColor $color
    Write-Host ("{0,-8} " -f $statusLabel) -NoNewline -ForegroundColor $statusColor
    Write-Host ("{0,-10} " -f $branch) -NoNewline -ForegroundColor DarkCyan

    if ($dirtyCounts.Work -gt 0 -and $dirtyCounts.Env -gt 0) {
        Write-Host ("● {0} work + {1} env  " -f $dirtyCounts.Work, $dirtyCounts.Env) -NoNewline -ForegroundColor Red
    } elseif ($dirtyCounts.Work -gt 0) {
        Write-Host ("● {0,-3} work   " -f $dirtyCounts.Work) -NoNewline -ForegroundColor Red
    } elseif ($dirtyCounts.Env -gt 0) {
        Write-Host ("◇ {0,-3} env    " -f $dirtyCounts.Env) -NoNewline -ForegroundColor DarkYellow
    } else {
        Write-Host "✓ clean     " -NoNewline -ForegroundColor DarkGreen
    }

    switch ($planHealth) {
        "plan"  { Write-Host "plan  " -NoNewline -ForegroundColor DarkGreen  }
        "notes" { Write-Host "notes " -NoNewline -ForegroundColor DarkYellow }
        default { Write-Host "      " -NoNewline                              }
    }

    if ($aheadBehind) {
        Write-Host ("{0,-6} " -f $aheadBehind) -NoNewline -ForegroundColor DarkYellow
    } else {
        Write-Host "       " -NoNewline
    }

    if ($hash) {
        Write-Host "$hash  " -NoNewline -ForegroundColor DarkGray
        Write-Host ("{0,-36} " -f $msg) -NoNewline -ForegroundColor Gray
        Write-Host $timeStr -ForegroundColor DarkGray
    } else {
        Write-Host "(no commits)" -ForegroundColor DarkGray
    }

    if ($CountTotals -and $isDirty) {
        if ($dirtyCounts.Work -gt 0) { $script:totalWorkDirty++ } else { $script:totalEnvOnly++ }
    }

    return $isDirty
}

# ── Load registry ─────────────────────────────────────────────────────────────
$allProjects = Read-Projects $YamlFile

if (-not $allProjects) {
    Write-Host "Could not parse $YamlFile" -ForegroundColor Red
    exit 1
}

$GroupOrder = @(
    $allProjects |
        ForEach-Object { $_.group } |
        Where-Object { $_ } |
        Select-Object -Unique |
        Where-Object { $_ -ne "archive" }
)
if ($allProjects | Where-Object { $_.group -eq "archive" }) {
    $GroupOrder += "archive"
}

$colorIndex = 0
foreach ($groupName in $GroupOrder) {
    if (-not $GroupMeta.ContainsKey($groupName)) {
        $label = ($groupName -replace "[-_]", " ").ToUpperInvariant()
        $GroupMeta[$groupName] = @{
            Label = $label
            Color = $FallbackColors[$colorIndex % $FallbackColors.Count]
        }
        $colorIndex++
    }
}

# ── Validate group filter ─────────────────────────────────────────────────────
if ($Group -and -not $GroupMeta.ContainsKey($Group)) {
    Write-Host "Unknown group '$Group'. Valid: $($GroupOrder -join ', ')" -ForegroundColor Red
    exit 1
}

$scanGroups = if ($Group) { @($Group) } else { $GroupOrder | Where-Object { $_ -ne "archive" } }

# ── Header ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  $RootDisplay  " -ForegroundColor White -BackgroundColor DarkGreen -NoNewline
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  " -ForegroundColor DarkGreen
Write-Host ""

$totalRepos = 0
$totalDirty = 0
$totalWorkDirty = 0
$totalEnvOnly = 0

foreach ($key in $scanGroups) {
    $meta     = $GroupMeta[$key]
    $projects = $allProjects | Where-Object { $_.group -eq $key }
    if (-not $projects) { continue }

    # Skip group header in DirtyOnly mode if nothing in group is dirty
    if ($DirtyOnly) {
        $hasAnyDirty = $false
        foreach ($p in $projects) {
            $fp = Join-Path $Root $p.path
            if (Test-Path (Join-Path $fp ".git")) {
                $dirtyCounts = Get-DirtyCounts $fp
                if ($dirtyCounts.Total -gt 0) { $hasAnyDirty = $true; break }
            }
        }
        if (-not $hasAnyDirty) { continue }
    }

    $bar = "─" * ([Math]::Max(2, 50 - $meta.Label.Length))
    Write-Host "  $($meta.Label) $bar" -ForegroundColor $meta.Color
    Write-Host ""

    foreach ($p in $projects) {
        $fp = Join-Path $Root $p.path
        if (Test-Path (Join-Path $fp ".git")) { $totalRepos++ }
        $wasDirty = Show-ProjectRow $p $meta.Color
        if ($wasDirty) { $totalDirty++ }
    }
    Write-Host ""
}

# ── Archive summary or detail ─────────────────────────────────────────────────
$archiveProjects = $allProjects | Where-Object { $_.group -eq "archive" }
$archiveDirty    = 0
foreach ($p in $archiveProjects) {
    $fp = Join-Path $Root $p.path
    if (Test-Path (Join-Path $fp ".git")) {
        $totalRepos++
        $dirtyCounts = Get-DirtyCounts $fp
        if ($dirtyCounts.Total -gt 0) {
            $archiveDirty++
            $totalDirty++
            if ($dirtyCounts.Work -gt 0) { $totalWorkDirty++ } else { $totalEnvOnly++ }
        }
    }
}

if ($Group -eq "archive") {
    $meta = $GroupMeta["archive"]
    $bar  = "─" * ([Math]::Max(2, 50 - $meta.Label.Length))
    Write-Host "  $($meta.Label) $bar" -ForegroundColor $meta.Color
    Write-Host ""
    foreach ($p in $archiveProjects) { Show-ProjectRow $p $meta.Color $false | Out-Null }
    Write-Host ""
} elseif (-not $Group) {
    $archiveNote = if ($archiveDirty -gt 0) { "($archiveDirty dirty) — run -Group archive to inspect" } else { "all clean" }
    Write-Host "  ARCHIVES — $archiveNote" -ForegroundColor DarkGray
    Write-Host ""
}

# ── Summary ───────────────────────────────────────────────────────────────────
$dirtyColor = if ($totalDirty -gt 0) { "Yellow" } else { "Green" }
Write-Host "  ── $totalRepos repos  │  " -NoNewline -ForegroundColor DarkGray
Write-Host "$totalDirty dirty" -NoNewline -ForegroundColor $dirtyColor
Write-Host " ($totalWorkDirty work, $totalEnvOnly env-only)" -NoNewline -ForegroundColor DarkGray
Write-Host "  │  source: projects.yaml  ──" -ForegroundColor DarkGray
Write-Host ""
