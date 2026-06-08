#!/usr/bin/env python3
"""
find_epic_relations.py
======================
Mode B: Find all issues related to a given epic.

Relationship signals, in priority order:
  0. Hierarchy links  — parent_issue / sub_issues in frontmatter  ✅ Definitive
  1. Same milestone   — issues sharing the epic's milestone        ✅ Hard data
  2. Keyword match    — epic title phrases in issue title/body     ✅ Hard data
  3. Explicit ref     — standalone #<epic_number> in body          ✅ Hard data

Output:
  Full results  → written to <issues_folder>/reports/epic-<N>-relations-YYYY-MM-DD.md
  Summary only  → printed to terminal

Usage:
  python scripts/find_epic_relations.py <issues_folder> <epic_number>

Example:
  python scripts/find_epic_relations.py issues/DBDHub-SecuritasOfficer-Android/ 1042
"""

import os
import re
import sys
import yaml
from collections import defaultdict
from datetime import date
from typing import Optional, List


# ---------------------------------------------------------------------------
# Type classification (same logic as classify_issues.py)
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
# File parsing — includes hierarchy fields
# ---------------------------------------------------------------------------
def parse_issue(filepath: str) -> Optional[dict]:
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
    sub_issue_numbers = [s["number"] for s in raw_subs if isinstance(s, dict) and "number" in s]

    return {
        "number":       meta.get("number"),
        "title":        meta.get("title", ""),
        "state":        meta.get("state", "open"),
        "labels":       [str(l) for l in (meta.get("labels") or [])],
        "milestone":    meta.get("milestone", ""),
        "url":          meta.get("url", ""),
        "parent_issue": meta.get("parent_issue"),
        "sub_issues":   sub_issue_numbers,
        "body":         raw,
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
# Signal 3: Explicit #reference detection (with false-positive guard)
# ---------------------------------------------------------------------------
FALSE_POSITIVE_PATTERNS = [
    re.compile(r'node-id[=\-]\d*'),
    re.compile(r'files/\d+/'),
    re.compile(r'assets/\d+/'),
    re.compile(r'/\d{7,}'),
]
ISSUE_REF_PATTERN = re.compile(r'(?<![/\-\d])#(\d+)(?!\d)')


def find_real_references(body: str, target_num: int) -> List[str]:
    real_refs = []
    for match in ISSUE_REF_PATTERN.finditer(body):
        if int(match.group(1)) != target_num:
            continue
        start = match.start()
        if start > 0 and body[start - 1].isdigit():
            continue
        surrounding = body[max(0, start - 80): start + 80]
        if any(p.search(surrounding) for p in FALSE_POSITIVE_PATTERNS):
            continue
        snippet = body[max(0, start - 50): start + 80].replace("\n", " ").strip()
        real_refs.append(snippet)
    return real_refs


# ---------------------------------------------------------------------------
# Signal 2: Keyword extraction from epic title
# ---------------------------------------------------------------------------
STOP_WORDS = {
    "android", "ios", "epic", "the", "a", "an", "for", "to", "in",
    "and", "or", "of", "on", "with", "from", "geo", "geo:", "geco:",
    "story", "task", "bug", "feature", "update", "spike", "investigate",
    "--", "-", ":", "+"
}


def extract_keywords(title: str) -> List[str]:
    cleaned = re.sub(r'^(EPIC\s*[-–]+\s*|GEO:\s*EPIC:\s*|GEO:\s*Epic\s*[-–]+\s*)', '', title, flags=re.IGNORECASE)
    cleaned = re.sub(r'^(Android\s*[-–]+\s*|iOS\s*[-–]+\s*)', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\(.*?\)', '', cleaned)

    words = re.findall(r"[A-Za-z][A-Za-z0-9']+", cleaned)
    meaningful = [w for w in words if w.lower() not in STOP_WORDS and len(w) > 2]

    phrases = [f"{meaningful[i]} {meaningful[i+1]}" for i in range(len(meaningful) - 1)]
    specific_singles = [w for w in meaningful if len(w) > 9]
    return list(dict.fromkeys(phrases + specific_singles))


def keyword_match_score(issue: dict, keywords: List[str]) -> List[str]:
    title_lower = issue["title"].lower()
    body_lower  = issue["body"].lower()
    hits = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title_lower:
            hits.append(kw)
        elif " " in kw and kw_lower in body_lower:
            hits.append(kw)
    return hits


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------
def md_table(rows: list, headers: list) -> List[str]:
    if not rows:
        return ["*(none)*", ""]
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def pad(val, width):
        return str(val).ljust(width)

    lines = [
        "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |",
        "| " + " | ".join("-" * w for w in col_widths) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(pad(str(c), col_widths[i]) for i, c in enumerate(row)) + " |")
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/find_epic_relations.py <issues_folder> <epic_number>")
        sys.exit(1)

    folder = sys.argv[1].rstrip("/")
    try:
        epic_num = int(sys.argv[2])
    except ValueError:
        print(f"Error: epic_number must be an integer, got: {sys.argv[2]}")
        sys.exit(1)

    if not os.path.isdir(folder):
        print(f"Error: folder not found: {folder}")
        sys.exit(1)

    today       = date.today().isoformat()
    repo_label  = os.path.basename(folder)
    reports_dir = os.path.join(folder, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    out_path    = os.path.join(reports_dir, f"epic-{epic_num}-relations-{today}.md")

    all_issues   = load_all_issues(folder)
    issue_by_num = {i["number"]: i for i in all_issues}

    epic = issue_by_num.get(epic_num)
    if not epic:
        print(f"Error: issue #{epic_num} not found in {folder}")
        sys.exit(1)

    epic_milestone     = epic["milestone"]
    epic_keywords      = extract_keywords(epic["title"])
    declared_sub_nums  = set(epic["sub_issues"])

    # Sibling epics (for milestone pollution check)
    sibling_epic_keywords = []
    for issue in all_issues:
        if issue["number"] == epic_num:
            continue
        if "epic" in [l.lower() for l in issue["labels"]] and issue["milestone"] == epic_milestone:
            sibling_epic_keywords.append((issue["number"], issue["title"], extract_keywords(issue["title"])))

    # Collect signals
    candidates = {}
    for issue in all_issues:
        num = issue["number"]
        if num == epic_num:
            continue
        if issue["state"] == "closed":
            continue

        signals = []
        tier    = 99

        if num in declared_sub_nums:
            signals.append(f"sub_issue of #{epic_num} (declared on epic)")
            tier = min(tier, 0)

        if issue["parent_issue"] == epic_num:
            signals.append(f"parent_issue = #{epic_num} (declared on issue)")
            tier = min(tier, 0)

        if epic_milestone and issue["milestone"] == epic_milestone:
            signals.append(f"same milestone ({epic_milestone})")
            tier = min(tier, 1)

        matched_kws = keyword_match_score(issue, epic_keywords)
        if matched_kws:
            signals.append(f"keyword match: {', '.join(matched_kws[:3])}")
            tier = min(tier, 2)

        refs = find_real_references(issue["body"], epic_num)
        if refs:
            signals.append(f"explicit reference to #{epic_num}")
            tier = min(tier, 3)

        if not signals:
            continue

        # Milestone pollution check
        if tier > 0 and sibling_epic_keywords and issue["milestone"] == epic_milestone:
            our_score = len(keyword_match_score(issue, epic_keywords))
            for sib_num, sib_title, sib_kws in sibling_epic_keywords:
                if len(keyword_match_score(issue, sib_kws)) > our_score:
                    signals = [s for s in signals if "same milestone" not in s]
                    break

        if signals:
            candidates[num] = {"issue": issue, "signals": signals, "tier": tier}

    # Group by type
    grouped = defaultdict(list)
    for num, data in sorted(candidates.items()):
        issue_type = classify(data["issue"]["labels"], data["issue"]["title"])
        if issue_type == "Epic":
            continue
        grouped[issue_type].append(data)

    # Signal summary counts
    hierarchy_nums = sorted(n for n, d in candidates.items() if d["tier"] == 0)
    milestone_nums = sorted(n for n, d in candidates.items() if any("same milestone" in s for s in d["signals"]))
    keyword_nums   = sorted(n for n, d in candidates.items() if any("keyword" in s for s in d["signals"]))
    ref_nums       = sorted(n for n, d in candidates.items() if any("explicit reference" in s for s in d["signals"]))

    def fmt(nums):
        return ", ".join(f"#{n}" for n in nums) if nums else "(none)"

    ORDER = ["User Story", "Task", "Defect"]

    # ── Build markdown file ───────────────────────────────────────────────────
    md = []
    md.append(f"# Related Issues for Epic #{epic_num} — {epic['title']}")
    md.append(f"*Generated: {today} | Repo: {repo_label}*")
    md.append("")
    md.append(f"**Milestone:** {epic_milestone or '(none)'}  ")
    md.append(f"**Declared sub-issues:** {sorted(declared_sub_nums) or '(none)'}  ")
    md.append(f"**Keywords extracted:** {epic_keywords}")
    md.append("")
    md.append("---")
    md.append("## Relationship Evidence")
    md.append("")
    evidence_rows = [
        ["Hierarchy link (sub_issues / parent_issue)", fmt(hierarchy_nums), "✅✅ Definitive"],
        [f"Same milestone ({epic_milestone or '—'})",  fmt(milestone_nums), "✅ Hard data"],
        ["Keyword match in title/body",                fmt(keyword_nums),   "✅ Hard data"],
        [f"Explicit #{epic_num} reference in body",    fmt(ref_nums),       "✅ Hard data"],
    ]
    md.extend(md_table(evidence_rows, ["Signal", "Issues", "Confidence"]))

    for type_name in ORDER:
        items = grouped.get(type_name, [])
        md.append("---")
        md.append(f"## {type_name}s ({len(items)})")
        md.append("")
        if not items:
            md.append("*None found through data.*")
            md.append("")
            md.append(f"> **Suggestion:** Check if {type_name.lower()}s exist in other repos for this epic,")
            md.append(f"> or verify that sub-issues are linked on GitHub for #{epic_num}.")
            md.append("")
            continue

        items_sorted = sorted(items, key=lambda d: (d["tier"], d["issue"]["number"]))
        rows = []
        for data in items_sorted:
            issue   = data["issue"]
            badge   = "🔗 " if data["tier"] == 0 else ""
            labels  = ", ".join(issue["labels"]) if issue["labels"] else "*(no label)*"
            title_link = f"[{issue['title']}]({issue['url']})" if issue.get("url") else issue["title"]
            evidence = " \\| ".join(data["signals"])
            rows.append([f"{badge}#{issue['number']}", labels, issue["milestone"] or "", title_link, evidence])
        md.extend(md_table(rows, ["#", "Labels", "Milestone", "Title", "Evidence"]))

    # Superseded / duplicate detection
    seen_titles = defaultdict(list)
    for data in candidates.values():
        issue = data["issue"]
        normalized = re.sub(r'^\s*(android|ios)\s*[-–]+\s*', '', issue["title"],
                            flags=re.IGNORECASE).lower().strip()
        seen_titles[normalized].append(issue)

    duplicates = {k: v for k, v in seen_titles.items() if len(v) > 1}
    if duplicates:
        md.append("---")
        md.append("## ⚠ Possible Superseded / Duplicate Stories")
        md.append("")
        for norm_title, issues in duplicates.items():
            issues_sorted = sorted(issues, key=lambda x: x.get("number", 0))
            md.append(f"**Normalized title:** \"{norm_title}\"")
            for i in issues_sorted:
                md.append(f"- #{i['number']} — {i['title']}")
            md.append(f"→ Latest is likely #{issues_sorted[-1]['number']}; earlier may be superseded.")
            md.append("")

    # Summary table at end of file
    md.append("---")
    md.append("## Summary")
    md.append("")
    summary_rows = [(t, len(grouped.get(t, []))) for t in ORDER]
    summary_rows.append(("**TOTAL**", f"**{sum(len(grouped.get(t,[])) for t in ORDER)}**"))
    md.extend(md_table(summary_rows, ["Type", "Count"]))

    # Write file
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    # ── Terminal: summary only ────────────────────────────────────────────────
    total_related = sum(len(grouped.get(t, [])) for t in ORDER)
    print(f"\n{'='*60}")
    print(f"  Epic #{epic_num} — {epic['title'][:50]}{'…' if len(epic['title'])>50 else ''}")
    print(f"  Milestone : {epic_milestone or '(none)'}")
    print(f"  {today}")
    print(f"{'='*60}")
    print(f"\n  Hierarchy links : {len(hierarchy_nums)} issue(s)  {fmt(hierarchy_nums)}")
    print(f"  Same milestone  : {len(milestone_nums)} issue(s)")
    print(f"  Keyword match   : {len(keyword_nums)} issue(s)")
    print(f"  Explicit refs   : {len(ref_nums)} issue(s)\n")

    for type_name in ORDER:
        count = len(grouped.get(type_name, []))
        print(f"  {type_name:<15} {count}")
    print(f"  {'─'*20}")
    print(f"  {'TOTAL':<15} {total_related}")
    print(f"\n  Full report written to:\n  {out_path}\n")


if __name__ == "__main__":
    main()
