#!/usr/bin/env python3
"""
Consistency check for prayog-skills cross-file token invariants.

Checks that known cross-referenced tokens (report prefixes, branch patterns,
skill names, trigger strings) are used consistently across all SKILL.md and
references/*.md files. Exits 1 if any violation is found.

Run: python scripts/check_consistency.py
CI:  add to .github/workflows/ci.yml as a step.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"

# ── Invariants ────────────────────────────────────────────────────────────────
# Each entry: (description, pattern, allowed_values, file_glob)
# pattern = regex to extract the value; must match in files matching file_glob
# allowed_values = the only acceptable matches (set); None = collect and check
#                  all files agree on the same value.

SINGLE_VALUE_INVARIANTS = [
    (
        "feasibility_prefix must be Initiative-Feasibility-Report everywhere",
        r"feasibility_prefix[:\|]\s*([\w-]+)",
        {"Initiative-Feasibility-Report"},
        "**/*.{md,yaml}",
    ),
    (
        "No stale short_code / {sc} branch convention outside spec-implementation-plan",
        r"chore/\{sc\}",
        set(),  # empty = must not appear
        "**/development/**/references/output-template.md",
    ),
    (
        "No stale spec-handoff PR trigger strings",
        r'background_trigger:.*spec-handoff',
        set(),  # must not appear
        "**/*.md",
    ),
    (
        "No stale spec-feasibility-review references (renamed to initiative-feasibility)",
        r'spec-feasibility-review',
        set(),  # must not appear
        "**/*.md",
    ),
]

SYNC_COPY_INVARIANT = (
    "governance.md files marked SYNC-COPY must be byte-identical",
    [
        "skills/development/pre-implement/references/governance.md",
        "skills/development/initiative-feasibility/references/governance.md",
        "skills/development/spec-implementation-plan/references/governance.md",
    ],
)

SKILL_REGISTRY_INVARIANT = (
    "Every skill directory must be listed in README.md",
    # skills that are intentionally unlisted (stubs, meta-only)
    set(),
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def all_skill_files(pattern: str = "**/*.md") -> list[Path]:
    return list(SKILLS_DIR.glob(pattern)) + list((ROOT / "profiles").glob("*.yaml"))


def check_single_value(description: str, regex: str, allowed: set[str], glob: str) -> list[str]:
    errors = []
    files = list(SKILLS_DIR.glob(glob)) + list((ROOT / "profiles").glob("*.yaml"))
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in re.finditer(regex, text):
            value = match.group(1).strip() if match.lastindex else match.group(0).strip()
            if allowed and value not in allowed:
                errors.append(f"  {f.relative_to(ROOT)}: found {value!r}, expected one of {allowed}")
            elif not allowed:
                # "must not appear" case
                errors.append(f"  {f.relative_to(ROOT)}: stale pattern found: {match.group(0)!r}")
    return errors


def check_sync_copy(description: str, paths: list[str]) -> list[str]:
    errors = []
    contents = []
    for p in paths:
        full = ROOT / p
        if not full.exists():
            errors.append(f"  MISSING: {p}")
            continue
        contents.append((p, full.read_text(encoding="utf-8")))
    if len(contents) < 2:
        return errors
    ref_path, ref_text = contents[0]
    for other_path, other_text in contents[1:]:
        if ref_text != other_text:
            errors.append(
                f"  DRIFT: {other_path} differs from {ref_path}\n"
                f"    Run: diff {ref_path} {other_path}"
            )
    return errors


def check_skill_registry() -> list[str]:
    errors = []
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill_dir in SKILLS_DIR.rglob("*/SKILL.md"):
        skill_name = skill_dir.parent.name
        if skill_name not in readme:
            errors.append(f"  {skill_dir.relative_to(ROOT)}: skill {skill_name!r} not mentioned in README.md")
    return errors


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    all_errors: list[tuple[str, list[str]]] = []

    for description, regex, allowed, glob in SINGLE_VALUE_INVARIANTS:
        errors = check_single_value(description, regex, allowed, glob)
        if errors:
            all_errors.append((description, errors))

    desc, paths = SYNC_COPY_INVARIANT
    errors = check_sync_copy(desc, paths)
    if errors:
        all_errors.append((desc, errors))

    desc, _ = SKILL_REGISTRY_INVARIANT
    errors = check_skill_registry()
    if errors:
        all_errors.append((desc, errors))

    if all_errors:
        print("prayog-skills consistency check FAILED\n")
        for description, errors in all_errors:
            print(f"[FAIL] {description}")
            for e in errors:
                print(e)
            print()
        return 1

    print("prayog-skills consistency check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
