#!/usr/bin/env python3
"""
build_hierarchy.py
==================
Mode B: Build a full repo-wide hierarchy report organized as:

  For each Milestone (alphabetical):
    ├── Epics
    │   └── User Stories / Tasks linked to that epic
    │       └── Defects linked to those stories/tasks
    ├── User Stories & Tasks (no epic, within this milestone)
    └── Defects (no story/task or epic, within this milestone)

  At the end — Issues with no Milestone (same hierarchy order):
    ├── Epics → Stories/Tasks → Defects
    ├── User Stories & Tasks (no epic)
    └── Defects

Output:
  Full report → <issues_folder>/reports/hierarchy-YYYY-MM-DD.md
  Summary     → terminal

Usage:
  python scripts/build_hierarchy.py <issues_folder>

Example:
  python scripts/build_hierarchy.py issues/DBDHub-SecuritasOfficer-Android/
"""

import os
import re
import sys
import yaml
from collections import defaultdict
from datetime import date
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------------------------
# Classification (same as other scripts)
# ---------------------------------------------------------------------------
LABEL_PRIORITY = [
    ({"epic"},                                    "Epic"),
    ({"bug", "uat-bug"},                          "Defect"),
    ({"story", "technical story", "enhancement"}, "User Story"),
    ({"design", "housekeeping", "wontfix"},        "Task"),
]


def classify(labels: list, title: str) -> str:
    ll = {l.lower() for l in labels}
    for label_set, type_name in LABEL_PRIORITY:
        if ll & label_set:
            return type_name
    t = title.upper()
    if "EPIC" in t:
        return "Epic"
    if t.startswith("SEC:") or "SUSA-" in t:
        return "Task"
    if any(kw in t for kw in ["BUG", "CRASH", "ERROR"]):
        return "Defect"
    return "Task"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_issue(filepath: str) -> Optional[Dict[str, Any]]:
    with open(filepath, encoding="utf-8") as f:
        raw = f.read()

    if not raw.startswith("---"):
        return None
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None

    raw_subs = meta.get("sub_issues") or []
    sub_nums = [s["number"] for s in raw_subs if isinstance(s, dict) and "number" in s]

    return {
        "number":       meta.get("number"),
        "title":        meta.get("title", ""),
        "state":        meta.get("state", "open"),
        "labels":       [str(l) for l in (meta.get("labels") or [])],
        "milestone":    meta.get("milestone") or "",
        "url":          meta.get("url", ""),
        "parent_issue": meta.get("parent_issue"),   # int or None
        "sub_issues":   sub_nums,                   # list[int]
        "body":         raw,
    }


def load_all_issues(folder: str) -> List[Dict[str, Any]]:
    issues = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".md"):
            continue
        issue = parse_issue(os.path.join(folder, fname))
        if issue and issue["number"] is not None:
            issues.append(issue)
    return issues


# ---------------------------------------------------------------------------
# Reference detection (for linking defects → stories/tasks)
# ---------------------------------------------------------------------------
FALSE_POSITIVE_PATTERNS = [
    re.compile(r'node-id[=\-]\d*'),
    re.compile(r'files/\d+/'),
    re.compile(r'assets/\d+/'),
    re.compile(r'/\d{7,}'),
]
ISSUE_REF_PATTERN = re.compile(r'(?<![/\-\d])#(\d+)(?!\d)')


def referenced_numbers(body: str) -> List[int]:
    """Return all genuine issue numbers referenced in body."""
    found = []
    for match in ISSUE_REF_PATTERN.finditer(body):
        num = int(match.group(1))
        start = match.start()
        if start > 0 and body[start - 1].isdigit():
            continue
        surrounding = body[max(0, start - 80): start + 80]
        if any(p.search(surrounding) for p in FALSE_POSITIVE_PATTERNS):
            continue
        found.append(num)
    return found


# ---------------------------------------------------------------------------
# Keyword matching (for linking stories/tasks → epics without hierarchy data)
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "android", "ios", "epic", "the", "a", "an", "for", "to", "in",
    "and", "or", "of", "on", "with", "from", "geo", "geco",
    "story", "task", "bug", "feature", "update", "spike", "investigate",
}


def extract_keywords(title: str) -> List[str]:
    cleaned = re.sub(r'^(EPIC\s*[-–]+\s*|GEO:\s*EPIC:\s*|GEO:\s*Epic\s*[-–]+\s*)', '', title, flags=re.IGNORECASE)
    cleaned = re.sub(r'^(Android\s*[-–]+\s*|iOS\s*[-–]+\s*)', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\(.*?\)', '', cleaned)
    words = re.findall(r"[A-Za-z][A-Za-z0-9']+", cleaned)
    meaningful = [w for w in words if w.lower() not in STOP_WORDS and len(w) > 2]
    phrases = [f"{meaningful[i]} {meaningful[i+1]}" for i in range(len(meaningful) - 1)]
    singles = [w for w in meaningful if len(w) > 9]
    return list(dict.fromkeys(phrases + singles))


def keyword_score(issue: Dict, keywords: List[str]) -> int:
    title_lower = issue["title"].lower()
    body_lower  = issue["body"].lower()
    score = 0
    for kw in keywords:
        kw_l = kw.lower()
        if kw_l in title_lower:
            score += 2
        elif " " in kw and kw_l in body_lower:
            score += 1
    return score


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------
def md_table(rows: List[list], headers: List[str]) -> List[str]:
    if not rows:
        return ["*(none)*", ""]
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def pad(val, w):
        return str(val).ljust(w)

    lines = [
        "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |",
        "| " + " | ".join("-" * w for w in col_widths) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(pad(str(c), col_widths[i]) for i, c in enumerate(row)) + " |")
    lines.append("")
    return lines


def status_badge(state: str) -> str:
    return "🟡 open" if state == "open" else "🟢 done"


def issue_row(issue: Dict, badge: str = "") -> list:
    labels     = ", ".join(issue["labels"]) if issue["labels"] else "*(no label)*"
    title_link = f"[{issue['title']}]({issue['url']})" if issue.get("url") else issue["title"]
    return [f"{badge}#{issue['number']}", status_badge(issue["state"]), labels, title_link]


# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------
def build_milestone_section(
    ms_name: str,
    issues: List[Dict],
    issue_by_num: Dict[int, Dict],
) -> List[str]:
    """
    Build the markdown section for one milestone (or the no-milestone bucket).
    Returns a list of markdown lines.
    """
    md = []

    epics   = [i for i in issues if classify(i["labels"], i["title"]) == "Epic"]
    stories = [i for i in issues if classify(i["labels"], i["title"]) in ("User Story", "Task")]
    defects = [i for i in issues if classify(i["labels"], i["title"]) == "Defect"]

    epics_sorted   = sorted(epics,   key=lambda x: x["number"])
    stories_sorted = sorted(stories, key=lambda x: x["number"])
    defects_sorted = sorted(defects, key=lambda x: x["number"])

    # Track which stories and defects have been placed under an epic
    placed_stories = set()
    placed_defects = set()

    # ── Epics ────────────────────────────────────────────────────────────────
    if epics_sorted:
        md.append(f"### Epics ({len(epics_sorted)})")
        md.append("")

        for epic in epics_sorted:
            badge      = "🔗 " if epic["sub_issues"] else ""
            title_link = f"[{epic['title']}]({epic['url']})" if epic.get("url") else epic["title"]
            md.append(f"#### {badge}Epic #{epic['number']} — {status_badge(epic['state'])}")
            md.append(f"**{title_link}**  ")
            labels_str = ", ".join(epic["labels"]) if epic["labels"] else "*(no label)*"
            md.append(f"Labels: `{labels_str}`")
            md.append("")

            # Find child stories/tasks for this epic
            epic_kws   = extract_keywords(epic["title"])
            epic_subs  = set(epic["sub_issues"])

            child_stories = []
            for s in stories_sorted:
                # Signal 0: hierarchy
                if s["number"] in epic_subs or s["parent_issue"] == epic["number"]:
                    child_stories.append((s, "🔗"))
                    continue
                # Signal 1+2: same milestone + keyword
                if ms_name and s["milestone"] == ms_name and keyword_score(s, epic_kws) > 0:
                    child_stories.append((s, ""))

            # Deduplicate (keep first occurrence)
            seen = set()
            unique_children = []
            for s, badge_s in child_stories:
                if s["number"] not in seen:
                    seen.add(s["number"])
                    unique_children.append((s, badge_s))

            if unique_children:
                rows = []
                for s, badge_s in sorted(unique_children, key=lambda x: (x[0]["state"] != "open", x[0]["number"])):
                    placed_stories.add(s["number"])
                    labels_s     = ", ".join(s["labels"]) if s["labels"] else "*(no label)*"
                    title_link_s = f"[{s['title']}]({s['url']})" if s.get("url") else s["title"]
                    rows.append([f"{badge_s}#{s['number']}", status_badge(s["state"]), labels_s, title_link_s])

                    # Defects linked to this story
                    child_defects = []
                    for d in defects_sorted:
                        if d["parent_issue"] == s["number"]:
                            child_defects.append(d)
                            continue
                        if s["number"] in referenced_numbers(d["body"]):
                            child_defects.append(d)

                    for d in child_defects:
                        placed_defects.add(d["number"])
                        labels_d     = ", ".join(d["labels"]) if d["labels"] else "*(no label)*"
                        title_link_d = f"[{d['title']}]({d['url']})" if d.get("url") else d["title"]
                        rows.append([f"↳ #{d['number']}", status_badge(d["state"]), labels_d, title_link_d])

                md.extend(md_table(rows, ["#", "Status", "Labels", "Title"]))
            else:
                md.append("*No linked user stories or tasks found.*")
                md.append("")

    # ── Stories & Tasks without an epic ─────────────────────────────────────
    orphan_stories = [s for s in stories_sorted if s["number"] not in placed_stories]
    if orphan_stories:
        md.append(f"### User Stories & Tasks — no epic ({len(orphan_stories)})")
        md.append("")
        rows = []
        for s in orphan_stories:
            rows.append(issue_row(s))
            # Defects linked to this orphan story
            for d in defects_sorted:
                if d["parent_issue"] == s["number"] or s["number"] in referenced_numbers(d["body"]):
                    placed_defects.add(d["number"])
                    labels_d     = ", ".join(d["labels"]) if d["labels"] else "*(no label)*"
                    title_link_d = f"[{d['title']}]({d['url']})" if d.get("url") else d["title"]
                    rows.append([f"↳ #{d['number']}", status_badge(d["state"]), labels_d, title_link_d])
        md.extend(md_table(rows, ["#", "Status", "Labels", "Title"]))

    # ── Orphan defects (not linked to any story or epic) ─────────────────────
    orphan_defects = [d for d in defects_sorted if d["number"] not in placed_defects]
    if orphan_defects:
        md.append(f"### Defects — no story/task or epic ({len(orphan_defects)})")
        md.append("")
        md.extend(md_table([issue_row(d) for d in orphan_defects], ["#", "Status", "Labels", "Title"]))

    return md


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_hierarchy.py <issues_folder>")
        sys.exit(1)

    folder = sys.argv[1].rstrip("/")
    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    today       = date.today().isoformat()
    repo_label  = os.path.basename(folder)
    reports_dir = os.path.join(folder, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    out_path    = os.path.join(reports_dir, f"hierarchy-{today}.md")

    all_issues   = load_all_issues(folder)
    issue_by_num = {i["number"]: i for i in all_issues}
    total        = len(all_issues)
    closed       = sum(1 for i in all_issues if i["state"] == "closed")

    # Group issues by milestone; blank milestone → no-milestone bucket
    by_milestone: Dict[str, List[Dict]] = defaultdict(list)
    for issue in all_issues:
        by_milestone[issue["milestone"]].append(issue)

    # Milestones: alphabetical; no-milestone always last
    milestone_names = sorted(
        [ms for ms in by_milestone if ms],
        key=str.lower,
    )
    no_milestone_issues = by_milestone.get("", [])

    # ── Build markdown ────────────────────────────────────────────────────────
    md = []
    md.append(f"# Issue Hierarchy — {repo_label}")
    md.append(f"*Generated: {today}*")
    md.append("")
    md.append(f"**Total issues:** {total} | **Closed/DONE:** {closed} | **Open/Active:** {total - closed}")
    md.append("")

    # Stats per milestone for TOC-style summary
    md.append("## Milestones")
    md.append("")
    ms_summary_rows = []
    for ms in milestone_names:
        issues_in_ms = by_milestone[ms]
        epics_c   = sum(1 for i in issues_in_ms if classify(i["labels"], i["title"]) == "Epic")
        stories_c = sum(1 for i in issues_in_ms if classify(i["labels"], i["title"]) in ("User Story", "Task"))
        defects_c = sum(1 for i in issues_in_ms if classify(i["labels"], i["title"]) == "Defect")
        ms_summary_rows.append([ms, len(issues_in_ms), epics_c, stories_c, defects_c])
    if no_milestone_issues:
        epics_c   = sum(1 for i in no_milestone_issues if classify(i["labels"], i["title"]) == "Epic")
        stories_c = sum(1 for i in no_milestone_issues if classify(i["labels"], i["title"]) in ("User Story", "Task"))
        defects_c = sum(1 for i in no_milestone_issues if classify(i["labels"], i["title"]) == "Defect")
        ms_summary_rows.append(["*(no milestone)*", len(no_milestone_issues), epics_c, stories_c, defects_c])
    md.extend(md_table(ms_summary_rows, ["Milestone", "Total", "Epics", "Stories/Tasks", "Defects"]))

    # ── One section per milestone (collapsible) ──────────────────────────────
    for ms in milestone_names:
        issues_in_ms = by_milestone[ms]
        open_count   = sum(1 for i in issues_in_ms if i["state"] == "open")
        done_count   = len(issues_in_ms) - open_count
        md.append("")
        md.append("---")
        md.append("")
        md.append(f"<details>")
        md.append(f"<summary><strong>📌 Milestone: {ms}</strong>    🟡 {open_count} open  ·  🟢 {done_count} done  ·  {len(issues_in_ms)} total</summary>")
        md.append("")
        md.extend(build_milestone_section(ms, issues_in_ms, issue_by_num))
        md.append("</details>")

    # ── No-milestone bucket (collapsible) ─────────────────────────────────────
    if no_milestone_issues:
        open_count = sum(1 for i in no_milestone_issues if i["state"] == "open")
        done_count = len(no_milestone_issues) - open_count
        md.append("")
        md.append("---")
        md.append("")
        md.append(f"<details>")
        md.append(f"<summary><strong>📌 No Milestone</strong>    🟡 {open_count} open  ·  🟢 {done_count} done  ·  {len(no_milestone_issues)} total</summary>")
        md.append("")
        md.extend(build_milestone_section("", no_milestone_issues, issue_by_num))
        md.append("</details>")

    # Write file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    # ── Terminal summary ──────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Issue Hierarchy — {repo_label}")
    print(f"  {today}")
    print(f"{'='*60}")
    print(f"\n  Total: {total}  |  Closed/DONE: {closed}  |  Open: {total - closed}\n")
    print(f"  {'Milestone':<22} {'Total':>6}  {'Epics':>5}  {'Stories/Tasks':>13}  {'Defects':>7}")
    print(f"  {'-'*22} {'-'*6}  {'-'*5}  {'-'*13}  {'-'*7}")
    for row in ms_summary_rows:
        print(f"  {str(row[0]):<22} {row[1]:>6}  {row[2]:>5}  {row[3]:>13}  {row[4]:>7}")
    print(f"\n  Full report written to:\n  {out_path}\n")


if __name__ == "__main__":
    main()
