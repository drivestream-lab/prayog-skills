#!/usr/bin/env python3
"""
classify_issues.py
==================
Mode A: Classify all open (non-DONE) GitHub issues in a folder into:
  - Epics, User Stories, Tasks, Defects

Output:
  Full results  → written to <issues_folder>/reports/classification-YYYY-MM-DD.md
  Summary only  → printed to terminal

Usage:
  python scripts/classify_issues.py <issues_folder>

Example:
  python scripts/classify_issues.py issues/DBDHub-SecuritasOfficer-Android/
"""

import os
import sys
import yaml
from collections import defaultdict
from datetime import date
from typing import Optional


# ---------------------------------------------------------------------------
# Label → Type mapping (priority: Epic > Defect > User Story > Task)
# ---------------------------------------------------------------------------
LABEL_MAP = {
    "epic":             "Epic",
    "bug":              "Defect",
    "uat-bug":          "Defect",
    "story":            "User Story",
    "technical story":  "User Story",
    "enhancement":      "User Story",
    "design":           "Task",
    "housekeeping":     "Task",
    "wontfix":          "Task",
}

PRIORITY = ["Epic", "Defect", "User Story", "Task"]


def classify_by_labels(labels: list) -> Optional[str]:
    labels_lower = [l.lower() for l in labels]
    for type_name in PRIORITY:
        for label, mapped in LABEL_MAP.items():
            if mapped == type_name and label in labels_lower:
                return type_name
    return None


def classify_by_title(title: str) -> str:
    t = title.upper()
    if "EPIC" in t:
        return "Epic"
    if any(kw in t for kw in ["BUG", "CRASH", "FIX ERROR", "DEFECT"]):
        return "Defect"
    if t.startswith("SEC:") or "SUSA-" in t:
        return "Task"
    return "Task"


def classify(labels: list, title: str) -> str:
    result = classify_by_labels(labels)
    return result if result else classify_by_title(title)


def parse_issue(filepath: str) -> Optional[dict]:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None

    return {
        "number":    meta.get("number"),
        "title":     meta.get("title", ""),
        "state":     meta.get("state", "open"),
        "labels":    [str(l) for l in (meta.get("labels") or [])],
        "milestone": meta.get("milestone", ""),
        "assignees": meta.get("assignees") or [],
        "author":    meta.get("author", ""),
        "url":       meta.get("url", ""),
    }


def load_all_issues(folder: str) -> list:
    issues = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".md"):
            continue
        meta = parse_issue(os.path.join(folder, fname))
        if meta and meta["number"] is not None:
            issues.append(meta)
    return issues


# ---------------------------------------------------------------------------
# Formatting helpers — write to a list of lines (used for both file and terminal)
# ---------------------------------------------------------------------------
def md_table(rows: list, headers: list) -> list:
    """Return GitHub-flavoured markdown table lines."""
    if not rows:
        return ["*(none)*", ""]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def pad(val, width):
        return str(val).ljust(width)

    header_line = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"
    sep_line    = "| " + " | ".join("-" * w for w in col_widths) + " |"
    lines = [header_line, sep_line]
    for row in rows:
        lines.append("| " + " | ".join(pad(str(c), col_widths[i]) for i, c in enumerate(row)) + " |")
    lines.append("")
    return lines


def plain_table(rows: list, headers: list) -> list:
    """Return fixed-width plain-text table lines for terminal output."""
    if not rows:
        return ["  (none)"]
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_widths)
    sep = "  " + "  ".join("-" * w for w in col_widths)
    lines = [fmt.format(*headers), sep]
    for row in rows:
        lines.append(fmt.format(*[str(c) for c in row]))
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/classify_issues.py <issues_folder>")
        sys.exit(1)

    folder = sys.argv[1].rstrip("/")
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    today       = date.today().isoformat()          # e.g. 2026-02-26
    repo_label  = os.path.basename(folder)          # e.g. DBDHub-SecuritasOfficer-Android
    reports_dir = os.path.join(folder, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    out_path    = os.path.join(reports_dir, f"classification-{today}.md")

    all_issues   = load_all_issues(folder)
    total        = len(all_issues)
    closed       = [i for i in all_issues if i["state"] == "closed"]
    open_issues  = [i for i in all_issues if i["state"] == "open"]

    # Classify
    results = defaultdict(list)
    for issue in open_issues:
        results[classify(issue["labels"], issue["title"])].append(issue)
    for bucket in results.values():
        bucket.sort(key=lambda x: x["number"])

    # ── Build markdown file content ──────────────────────────────────────────
    md = []
    md.append(f"# Issue Classification — {repo_label}")
    md.append(f"*Generated: {today}*")
    md.append("")
    md.append(f"**Total issues:** {total} | **Closed/DONE:** {len(closed)} | **Open/Active:** {len(open_issues)}")
    md.append("")

    for type_name in PRIORITY:
        items = results.get(type_name, [])
        md.append(f"---")
        md.append(f"## {type_name}s ({len(items)})")
        md.append("")
        rows = []
        for i in items:
            labels_str = ", ".join(i["labels"]) if i["labels"] else "*(no label)*"
            title_link = f"[{i['title']}]({i['url']})" if i.get("url") else i["title"]
            status = "🟡 open" if i["state"] == "open" else "🟢 done"
            rows.append([f"#{i['number']}", status, labels_str, i["milestone"] or "", title_link])
        md.extend(md_table(rows, ["#", "Status", "Labels", "Milestone", "Title"]))

    # Summary table
    md.append("---")
    md.append("## Summary")
    md.append("")
    summary_rows = [(t, len(results.get(t, []))) for t in PRIORITY]
    summary_rows.append(("**TOTAL**", f"**{len(open_issues)}**"))
    md.extend(md_table(summary_rows, ["Type", "Open Count"]))

    # Write file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    # ── Terminal: summary only ────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Issue Classification — {repo_label}")
    print(f"  {today}")
    print(f"{'='*60}")
    print(f"\n  Total : {total}  |  Closed/DONE : {len(closed)}  |  Open : {len(open_issues)}\n")

    summary_rows_plain = [(t, len(results.get(t, []))) for t in PRIORITY]
    summary_rows_plain.append(("TOTAL", len(open_issues)))
    for line in plain_table(summary_rows_plain, ["Type", "Count"]):
        print(line)

    print(f"\n  Full report written to:\n  {out_path}\n")


if __name__ == "__main__":
    main()
