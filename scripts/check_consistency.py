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
#
# WARNING: pathlib.Path.glob() does NOT support shell-style brace expansion
# (e.g. "*.{md,yaml}" is a LITERAL pattern, not "*.md OR *.yaml" — it will
# silently match zero files). Use a single extension per glob, or "**/*.md"
# if you need broad coverage. check_single_value() already appends
# profiles/*.yaml to every invariant's file list unconditionally, so most
# invariants only need to glob under skills/.

SINGLE_VALUE_INVARIANTS = [
    (
        "feasibility_prefix must be Initiative-Feasibility-Report everywhere",
        # \s* before the delimiter matters: markdown tables render this as
        # "| feasibility_prefix | value |" (space before the pipe), not
        # "feasibility_prefix: value" — a delimiter-adjacent regex silently
        # matches only the YAML form and misses every layout-defaults.md.
        r"feasibility_prefix\s*[:\|]\s*([\w-]+)",
        {"Initiative-Feasibility-Report"},
        "**/*.md",
    ),
    (
        "No stale short_code / {sc} branch convention outside spec-implementation-plan",
        r"chore/\{sc\}",
        set(),  # empty = must not appear
        "**/development/**/references/output-template.md",
    ),
    (
        "No stale prd-handoff references",
        r'prd-handoff',
        set(),  # must not appear
        "**/*.md",
    ),
    (
        "No stale generate-work-manifest references",
        r'generate-work-manifest',
        set(),  # must not appear
        "**/*.md",
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

CHECK_REGISTRIES = [
    (
        "skills/development/spec-draft/references/checks.md",
        "D",
        12,
        [
            "skills/development/spec-draft/SKILL.md",
            "skills/development/spec-draft/references/output-template.md",
        ],
    ),
    (
        "skills/development/initiative-feasibility/references/checks.md",
        "F",
        14,
        [
            "skills/development/initiative-feasibility/SKILL.md",
            "skills/development/initiative-feasibility/references/output-template.md",
        ],
    ),
    (
        "skills/development/spec-technical-review/references/checks.md",
        "T",
        11,
        [
            "skills/development/spec-technical-review/SKILL.md",
            "skills/development/spec-technical-review/references/output-template.md",
        ],
    ),
    (
        "skills/development/spec-implementation-plan/references/checks.md",
        "P",
        14,
        [
            "skills/development/spec-implementation-plan/SKILL.md",
            "skills/development/spec-implementation-plan/references/output-template.md",
        ],
    ),
]

REQUIRED_TOKENS = {
    "skills/requirements/prd-impact-map/references/output-template.md": [
        "schema_version:",
        "source_prd_digest:",
        "Scope digest",
        "## 9. Downstream ripple ledger",
        "## T0 collision report",
        "human_decision: pending",
        "## 11. PR readiness handoff",
        "## 12. Approval request",
        "No GitHub side effects have occurred",
    ],
    "skills/development/spec-draft/references/output-template.md": [
        "PRD digest",
        "Impact-map revision",
        "Repo scope digest",
        "## Negative and failure paths",
        "## Draft check summary",
        "D12 Output completeness",
    ],
    "skills/development/initiative-feasibility/references/output-template.md": [
        "Source freshness",
        "Repo scope digest",
        "Default if deferred",
        "Resolution reference",
    ],
    "skills/development/spec-technical-review/references/output-template.md": [
        "Source freshness",
        "Feasibility digest",
        "All T1–T11 checks",
    ],
    "skills/development/spec-implementation-plan/references/output-template.md": [
        "## Source freshness and command contract",
        "Spec path",
        "## 9. WorkManifest seed",
    ],
    "skills/development/pre-implement/references/output-template.md": [
        "Plan source freshness",
        "`check_command`",
        "`ground_command`",
    ],
}

FORBIDDEN_WORKFLOW_TEXT = {
    "skills/development/spec-technical-review": ["T1–T10", "T1-T10"],
    "skills/development/spec-implementation-plan": ["P14 | **WorkManifest seed** — §8"],
    "skills/development/loop-spec/SKILL.md": ["Human explicitly approves → `/ground-spec`"],
}

DELIVERY_CONTRACT_FILES = [
    "delivery-contract.yaml",
    "workflow.yaml",
    "references/handoff-envelope.md",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def all_skill_files(pattern: str = "**/*.md") -> list[Path]:
    return list(SKILLS_DIR.glob(pattern)) + list((ROOT / "profiles").glob("*.yaml"))


def check_single_value(description: str, regex: str, allowed: set[str], glob: str) -> list[str]:
    errors = []
    skill_files = list(SKILLS_DIR.glob(glob))
    profile_files = list((ROOT / "profiles").glob("*.yaml"))
    if not skill_files:
        # A glob that matches nothing under skills/ is almost always a bug in
        # the glob itself (e.g. unsupported brace expansion — see WARNING
        # above) rather than a genuinely empty file set. Check skill_files in
        # isolation: profile_files is appended unconditionally below and
        # would otherwise mask a fully-broken skills/ glob (as it did here
        # originally — "**/*.{md,yaml}" matched 0 skill files but the check
        # still "passed" because the 2 profile yamls were always present).
        return [
            f"  BROKEN CHECK: glob {glob!r} matched 0 files under {SKILLS_DIR.relative_to(ROOT)}/ "
            f"— this invariant is not validating anything under skills/. Fix the glob (see "
            f"WARNING above SINGLE_VALUE_INVARIANTS) rather than ignoring this error."
        ]
    files = skill_files + profile_files
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


def check_profile_registry() -> list[str]:
    """Every skills/development/*/SKILL.md must be listed in every
    profiles/*.yaml `development_skills:` block, and every entry in that
    block must correspond to a real skill directory (no stale entries).

    This is the check that would have caught the original registry-drift
    bug (ground-spec/loop-spec/spec-technical-review missing from
    profiles/*.yaml) — README mentions alone do not cover it, because
    launchpad sync-harness seeds consumer repos from profiles/*.yaml, not
    from README.md.

    Deliberately avoids a YAML-parsing dependency (keeps this script
    stdlib-only) by extracting the development_skills: block with a
    targeted regex instead.
    """
    errors: list[str] = []
    dev_dir = SKILLS_DIR / "development"
    if not dev_dir.exists():
        return errors
    actual_skills = {p.parent.name for p in dev_dir.glob("*/SKILL.md")}

    profile_files = list((ROOT / "profiles").glob("*.yaml"))
    if not profile_files:
        return [f"  BROKEN CHECK: no profiles/*.yaml files found"]

    block_re = re.compile(r"development_skills:\s*\n((?:[ \t]*-[ \t]*\S+[ \t]*\n?)+)")
    item_re = re.compile(r"-\s*(\S+)")

    for pf in profile_files:
        text = pf.read_text(encoding="utf-8")
        if "requirements_skills:" in text and "development_skills:" not in text:
            continue
        m = block_re.search(text)
        if not m:
            errors.append(f"  {pf.relative_to(ROOT)}: no development_skills: list found")
            continue
        listed = set(item_re.findall(m.group(1)))
        for skill in sorted(actual_skills - listed):
            errors.append(
                f"  {pf.relative_to(ROOT)}: missing {skill!r} "
                f"(exists at skills/development/{skill}/SKILL.md but not in development_skills:)"
            )
        for skill in sorted(listed - actual_skills):
            errors.append(
                f"  {pf.relative_to(ROOT)}: stale entry {skill!r} "
                f"(listed in development_skills: but skills/development/{skill}/ does not exist)"
            )
    return errors


def check_requirements_profile_registry() -> list[str]:
    """Every skills/requirements/*/SKILL.md must be listed in profiles that
    declare requirements_skills (meta-pm), with no stale entries."""
    errors: list[str] = []
    req_dir = SKILLS_DIR / "requirements"
    if not req_dir.exists():
        return errors
    actual_skills = {p.parent.name for p in req_dir.glob("*/SKILL.md")}

    profile_files = list((ROOT / "profiles").glob("*.yaml"))
    block_re = re.compile(r"requirements_skills:\s*\n((?:[ \t]*-[ \t]*\S+[ \t]*\n?)+)")
    item_re = re.compile(r"-\s*(\S+)")

    listed_any: set[str] = set()
    for pf in profile_files:
        text = pf.read_text(encoding="utf-8")
        m = block_re.search(text)
        if not m:
            continue
        listed = set(item_re.findall(m.group(1)))
        listed_any |= listed
        for skill in sorted(actual_skills - listed):
            errors.append(
                f"  {pf.relative_to(ROOT)}: missing {skill!r} "
                f"(exists at skills/requirements/{skill}/SKILL.md but not in requirements_skills:)"
            )
        for skill in sorted(listed - actual_skills):
            errors.append(
                f"  {pf.relative_to(ROOT)}: stale entry {skill!r} "
                f"(listed in requirements_skills: but skills/requirements/{skill}/ does not exist)"
            )

    if not listed_any and actual_skills:
        errors.append(
            "  no profiles/*.yaml declares requirements_skills: "
            f"but skills/requirements/ contains {sorted(actual_skills)}"
        )
    return errors


def check_check_registries() -> list[str]:
    """Check registry IDs and their advertised ranges in consumers."""
    errors: list[str] = []
    for registry_path, prefix, final_number, consumers in CHECK_REGISTRIES:
        registry = ROOT / registry_path
        if not registry.exists():
            errors.append(f"  MISSING: {registry_path}")
            continue
        text = registry.read_text(encoding="utf-8")
        found = {
            int(match)
            for match in re.findall(
                rf"^\|\s*{re.escape(prefix)}(\d+)\s*\|",
                text,
                flags=re.MULTILINE,
            )
        }
        expected = set(range(1, final_number + 1))
        if found != expected:
            errors.append(
                f"  {registry_path}: {prefix} IDs are {sorted(found)}, "
                f"expected {sorted(expected)}"
            )
        advertised = f"{prefix}1–{prefix}{final_number}"
        if advertised not in text:
            errors.append(f"  {registry_path}: heading must advertise {advertised}")
        for consumer_path in consumers:
            consumer = ROOT / consumer_path
            if not consumer.exists():
                errors.append(f"  MISSING consumer: {consumer_path}")
                continue
            if advertised not in consumer.read_text(encoding="utf-8"):
                errors.append(
                    f"  {consumer_path}: must reference complete range {advertised}"
                )
    return errors


def check_required_tokens() -> list[str]:
    """Validate producer/consumer template fields and canonical sections."""
    errors: list[str] = []
    for relative_path, tokens in REQUIRED_TOKENS.items():
        path = ROOT / relative_path
        if not path.exists():
            errors.append(f"  MISSING: {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"  {relative_path}: missing required token {token!r}")
    return errors


def check_forbidden_workflow_text() -> list[str]:
    """Reject known stale workflow contracts."""
    errors: list[str] = []
    for relative_path, forbidden_values in FORBIDDEN_WORKFLOW_TEXT.items():
        path = ROOT / relative_path
        paths = list(path.rglob("*.md")) if path.is_dir() else [path]
        for candidate in paths:
            if not candidate.exists():
                continue
            text = candidate.read_text(encoding="utf-8")
            for forbidden in forbidden_values:
                if forbidden in text:
                    errors.append(
                        f"  {candidate.relative_to(ROOT)}: stale workflow text "
                        f"{forbidden!r}"
                    )
    return errors


def check_local_markdown_links() -> list[str]:
    """Ensure repository-local Markdown links resolve."""
    errors: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for raw_target in link_re.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:"))
                or "{" in target
                or "}" in target
            ):
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"  {source.relative_to(ROOT)}: broken local link {raw_target!r}"
                )
    return errors


def check_profile_contracts() -> list[str]:
    """Check stack-neutral layout keys required by development skills."""
    errors: list[str] = []
    required_dev_keys = {
        "constitution:",
        "rules_glob:",
        "product_spec_dir:",
        "as_built:",
        "adr_dir:",
        "reports_dir:",
        "tests_readme:",
        "source_roots:",
        "unit_tests_dir:",
        "live_verify_dir:",
        "debug_tests_dir:",
    }
    for profile in (ROOT / "profiles").glob("*.yaml"):
        text = profile.read_text(encoding="utf-8")
        if "development_skills:" in text:
            for key in sorted(required_dev_keys):
                if key not in text:
                    errors.append(
                        f"  {profile.relative_to(ROOT)}: missing layout key {key}"
                    )
        if "requirements_skills:" in text and "reports_dir:" not in text:
            errors.append(
                f"  {profile.relative_to(ROOT)}: missing layout key reports_dir:"
            )
    return errors


def check_delivery_contract_surface() -> list[str]:
    """Check portable workflow files and handoff instructions are present."""
    errors: list[str] = []
    for relative_path in DELIVERY_CONTRACT_FILES:
        if not (ROOT / relative_path).is_file():
            errors.append(f"  MISSING: {relative_path}")

    for skill_file in SKILLS_DIR.glob("*/*/SKILL.md"):
        text = skill_file.read_text(encoding="utf-8")
        if "## Workflow handoff" not in text:
            errors.append(
                f"  {skill_file.relative_to(ROOT)}: missing Workflow handoff section"
            )
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

    errors = check_profile_registry()
    if errors:
        all_errors.append(("Every skills/development/*/ must be listed in every profiles/*.yaml development_skills:", errors))

    errors = check_requirements_profile_registry()
    if errors:
        all_errors.append(("Every skills/requirements/*/ must be listed in profiles requirements_skills:", errors))

    errors = check_check_registries()
    if errors:
        all_errors.append(("Check registries and advertised ranges must agree", errors))

    errors = check_required_tokens()
    if errors:
        all_errors.append(("Workflow producer/consumer contracts must be complete", errors))

    errors = check_forbidden_workflow_text()
    if errors:
        all_errors.append(("Known stale workflow contracts must not reappear", errors))

    errors = check_local_markdown_links()
    if errors:
        all_errors.append(("Repository-local Markdown links must resolve", errors))

    errors = check_profile_contracts()
    if errors:
        all_errors.append(("Harness profiles must satisfy layout contracts", errors))

    errors = check_delivery_contract_surface()
    if errors:
        all_errors.append(("Delivery contract and skill handoffs must be complete", errors))

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
