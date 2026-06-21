"""
fix_md_tables.py — auto-fix MD060 table separator style repo-wide.

Rewrites all table separator rows to use | --- | --- | format.
Run after getting MD060 violations from check_md_tables.py.

Run:  python scripts/fix_md_tables.py [file ...]
      python scripts/fix_md_tables.py  (fixes all markdown files in repo)
"""
import re
import sys
import glob


def fix_separators(content: str) -> tuple[str, int]:
    lines = content.split("\n")
    result = []
    count = 0
    for line in lines:
        s = line.strip()
        if (
            s.startswith("|")
            and s.endswith("|")
            and re.match(r"^[\|\-\: ]+$", s)
            and re.search(r"\|[-:]+\|", s)
        ):
            cols = s.count("|") - 1
            result.append("| " + " | ".join(["---"] * cols) + " |")
            count += 1
        else:
            result.append(line)
    return "\n".join(result), count


def main() -> int:
    if len(sys.argv) > 1:
        paths = sys.argv[1:]
    else:
        paths = glob.glob("**/*.md", recursive=True)

    paths = [p for p in paths if "node_modules" not in p]

    total_files = 0
    total_fixes = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
            new_content, count = fix_separators(content)
            if count:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"fixed {count} separator(s): {path}")
                total_files += 1
                total_fixes += count
        except OSError as e:
            print(f"error: {path}: {e}")

    if total_fixes:
        print(f"\n{total_fixes} separator(s) fixed across {total_files} file(s).")
    else:
        print("No violations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
