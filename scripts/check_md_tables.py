"""
check_md_tables.py — enforce MD060 table separator style.

Fails with exit code 1 if any markdown file contains a table separator row
that does not use the | --- | --- | format (spaces inside pipes, three dashes).

Run:  python scripts/check_md_tables.py [file ...]
      python scripts/check_md_tables.py  (scans repo root recursively)

Wired into pre-commit (.pre-commit-config.yaml) and CI (lint.yml).
Governed by: anti_stall.lint_compliance.MD060 in
  governance-commons/agent-project-orchestrator/governance/multi-agent.yaml
"""
import re
import sys
import glob

BAD_SEP = re.compile(r"^\|[\|\-\: ]+\|$")   # is a separator row
GOOD_SEP = re.compile(r"^\| --- (\| --- )*\|$")  # all cells are exactly "---" with spaces


def is_separator(line: str) -> bool:
    s = line.strip()
    # Must start/end with pipe, contain only pipe/dash/colon/space, AND have at least one dash
    return bool(
        s.startswith("|")
        and s.endswith("|")
        and re.match(r"^[\|\-\: ]+$", s)
        and "-" in s
    )


def is_correct(line: str) -> bool:
    """True if separator row already uses | --- | format."""
    s = line.strip()
    # Every cell between pipes must be exactly " --- " (with surrounding spaces)
    inner = s[1:-1]  # strip leading and trailing |
    cells = inner.split("|")
    return all(c.strip() in ("---", ":---", "---:", ":---:") and c.startswith(" ") and c.endswith(" ") for c in cells)


def check_file(path: str) -> list[tuple[int, str]]:
    violations = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for lineno, raw in enumerate(f, 1):
                line = raw.rstrip("\n")
                if is_separator(line) and not is_correct(line):
                    violations.append((lineno, line.strip()))
    except OSError:
        pass
    return violations


def main() -> int:
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob.glob("**/*.md", recursive=True)

    paths = [p for p in paths if "node_modules" not in p]

    total = 0
    for path in paths:
        violations = check_file(path)
        for lineno, line in violations:
            print(f"{path}:{lineno}: MD060 bad separator: {line!r}")
            print(f"  fix:  | " + " | ".join(["---"] * (line.count("|") - 1)) + " |")
            total += 1

    if total:
        print(f"\n{total} MD060 violation(s). Run: python scripts/fix_md_tables.py")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
