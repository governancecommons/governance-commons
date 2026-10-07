<#
.SYNOPSIS
    Validates planning document conformance against DEV-ACCORD.00 (GC:2008).

.DESCRIPTION
    Checks all DEV-PATH, DEV-PLAN, DEV-RELEASE, and DEV-TRACKS files across the
    portfolio for conformance with the Planning Document Standard (DEV-ACCORD.00).

    ERRORS (exit code 1):
      E1 — H1 is not the first non-empty line
      E2 — H1 doc type is not a registered DEV-ACCORD type
      E3 — H1 separator is not em dash (U+2014)
      E4 — H1 project scope is empty
      E5 — Two or more docs of the same type share the same H1 (collision)

    WARNINGS (exit code 0; exit code 1 with -Strict):
      W1 — AUTHORITY LEVEL not declared within first 15 lines
      W2 — Status not declared within first 15 lines
      W3 — File named TRACKS.md found (canonical name is DEV-TRACKS.md per DEV-ACCORD-CI-5)

.PARAMETER Strict
    Treat warnings as errors (exit 1 if any warnings).

.PARAMETER Project
    Check only a named project path relative to TargetPath, e.g. "eco" or "governance-commons/ons".

.PARAMETER TargetPath
    Portfolio or repository root to scan (default current directory).

.PARAMETER Help
    Show help and exit.

.EXAMPLE
    .\validate-planning.ps1
    .\validate-planning.ps1 -Strict
    .\validate-planning.ps1 -Project eco
    .\validate-planning.ps1 -Project governance-commons/agent-dossier

.LINK
    Standard: governance-commons/passes/dev-accord/DEV-ACCORD.00.md (GC:2008)
#>
param(
    [switch] $Strict,
    [string] $Project = "",
    [string] $TargetPath = ".",
    [switch] $Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

$Root    = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($TargetPath)
$EmDash  = [char]0x2014   # — U+2014
$EnDash  = [char]0x2013   # – U+2013
$ValidTypes = @("DEV-PATH", "DEV-PLAN", "DEV-RELEASE", "DEV-TRACKS")

# ── Counters ──────────────────────────────────────────────────────────────────
$Errors   = 0
$Warnings = 0

# ── Result collectors ─────────────────────────────────────────────────────────
$AllDocs     = [System.Collections.Generic.List[hashtable]]::new()   # all docs with their parsed H1
$H1ByType    = @{}   # keyed by doc type, value = list of {H1, Path}

# ── Output helpers ────────────────────────────────────────────────────────────
function Write-Error-Finding([string]$code, [string]$path, [string]$msg) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  [ERROR $code]" -NoNewline -ForegroundColor Red
    Write-Host " $rel" -NoNewline -ForegroundColor White
    Write-Host " — $msg" -ForegroundColor DarkRed
    $script:Errors++
}

function Write-Warning-Finding([string]$code, [string]$path, [string]$msg) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  [WARN  $code]" -NoNewline -ForegroundColor DarkYellow
    Write-Host " $rel" -NoNewline -ForegroundColor White
    Write-Host " — $msg" -ForegroundColor DarkYellow
    $script:Warnings++
}

function Write-Pass-Finding([string]$path) {
    $rel = $path.Replace($Root + "\", "").Replace($Root + "/", "")
    Write-Host "  [PASS     ]" -NoNewline -ForegroundColor DarkGreen
    Write-Host " $rel" -ForegroundColor Gray
}

# ── File checker ──────────────────────────────────────────────────────────────
function Test-PlanningDoc([string]$filePath) {
    if (-not (Test-Path $filePath)) { return }

    $rel  = $filePath.Replace($Root + "\", "").Replace($Root + "/", "")
    $name = Split-Path $filePath -Leaf

    # W3 — TRACKS.md legacy name
    if ($name -eq "TRACKS.md") {
        Write-Warning-Finding "W3" $filePath "file named TRACKS.md — canonical name is DEV-TRACKS.md (DEV-ACCORD-CI-5)"
        return
    }

    # Only process registered doc types
    $typeFromName = [System.IO.Path]::GetFileNameWithoutExtension($name)
    if ($typeFromName -notin $ValidTypes) { return }

    $lines = Get-Content $filePath -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $lines) {
        Write-Error-Finding "E1" $filePath "file is empty"
        return
    }

    # Find first non-empty line
    $firstLine = $null
    $firstLineIdx = -1
    for ($i = 0; $i -lt [Math]::Min($lines.Count, 5); $i++) {
        if ($lines[$i].Trim() -ne "") {
            $firstLine = $lines[$i]
            $firstLineIdx = $i
            break
        }
    }

    if (-not $firstLine -or -not $firstLine.StartsWith("# ")) {
        $found = "<none>"
        if ($firstLine) {
            $found = $firstLine.Substring(0, [Math]::Min(60, $firstLine.Length))
        }
        Write-Error-Finding "E1" $filePath "H1 is not the first non-empty line (found: '$found')"
        return
    }

    # Parse H1: # {DOC-TYPE}{sep}{Scope}
    $h1Body = $firstLine.Substring(2)   # strip "# "

    # E3 — separator check (em dash required)
    $hasEmDash = $h1Body.Contains($EmDash)
    $hasHyphen = $h1Body -match "^[A-Z\-]+ - "
    $hasEnDash = $h1Body.Contains($EnDash)

    # E2 — doc type prefix
    $detectedType = $null
    foreach ($t in $ValidTypes) {
        if ($h1Body.StartsWith("$t $EmDash") -or $h1Body.StartsWith("$t$EmDash")) {
            $detectedType = $t
            break
        }
        # Also catch wrong-separator cases to give better error messages
        if ($h1Body.StartsWith("$t ") -or $h1Body.StartsWith($t)) {
            $detectedType = $t
            break
        }
    }

    $docHasErrors = $false

    if (-not $detectedType) {
        Write-Error-Finding "E2" $filePath "H1 doc type not recognized — expected one of: $($ValidTypes -join ', ') (H1: '$h1Body')"
        $docHasErrors = $true
    } elseif ($detectedType -ne $typeFromName) {
        Write-Error-Finding "E2" $filePath "H1 doc type '$detectedType' does not match filename '$name'"
        $docHasErrors = $true
    }

    if (-not $hasEmDash) {
        if ($hasHyphen) {
            Write-Error-Finding "E3" $filePath "H1 uses hyphen (-) as separator — must be em dash $($EmDash) (U+2014)"
        } elseif ($hasEnDash) {
            Write-Error-Finding "E3" $filePath "H1 uses en dash ($($EnDash)) as separator — must be em dash $($EmDash) (U+2014)"
        } else {
            Write-Error-Finding "E3" $filePath "H1 missing em dash separator $($EmDash) (U+2014)"
        }
        $docHasErrors = $true
    }

    # E4 — scope empty
    $scope = ""
    if ($hasEmDash -and $detectedType) {
        $afterType = $h1Body.Substring($detectedType.Length).TrimStart()
        if ($afterType.StartsWith($EmDash)) {
            $scope = $afterType.Substring(1).Trim()
        }
    }
    if ($hasEmDash -and $scope -eq "") {
        Write-Error-Finding "E4" $filePath "H1 project scope is empty after em dash"
        $docHasErrors = $true
    }

    # Collect for collision check (E5) even if other errors present
    if ($detectedType -and $hasEmDash -and $scope -ne "") {
        $h1Text = $firstLine.Trim()
        if (-not $H1ByType.ContainsKey($detectedType)) {
            $H1ByType[$detectedType] = [System.Collections.Generic.List[hashtable]]::new()
        }
        $H1ByType[$detectedType].Add(@{ H1 = $h1Text; Path = $filePath })
    }

    # Warnings — read up to 15 lines
    $head15 = $lines | Select-Object -First 15
    $head15Text = $head15 -join "`n"

    if ($head15Text -notmatch '\*\*AUTHORITY LEVEL: AL:\d') {
        Write-Warning-Finding "W1" $filePath "AUTHORITY LEVEL not declared in first 15 lines"
    }
    if ($head15Text -notmatch '\*\*[Ss]tatus[:\*]') {
        Write-Warning-Finding "W2" $filePath "Status not declared in first 15 lines"
    }

    if (-not $docHasErrors) {
        Write-Pass-Finding $filePath
    }
}

# ── Collect paths to scan ─────────────────────────────────────────────────────
$ScanPaths = [System.Collections.Generic.List[string]]::new()

# Always include root planning docs
foreach ($dt in $ValidTypes) {
    $ScanPaths.Add((Join-Path $Root "$dt.md"))
}
$ScanPaths.Add((Join-Path $Root "TRACKS.md"))   # W3 check for legacy name at root

if ($Project) {
    # Single project mode
    $projRoot = Join-Path $Root $Project
    if (-not (Test-Path $projRoot)) {
        Write-Host "Project path not found: $projRoot" -ForegroundColor Red
        exit 1
    }
    foreach ($dt in $ValidTypes) {
        $ScanPaths.Add((Join-Path $projRoot "$dt.md"))
    }
    $ScanPaths.Add((Join-Path $projRoot "TRACKS.md"))
} else {
    # Full portfolio scan — find all DEV-*.md and TRACKS.md up to 3 levels deep
    $ExcludePatterns = @("*_archive*", "*\.claude\worktrees*", "*node_modules*", "*\.venv*", "*dist\*", "*__pycache__*")

    $found = Get-ChildItem -Path $Root -Recurse -Depth 4 -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object {
            # Exact-case match — canonical names are uppercase DEV-*.md
            # This excludes lowercase redirect files like dev-path.md in .eco runtime folders
            ($_.Name -cmatch '^(DEV-PATH|DEV-PLAN|DEV-RELEASE|DEV-TRACKS)\.md$') -or
            ($_.Name -ceq 'TRACKS.md')
        } |
        Where-Object {
            # Exclude archive directories
            $_.FullName -notmatch '(?i)(archive|_archive|lasso_archive|lasso-mvp_archive|devtoolkit-legacy)' -and
            # Exclude git worktrees
            $_.FullName -notmatch '(?i)[\\/]\.claude[\\/]worktrees[\\/]' -and
            # Exclude runtime and preserved reconciliation artifacts; neither is an active planning owner.
            $_.FullName -notmatch '[\\/](\.eco|\.reconciliation)[\\/]' -and
            # Exclude state-snapshot directories
            $_.FullName -notmatch '(?i)state-snapshot' -and
            # Exclude node_modules, .venv, dist
            $_.FullName -notmatch '(?i)(node_modules|\.venv|[\\/]dist[\\/])'
        }

    foreach ($f in $found) {
        if (-not $ScanPaths.Contains($f.FullName)) {
            $ScanPaths.Add($f.FullName)
        }
    }
}

# A portfolio registry chooses active planning owners. Preserved copies remain
# inspectable through -Project; they must not compete with the declared owner.
$PlanningOwners = @{}
$RegistryProjects = @{}
$registryPath = Join-Path $Root "projects.yaml"
if (-not $Project -and (Test-Path -LiteralPath $registryPath)) {
    $current = $null
    $planning = $false
    foreach ($line in (Get-Content -LiteralPath $registryPath -Encoding UTF8)) {
        if ($line -match '^  - name:\s*(.+?)\s*$') {
            $current = @{ Name=$Matches[1].Trim('"', "'"); Path=""; Docs=@{} }
            $RegistryProjects[$current.Name] = $current
            $planning = $false
        } elseif ($current -and $line -match '^    path:\s*(.+?)\s*$') {
            $current.Path = $Matches[1].Trim('"', "'")
        } elseif ($current -and $line -match '^    planning:\s*$') {
            $planning = $true
        } elseif ($current -and $planning -and $line -match '^      (?:canonical|path|tracks|release):\s*(.+?)\s*$') {
            $pointer = $Matches[1].Trim('"', "'")
            $fileName = Split-Path $pointer -Leaf
            if ($fileName -cmatch '^DEV-(PATH|PLAN|RELEASE|TRACKS)\.md$') { $current.Docs[$fileName] = $pointer }
        } elseif ($line -match '^    \S') { $planning = $false }
    }
    foreach ($entry in $RegistryProjects.Values) {
        if (-not $entry.Path) { continue }
        foreach ($type in $ValidTypes) {
            $fileName = "$type.md"
            $explicit = $entry.Docs.ContainsKey($fileName)
            $pointer = if ($explicit) { $entry.Docs[$fileName] } else { Join-Path $entry.Path $fileName }
            $owner = [IO.Path]::GetFullPath((Join-Path $Root $pointer))
            if ($owner -match '(?i)([\\/]\.eco[\\/]|archive|state-snapshot)') { continue }
            $boundary = $Root.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
            if (-not $owner.StartsWith($boundary, [StringComparison]::OrdinalIgnoreCase)) {
                Write-Host "[ERROR] Planning pointer escapes portfolio: $pointer" -ForegroundColor Red; $Errors++; continue
            }
            if (-not (Test-Path -LiteralPath $owner -PathType Leaf)) {
                if ($explicit) { Write-Host "[ERROR] Missing registered planning owner: $pointer" -ForegroundColor Red; $Errors++ }
                continue
            }
            $PlanningOwners["$($entry.Path)|$fileName"] = $owner
            if (-not $ScanPaths.Contains($owner)) { $ScanPaths.Add($owner) }
        }
    }
}

function Get-DeclaredPlanningOwner([string]$file) {
    $relative = [IO.Path]::GetRelativePath($Root, $file).Replace('\', '/')
    $fileName = Split-Path $file -Leaf
    foreach ($entry in $RegistryProjects.Values) {
        if (-not $entry.Path) { continue }
        $projectPath = $entry.Path.Replace('\', '/').TrimEnd('/')
        $inProject = $relative.Equals("$projectPath/$fileName", [StringComparison]::OrdinalIgnoreCase) -or $relative.Equals("$projectPath/docs/$fileName", [StringComparison]::OrdinalIgnoreCase)
        $inPreservedCopy = $relative.StartsWith("dev-docs/$($entry.Name)/", [StringComparison]::OrdinalIgnoreCase)
        if ($inProject -or $inPreservedCopy) {
            $owner = $PlanningOwners["$($entry.Path)|$fileName"]
            if ($owner -and $owner -ne $file) { return $owner }
        }
    }
    return $null
}

# ── Run checks ────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  DEV-ACCORD CONFORMANCE CHECK — validate-planning.ps1" -ForegroundColor White
Write-Host "  Standard: GC:2008 / DEV-ACCORD.00" -ForegroundColor DarkGray
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')  $Root" -ForegroundColor DarkGray
Write-Host ""

$checkedFiles = [System.Collections.Generic.HashSet[string]]::new()

foreach ($path in $ScanPaths) {
    $resolved = Resolve-Path $path -ErrorAction SilentlyContinue
    if (-not $resolved) { continue }
    $canonical = $resolved.Path
    if (-not $checkedFiles.Add($canonical)) { continue }
    $owner = Get-DeclaredPlanningOwner $canonical
    if ($owner) {
        Write-Host "  [INFO] Non-canonical copy retained: $canonical -> $owner" -ForegroundColor DarkGray
        continue
    }
    Test-PlanningDoc $canonical
}

# ── E5 — Collision check ──────────────────────────────────────────────────────
foreach ($type in $H1ByType.Keys) {
    $groups = $H1ByType[$type] | Group-Object -Property { $_.H1 }
    foreach ($g in $groups) {
        if ($g.Count -gt 1) {
            Write-Host ""
            Write-Host "  [ERROR E5]" -NoNewline -ForegroundColor Red
            Write-Host " H1 collision — $($g.Count) $type files share the same H1:" -ForegroundColor DarkRed
            foreach ($entry in $g.Group) {
                $rel = $entry.Path.Replace($Root + "\", "").Replace($Root + "/", "")
                Write-Host "             $rel" -ForegroundColor Red
            }
            $script:Errors++
        }
    }
}

# ── Summary ───────────────────────────────────────────────────────────────────
Write-Host ""
$total = $checkedFiles.Count

if ($Errors -eq 0 -and $Warnings -eq 0) {
    Write-Host "  ── $total docs checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "all conformant" -NoNewline -ForegroundColor Green
    Write-Host "  │  DEV-ACCORD.00 ──" -ForegroundColor DarkGray
} elseif ($Errors -eq 0) {
    Write-Host "  ── $total docs checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "0 errors" -NoNewline -ForegroundColor Green
    Write-Host "  $Warnings warnings" -NoNewline -ForegroundColor DarkYellow
    Write-Host "  │  DEV-ACCORD.00 ──" -ForegroundColor DarkGray
} else {
    Write-Host "  ── $total docs checked  │  " -NoNewline -ForegroundColor DarkGray
    Write-Host "$Errors errors" -NoNewline -ForegroundColor Red
    Write-Host "  $Warnings warnings" -NoNewline -ForegroundColor DarkYellow
    Write-Host "  │  DEV-ACCORD.00 ──" -ForegroundColor DarkGray
}
Write-Host ""

if ($Strict -and ($Errors -gt 0 -or $Warnings -gt 0)) { exit 1 }
if ($Errors -gt 0) { exit 1 }
exit 0
