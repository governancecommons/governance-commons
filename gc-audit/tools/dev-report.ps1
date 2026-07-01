# dev-report.ps1 — Portfolio Planning Status Report
# Standard: GC:2008 / DEV-ACCORD.00

param(
    [string]$Project  = "",      # Scope to one project (e.g. "eco", "governance-commons")
    [string]$TargetPath = ".",   # Portfolio root to scan
    [switch]$GapOnly,            # Show gap analysis table only
    [switch]$DetailOnly,         # Show per-project detail blocks only
    [string]$Output   = "",      # Write report to file path
    [switch]$Help
)

if ($Help) {
    @"
dev-report.ps1  Portfolio Planning Status Report
Standard: GC:2008 / DEV-ACCORD.00

Usage:
  .\dev-report.ps1                      Full report (gap table + per-project detail)
  .\dev-report.ps1 -GapOnly             Gap analysis table only
  .\dev-report.ps1 -DetailOnly          Per-project detail only
  .\dev-report.ps1 -Project eco         Single project
  .\dev-report.ps1 -Output report.md    Write to file

Output columns (gap table):
  PROJECT   — folder name
  STATUS    — from DEV-PLAN header (first 36 chars)
  AL        — authority level
  DONE/TOT  — work items done / total (from structured tables)
  PCT       — % complete (— when no structured work items found)
  PHASE     — current phase or active PASS/milestone

Detail block fields:
  Status     — header Status value
  Authority  — AL:N
  Phase      — active phase / milestone
  Items      — done/total breakdown: active, blocked, planned
  Next step  — highest-priority non-done work item
  Next block — first unchecked admission criterion or explicit blocker
"@
    exit 0
}

$Root = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)

# ─── Helpers ─────────────────────────────────────────────────────────────────

function Format-Md([string]$s) {
    ($s `
        -replace '\[([^\]]+)\]\([^)]+\)', '$1' `
        -replace '\*\*([^*]+)\*\*', '$1' `
        -replace '\*([^*]+)\*', '$1' `
        -replace '`([^`]*)`', '$1' `
        -replace '[✅⬜🔵⭕🔴🟡🟢]', '' `
        -replace '\s{2,}', ' '
    ).Trim()
}

function Find-ColIdx([string[]]$headers, [string]$pattern) {
    for ($i = 0; $i -lt $headers.Count; $i++) {
        if ($headers[$i] -match $pattern) { return $i }
    }
    return $null
}

function Get-RowStatus([string]$fullRow, [string[]]$cells, $statusIdx, $prioIdx) {
    # Priority 1: emoji in row
    if ($fullRow -match '✅') { return 'done' }
    if ($fullRow -match '⬜') { return 'planned' }
    if ($fullRow -match '🔵') { return 'active' }
    # Priority 2: status column text
    if ($null -ne $statusIdx -and $statusIdx -lt $cells.Count) {
        $sv = $cells[$statusIdx].ToLower().Trim()
        if ($sv -match '^done$|^complete$|^shipped$|^released$|spec-complete|release-complete') { return 'done' }
        if ($sv -match '^active$|in[ -]progress')                                               { return 'active' }
        if ($sv -match 'blocked')                                                               { return 'blocked' }
        if ($sv -match '^planned$|^queued$|^open$|^todo$|^not.started$')                       { return 'planned' }
    }
    # Priority 3: priority column as status proxy (P0/P1/P2 means it exists and is planned)
    if ($null -ne $prioIdx -and $prioIdx -lt $cells.Count) {
        if ($cells[$prioIdx] -match '^P[0-9]$|^P[0-9]\s|^High$|^Medium$|^Low$') { return 'planned' }
    }
    return 'skip'
}

# First-column headers that signal registry/metadata tables (not work items)
$script:ExcludeFirst = '^(pass|version|date|state|decision|format|question|q|area|artifact|component|layer|type|surface|release|gap|batch|phase|separator|rule|constraint|symbol|token|tier|scope|id name)$'

function Get-WorkItems([string]$content) {
    $rows  = [System.Collections.Generic.List[object]]::new()
    $lines = $content -split '\r?\n'
    $i     = 0

    while ($i -lt $lines.Count - 2) {
        $line = $lines[$i]
        # Detect table header row followed by separator row
        if ($line -match '^\s*\|.+\|$' -and $lines[$i + 1] -match '^\s*\|[\s\-|:]+\|$') {
            $rawHdrs = $line -split '\|' | Select-Object -Skip 1 | Select-Object -SkipLast 1 | ForEach-Object { $_.Trim() }
            $headers = @($rawHdrs | ForEach-Object { $_.ToLower() })
            $firstH  = if ($headers.Count -gt 0) { $headers[0] } else { '' }

            $workIdx   = Find-ColIdx $headers 'work|task|goal|item|description'
            $statusIdx = Find-ColIdx $headers '^status$|^state$'
            $prioIdx   = Find-ColIdx $headers 'priority'

            # Include only tables with a description column AND (status OR priority column)
            $isWork = (
                $firstH -notmatch $script:ExcludeFirst -and
                $headers.Count -ge 2 -and
                $null -ne $workIdx -and
                ($null -ne $statusIdx -or $null -ne $prioIdx)
            )

            if ($isWork) {
                $j = $i + 2
                while ($j -lt $lines.Count -and $lines[$j] -match '^\s*\|.+\|$') {
                    $cells = @($lines[$j] -split '\|' | Select-Object -Skip 1 | Select-Object -SkipLast 1 | ForEach-Object { $_.Trim() })
                    $st    = Get-RowStatus $lines[$j] $cells $statusIdx $prioIdx
                    if ($st -ne 'skip') {
                        $work = if ($null -ne $workIdx -and $workIdx -lt $cells.Count) { Format-Md $cells[$workIdx] } else { '' }
                        $prio = if ($null -ne $prioIdx -and $prioIdx -lt $cells.Count) { $cells[$prioIdx] } else { '' }
                        $rows.Add([pscustomobject]@{ Status = $st; Work = $work; Priority = $prio })
                    }
                    $j++
                }
                $i = $j
                continue
            }
        }
        $i++
    }
    return $rows.ToArray()
}

function Get-Phase([string]$content) {
    # Explicit phase/milestone fields (common patterns across portfolio)
    $checks = @(
        '(?m)^\*\*Active [Pp]hase:\*\*\s*(.+)$',
        '(?m)^\*\*Current [Pp]hase:\*\*\s*(.+)$',
        '(?m)^\*\*Active PASS:\*\*\s*(.+)$',
        '(?m)^\*\*Next milestone:\*\*\s*(.+)$',
        '(?m)^\*\*Current [Vv]ersion:\*\*\s*(.+)$',
        '(?m)^\*\*Current [Pp]osition:\*\*\s*(.+)$'
    )
    foreach ($pat in $checks) {
        if ($content -match $pat) { return Format-Md $Matches[1] }
    }
    # Section-based fallback: only if first line under section is ≤ 60 chars (a phase name, not description prose)
    if ($content -match '(?s)## (?:Current Phase|CURRENT PHASE)[^\n]*\n\n([^\n]{5,60})\n') {
        return Format-Md $Matches[1]
    }
    return ''
}

function Get-NextStep([string]$content, [object[]]$items) {
    # From structured items: first non-done, P0 > P1 > active > planned
    if ($items -and $items.Count -gt 0) {
        $todo = $items | Where-Object { $_.Status -in 'active', 'planned' }
        if ($todo) {
            $next = $todo | Sort-Object {
                $pr = $_.Priority
                if ($pr -match 'P0') { 0 } elseif ($pr -match 'P1') { 1 } elseif ($pr -match 'P2') { 2 } else { 5 }
            }, { if ($_.Status -eq 'active') { 0 } else { 1 } } | Select-Object -First 1
            if ($next -and $next.Work) { return $next.Work }
        }
    }
    # Prose fallback: first bullet under "Immediate priorities:", "Next Work:", "Active:"
    $prosePats = @(
        '(?s)(?:Immediate priorities?|Next Work|Priority Work|Active work|Queue)[^\n]*:\s*\n+((?:\s*[-*]\s+[^\n]+\n){1,5})',
        '(?s)\*\*Next step:\*\*\s*([^\n]+)',
        '(?s)\*\*Next milestone:\*\*\s*([^\n]+)'
    )
    foreach ($pat in $prosePats) {
        if ($content -match $pat) {
            $val = $Matches[1] -split '\n' | Where-Object { $_ -match '^\s*[-*]' } | Select-Object -First 1
            if (-not $val) { $val = $Matches[1] }
            $cleaned = Format-Md ($val -replace '^\s*[-*]\s+', '')
            if ($cleaned.Length -gt 5) { return $cleaned }
        }
    }
    return ''
}

function Get-Blockers([string]$releaseContent, [string]$planContent) {
    $found = [System.Collections.Generic.List[string]]::new()
    # Unchecked checklist items (admission criteria, acceptance gates)
    foreach ($text in @($releaseContent, $planContent)) {
        foreach ($line in ($text -split '\r?\n')) {
            if ($line -match '^\s*-\s*\[\s+\]\s*(.+)') {
                $v = Format-Md $Matches[1]
                if ($v -and -not $found.Contains($v)) { $found.Add($v) }
            }
        }
        if ($found.Count -ge 3) { break }
    }
    # Explicit blocker keywords (only if no checklist blockers)
    if ($found.Count -eq 0) {
        $blockerPat = '(?i)(?:\*\*Blocker[s]?:\*\*|blocked on|gated on|waiting on|requires?)[:\s]+(.{10,80})'
        foreach ($text in @($releaseContent, $planContent)) {
            foreach ($line in ($text -split '\r?\n')) {
                if ($line -match $blockerPat) {
                    $v = Format-Md $Matches[1]
                    if ($v -and -not $found.Contains($v)) { $found.Add($v) }
                }
            }
            if ($found.Count -ge 2) { break }
        }
    }
    return $found | Select-Object -Unique -First 2
}

# ─── Per-project analysis ────────────────────────────────────────────────────

function Get-ProjectData([string]$planPath) {
    $dir  = Split-Path $planPath -Parent
    $name = if ($dir -eq $Root) { 'dev (root)' } else { Split-Path $dir -Leaf }
    $rel  = $dir.Replace("$Root\", '').Replace($Root, '(root)')

    $p = [ordered]@{
        Name      = $name;  RelPath   = $rel
        Status    = '';     AL        = '';     Phase     = ''
        Done      = 0;      Active    = 0;      Blocked   = 0;     Planned   = 0;   Total = 0
        Pct       = '—';    NextStep  = '';     NextBlock = ''
    }

    $plan    = Get-Content $planPath -Raw -Encoding UTF8
    $head15  = ($plan -split '\r?\n' | Select-Object -First 15) -join "`n"
    $relPath = Join-Path $dir 'DEV-RELEASE.md'
    $release = if (Test-Path $relPath) { Get-Content $relPath -Raw -Encoding UTF8 } else { '' }

    # Header fields
    if ($head15 -match '\*\*Status:\*\*\s*(.+)') {
        $s = Format-Md $Matches[1]; $p.Status = if ($s.Length -gt 36) { $s.Substring(0, 33) + '...' } else { $s }
    }
    if ($head15 -match 'AL:(\d)') { $p.AL = "AL:$($Matches[1])" }

    # Phase
    $ph = Get-Phase $plan
    $p.Phase = if ($ph.Length -gt 55) { $ph.Substring(0, 52) + '...' } else { $ph }

    # Work items (structured tables)
    $items = Get-WorkItems $plan
    foreach ($it in $items) {
        switch ($it.Status) {
            'done'    { $p.Done++ }
            'active'  { $p.Active++ }
            'blocked' { $p.Blocked++ }
            default   { $p.Planned++ }
        }
    }
    $p.Total = $p.Done + $p.Active + $p.Blocked + $p.Planned
    if ($p.Total -gt 0) { $p.Pct = "$([int](($p.Done / $p.Total) * 100))%" }

    # Next step
    $ns = Get-NextStep $plan $items
    $p.NextStep = if ($ns.Length -gt 65) { $ns.Substring(0, 62) + '...' } else { $ns }

    # Blockers: release admission criteria first, then plan
    $blk = Get-Blockers $release $plan
    if ($blk.Count -eq 0 -and $p.Blocked -gt 0) {
        $bi = $items | Where-Object { $_.Status -eq 'blocked' } | Select-Object -First 1
        if ($bi -and $bi.Work) { $blk = @($bi.Work) }
    }
    if ($blk.Count -gt 0) {
        $nb = $blk[0]; $p.NextBlock = if ($nb.Length -gt 70) { $nb.Substring(0, 67) + '...' } else { $nb }
    }

    return [pscustomobject]$p
}

# ─── Discovery ───────────────────────────────────────────────────────────────

$scanRoot = if ($Project) { Join-Path $Root $Project } else { $Root }
if ($Project -and -not (Test-Path $scanRoot)) { Write-Error "Not found: $scanRoot"; exit 1 }

$planFiles = Get-ChildItem -Path $scanRoot -Recurse -File -Filter 'DEV-PLAN.md' | Where-Object {
    $_.Name -ceq 'DEV-PLAN.md' -and
    $_.FullName -notmatch '(?i)(archive|_archive|lasso_archive|lasso-mvp_archive)' -and
    $_.FullName -notmatch '[\\/]\.eco[\\/]' -and
    $_.FullName -notmatch '(?i)state-snapshot'
} | Sort-Object FullName

$projects = @($planFiles | ForEach-Object { Get-ProjectData $_.FullName })

# ─── Render ──────────────────────────────────────────────────────────────────

$buf = [System.Collections.Generic.List[string]]::new()
function L([string]$s = '') { $buf.Add($s) }

L ''
L '  DEV PORTFOLIO STATUS REPORT'
L '  Standard: GC:2008 / DEV-ACCORD.00'
L "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  $Root"
L ''

# ── Gap analysis table ────────────────────────────────────────────────────────

if (-not $DetailOnly) {
    $C1 = 30; $C2 = 24; $C3 = 7; $C4 = 9; $C5 = 6

    function Fit([string]$s, [int]$w) {
        if ($s.Length -gt $w) { $s.Substring(0, $w - 1) + '…' } else { $s.PadRight($w) }
    }

    L ('  ' + 'PROJECT'.PadRight($C1) + 'STATUS'.PadRight($C2) + 'AL'.PadRight($C3) + 'DONE/TOT'.PadRight($C4) + 'PCT'.PadRight($C5) + '  PHASE')
    L ('  ' + ('─' * ($C1 + $C2 + $C3 + $C4 + $C5 + 14)))

    foreach ($p in $projects) {
        $n  = Fit $p.Name $C1
        $sv = if ($p.Status) { $p.Status } else { '—' };         $s  = Fit $sv $C2
        $av = if ($p.AL)     { $p.AL     } else { '—' };         $al = Fit $av $C3
        $dv = if ($p.Total -gt 0) { "$($p.Done)/$($p.Total)" } else { '—' }; $dt = Fit $dv $C4
        L ('  ' + $n + $s + $al + $dt + $p.Pct.PadRight($C5) + '  ' + $p.Phase)
    }

    $tDone  = ($projects | ForEach-Object { [int]$_.Done    } | Measure-Object -Sum).Sum
    $tTotal = ($projects | ForEach-Object { [int]$_.Total   } | Measure-Object -Sum).Sum
    $tBlk   = ($projects | ForEach-Object { [int]$_.Blocked } | Measure-Object -Sum).Sum
    $tPct   = if ($tTotal -gt 0) { "$([int](($tDone / $tTotal) * 100))%" } else { '—' }

    L ('  ' + ('─' * ($C1 + $C2 + $C3 + $C4 + $C5 + 14)))
    L ("  $($projects.Count) projects │ $tDone/$tTotal structured items ($tPct) │ $tBlk blocked")
    L ''
}

# ── Per-project detail ────────────────────────────────────────────────────────

if (-not $GapOnly) {
    L '  ── PROJECT DETAIL ──────────────────────────────────────────────'
    L ''

    foreach ($p in $projects) {
        $bar = '─' * ([Math]::Max(2, 64 - $p.Name.Length))
        L "  ── $($p.Name) $bar"
        if ($p.Status)   { L "     Status:     $($p.Status)" }
        if ($p.AL)       { L "     Authority:  $($p.AL)" }
        if ($p.Phase)    { L "     Phase:      $($p.Phase)" }
        if ($p.Total -gt 0) {
            L "     Items:      $($p.Done)/$($p.Total) ($($p.Pct)) — $($p.Active) active  $($p.Blocked) blocked  $($p.Planned) planned"
        }
        if ($p.NextStep)  { L "     Next step:  $($p.NextStep)" }
        if ($p.NextBlock) { L "     Next block: $($p.NextBlock)" }
        L ''
    }
}

$report = $buf -join "`n"
Write-Host $report

if ($Output) {
    $report | Set-Content $Output -Encoding UTF8
    Write-Host "  Saved: $Output" -ForegroundColor Cyan
}
