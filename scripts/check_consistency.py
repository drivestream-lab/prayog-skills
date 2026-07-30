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

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover — CI installs PyYAML
    yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
DISPATCH_ENUM = frozenset({"manual", "orchestrated"})
COMMIT_WORKSPACE_ENUM = frozenset({"disabled", "optional", "required"})
FORGE_ACTION_ENUM = frozenset(
    {"commit_workspace", "open_draft_pr", "create_board_tickets"}
)

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
    (
        "Skills must not instruct creating *-revN / *-v2 report siblings as outputs",
        r"(?:save|write|create)\s+(?:as\s+)?`?(?:Validation-Report|Resolution|Impact-Map)[^`\n]*-(?:rev\d+|v\d+)\.md",
        set(),
        "**/*.md",
    ),
    (
        "Plans must not use shadow REQ-W{digit} product ids",
        r"\| REQ-W\d",
        set(),
        "**/spec-implementation-plan/**/*.md",
    ),
    (
        "Prompt templates must not treat handoff_path as read-only preference",
        r"Prefer the latest handoff artifact at `\{\{handoff_path\}\}`",
        set(),  # must not appear
        "**/prompts/template.md",
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
        12,
        [
            "skills/development/spec-technical-review/SKILL.md",
            "skills/development/spec-technical-review/references/output-template.md",
        ],
    ),
    (
        "skills/development/spec-implementation-plan/references/checks.md",
        "P",
        16,
        [
            "skills/development/spec-implementation-plan/SKILL.md",
            "skills/development/spec-implementation-plan/references/output-template.md",
        ],
    ),
    (
        "skills/development/ground-spec/references/checks.md",
        "G",
        10,
        [
            "skills/development/ground-spec/SKILL.md",
            "skills/development/ground-spec/references/output-template.md",
        ],
    ),
    (
        "skills/forge/create-board-tickets/references/checks.md",
        "B",
        8,
        [
            "skills/forge/create-board-tickets/SKILL.md",
            "skills/forge/create-board-tickets/references/output-template.md",
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
        "All T1–T12 checks",
        "T12 Product-boundary",
        "FF-",
        "approved REQ-",
    ],
    "skills/development/spec-technical-review/references/adr-template.md": [
        "product_constraints",
        "supersedes",
        "superseded_by",
        "changes_user_visible_behavior",
        "Product decisions excluded",
    ],
    "skills/development/spec-implementation-plan/references/output-template.md": [
        "## Source freshness and command contract",
        "Spec path",
        "## 9. WorkManifest seed",
        "Implements",
        "tasks:",
        "TASK-W0-01",
        "Workflow outcome",
        "apiVersion: prayog/v1",
        "depends_on:",
        "exit:",
        "criteria:",
        "evidence_expected:",
        "Verification Coverage",
        "Live-verification intent",
        "stop_conditions:",
        "cleanup:",
        "workmanifest-contract.md",
        "P1–P16",
    ],
    "skills/development/pre-implement/references/output-template.md": [
        "Plan source freshness",
        "`check_command`",
        "`ground_command`",
        "TASK-W{N}-01",
        "Pre-Implement-",
        "Bound by Forge/human context",
        "WorkManifest contract",
        "TASK exit proof",
        "Live-verification contract",
    ],
    "skills/development/ground-spec/references/output-template.md": [
        "GF-",
        "wave-signoff",
        "reviewed head",
        "G1–G10",
    ],
    "skills/development/loop-spec/SKILL.md": [
        "Wave-Execution-",
        "commit_workspace",
        "Never commit",
        "WorkManifest",
        "dependency order",
        "Do **not** mutate",
    ],
    "skills/development/verify/SKILL.md": [
        "Live-Verify-",
        "expected",
        "observed",
        "Integration / contract",
        "Smoke",
        "Sandbox",
    ],
    "skills/forge/create-board-tickets/references/output-template.md": [
        "workmanifest-contract-pass",
        "Preserved task metadata",
        "B1–B8",
    ],
    "skills/requirements/validate-requirements/output-templates.md": [
        "report_revision",
        "Validation-Report-{INIT}.md",
        "VF-01",
    ],
    "skills/requirements/review-findings/SKILL.md": [
        "Resolution-{INIT}.md",
        "Decision brief",
        "CHG-",
        "VF-",
    ],
    "references/id-conventions.md": [
        "REQ-{nn}",
        "VF-{nn}",
        "TASK-W{n}-{nn}",
        "GF-",
        "P1",
        "P16",
        "T12",
        "G1",
        "G10",
    ],
    "references/artifact-write-contract.md": [
        "Validation-Report-{INIT}.md",
        "Never create",
        "map_revision",
        "Pre-Implement-{INIT}-W{N}.md",
        "Wave-Execution-{INIT}-W{N}.md",
        "Live-Verify-{INIT}-W{N}.md",
        "Ground-Report-{SPEC}-W{N}.md",
    ],
}

FORBIDDEN_WORKFLOW_TEXT = {
    "skills/development/spec-technical-review": [
        "T1–T10",
        "T1-T10",
        "T1–T11",
        "T1-T11",
        "All T1–T11",
    ],
    "skills/development/spec-implementation-plan": [
        "P14 | **WorkManifest seed** — §8",
        "apiVersion: launchpad/v1",
        "launchpad WorkManifest",
    ],
    "skills/development/loop-spec/SKILL.md": [
        "Human explicitly approves → `/ground-spec`",
        "When TASK is green: commit",
    ],
    "skills/development/ground-spec": [
        "check every REQ in product spec",
        "Commit this report",
    ],
    "skills/development/pre-implement": [
        "unless the user asks",
        "unless user asks",
    ],
}

DELIVERY_CONTRACT_FILES = [
    "delivery-contract.yaml",
    "workflow.yaml",
    "references/handoff-envelope.md",
    "references/prompt-package-contract.md",
    "references/forge-side-effects.md",
    "references/workmanifest-contract.md",
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


def check_forge_profile_registry() -> list[str]:
    """Every skills/forge/*/SKILL.md must appear in every profile forge_skills."""
    errors: list[str] = []
    forge_dir = SKILLS_DIR / "forge"
    if not forge_dir.exists():
        return errors
    actual_skills = {p.parent.name for p in forge_dir.glob("*/SKILL.md")}
    profile_files = list((ROOT / "profiles").glob("*.yaml"))
    block_re = re.compile(r"forge_skills:\s*\n((?:[ \t]*-[ \t]*\S+[ \t]*\n?)+)")
    item_re = re.compile(r"-\s*(\S+)")

    if not profile_files:
        return ["  no profiles/*.yaml found"]

    for pf in profile_files:
        text = pf.read_text(encoding="utf-8")
        m = block_re.search(text)
        if not m:
            errors.append(
                f"  {pf.relative_to(ROOT)}: missing forge_skills: "
                f"(required for launchpad materialize)"
            )
            continue
        listed = set(item_re.findall(m.group(1)))
        for skill in sorted(actual_skills - listed):
            errors.append(
                f"  {pf.relative_to(ROOT)}: missing {skill!r} in forge_skills:"
            )
        for skill in sorted(listed - actual_skills):
            errors.append(
                f"  {pf.relative_to(ROOT)}: stale forge_skills entry {skill!r}"
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

    contract_path = ROOT / "delivery-contract.yaml"
    if contract_path.is_file():
        contract_text = contract_path.read_text(encoding="utf-8")
        for token in (
            "workmanifest_spec: references/workmanifest-contract.md",
            "apiVersion: prayog/v1",
            "kind: WorkManifest",
            "immutable-approved-execution-intent",
        ):
            if token not in contract_text:
                errors.append(
                    f"  delivery-contract.yaml: missing WorkManifest registration token {token!r}"
                )

    workflow_path = ROOT / "workflow.yaml"
    if workflow_path.is_file():
        workflow_text = workflow_path.read_text(encoding="utf-8")
        if "workmanifest-p14-pass" in workflow_text:
            errors.append(
                "  workflow.yaml: stale predicate workmanifest-p14-pass "
                "(use workmanifest-contract-pass)"
            )
        if "workmanifest-contract-pass" not in workflow_text:
            errors.append(
                "  workflow.yaml: missing documented predicate workmanifest-contract-pass"
            )

    for skill_file in SKILLS_DIR.glob("*/*/SKILL.md"):
        # engg-reviews is an adjunct pack — not on sdd-delivery workflow.
        if "engg-reviews" in skill_file.parts:
            continue
        text = skill_file.read_text(encoding="utf-8")
        if "## Workflow handoff" not in text:
            errors.append(
                f"  {skill_file.relative_to(ROOT)}: missing Workflow handoff section"
            )
            continue
        # Prompt-packaged lanes must dual-write orchestrator baton when bound.
        if "requirements" in skill_file.parts or "development" in skill_file.parts:
            handoff_idx = text.find("## Workflow handoff")
            handoff_chunk = text[handoff_idx : handoff_idx + 2000]
            if "handoff_path" not in handoff_chunk:
                errors.append(
                    f"  {skill_file.relative_to(ROOT)}: Workflow handoff must "
                    "require write to handoff_path baton"
                )
            if "overwrite" not in handoff_chunk.lower():
                errors.append(
                    f"  {skill_file.relative_to(ROOT)}: Workflow handoff must "
                    "require overwrite of handoff_path baton"
                )
            if "Derive `next_candidates`" not in handoff_chunk:
                errors.append(
                    f"  {skill_file.relative_to(ROOT)}: Workflow handoff must "
                    "require deriving next_candidates/human_checkpoint from workflow.yaml"
                )
            if "human-checkpoint" not in handoff_chunk:
                errors.append(
                    f"  {skill_file.relative_to(ROOT)}: Workflow handoff must "
                    "tie human_checkpoint to next node type human-checkpoint"
                )
    return errors


def check_workflow_dispatch_and_purpose() -> list[str]:
    """Assert dispatch on skills and purpose on human-checkpoints (YAML SSOT)."""
    errors: list[str] = []
    if yaml is None:
        return ["  MISSING dependency: PyYAML (required for workflow dispatch checks)"]

    workflow_path = ROOT / "workflow.yaml"
    policy_path = ROOT / "tests" / "fixtures" / "workflow_dispatch_policy.json"
    if not workflow_path.is_file():
        return ["  MISSING: workflow.yaml"]
    if not policy_path.is_file():
        return ["  MISSING: tests/fixtures/workflow_dispatch_policy.json"]

    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    nodes = workflow.get("nodes") or {}
    orchestrated = set(policy.get("orchestrated") or [])
    manual = set(policy.get("manual") or [])
    purposes = policy.get("human_checkpoint_purposes") or {}

    skill_nodes = {s for s, n in nodes.items() if n.get("type") == "skill"}
    if skill_nodes != orchestrated | manual:
        errors.append(
            f"  policy fixture skill set mismatch: workflow={sorted(skill_nodes)} "
            f"policy={sorted(orchestrated | manual)}"
        )
    if orchestrated & manual:
        errors.append(f"  policy fixture overlap: {sorted(orchestrated & manual)}")

    for stage, node in nodes.items():
        ntype = node.get("type")
        if ntype == "gate":
            errors.append(f"  {stage}: forbidden type: gate (use human-checkpoint)")
        if ntype == "skill":
            dispatch = node.get("dispatch")
            if dispatch not in DISPATCH_ENUM:
                errors.append(
                    f"  {stage}: skill requires dispatch in {sorted(DISPATCH_ENUM)}"
                )
            elif stage in orchestrated and dispatch != "orchestrated":
                errors.append(f"  {stage}: expected dispatch: orchestrated")
            elif stage in manual and dispatch != "manual":
                errors.append(f"  {stage}: expected dispatch: manual")
            if "purpose" in node:
                errors.append(f"  {stage}: purpose is only for human-checkpoint nodes")
        elif ntype == "human-checkpoint":
            purpose = node.get("purpose")
            if not isinstance(purpose, str) or not purpose.strip():
                errors.append(f"  {stage}: human-checkpoint requires purpose")
            elif stage in purposes and purpose != purposes[stage]:
                errors.append(
                    f"  {stage}: purpose {purpose!r} != policy {purposes[stage]!r}"
                )
            if "dispatch" in node:
                errors.append(f"  {stage}: dispatch is only for skill nodes")
        else:
            if "dispatch" in node:
                errors.append(f"  {stage}: dispatch is only for skill nodes")
            if "purpose" in node:
                errors.append(f"  {stage}: purpose is only for human-checkpoint nodes")

    checkpoint_ids = {
        s for s, n in nodes.items() if n.get("type") == "human-checkpoint"
    }
    if set(purposes) != checkpoint_ids:
        errors.append(
            f"  human_checkpoint_purposes keys mismatch: "
            f"workflow={sorted(checkpoint_ids)} policy={sorted(purposes)}"
        )
    return errors


def check_workflow_forge() -> list[str]:
    """Assert forge.commit_workspace on skills and forge on PR external-actions."""
    errors: list[str] = []
    if yaml is None:
        return ["  MISSING dependency: PyYAML (required for workflow forge checks)"]

    workflow_path = ROOT / "workflow.yaml"
    policy_path = ROOT / "tests" / "fixtures" / "workflow_forge_policy.json"
    if not workflow_path.is_file():
        return ["  MISSING: workflow.yaml"]
    if not policy_path.is_file():
        return ["  MISSING: tests/fixtures/workflow_forge_policy.json"]

    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    nodes = workflow.get("nodes") or {}
    commit_policy = policy.get("commit_workspace") or {}
    ea_policy = policy.get("external_action_forge") or {}
    auth_policy = policy.get("external_action_authorization") or {}
    skill_map = policy.get("human_forge_skills") or {}
    forbid_suffix = policy.get("forbid_auto_label_suffix") or "-lgtm"
    auth_enum = frozenset({"explicit", "automated"})

    skill_nodes = {s for s, n in nodes.items() if n.get("type") == "skill"}
    if set(commit_policy) != skill_nodes:
        errors.append(
            f"  forge commit_workspace keys mismatch: "
            f"workflow={sorted(skill_nodes)} policy={sorted(commit_policy)}"
        )

    ea_nodes = {s for s, n in nodes.items() if n.get("type") == "external-action"}
    if set(auth_policy) != ea_nodes:
        errors.append(
            f"  external_action_authorization keys mismatch: "
            f"workflow={sorted(ea_nodes)} policy={sorted(auth_policy)}"
        )

    for stage, node in nodes.items():
        ntype = node.get("type")
        forge = node.get("forge") or {}
        if ntype == "skill":
            cw = forge.get("commit_workspace")
            if cw not in COMMIT_WORKSPACE_ENUM:
                errors.append(
                    f"  {stage}: skill requires forge.commit_workspace in "
                    f"{sorted(COMMIT_WORKSPACE_ENUM)}"
                )
            elif stage in commit_policy and cw != commit_policy[stage]:
                errors.append(
                    f"  {stage}: commit_workspace {cw!r} != policy "
                    f"{commit_policy[stage]!r}"
                )
            if "action" in forge:
                errors.append(
                    f"  {stage}: forge.action belongs on external-action nodes"
                )
        elif ntype == "external-action":
            auth = node.get("authorization")
            if auth not in auth_enum:
                errors.append(
                    f"  {stage}: external-action requires authorization in "
                    f"{sorted(auth_enum)} (got {auth!r})"
                )
            elif stage in auth_policy and auth != auth_policy[stage]:
                errors.append(
                    f"  {stage}: authorization {auth!r} != policy "
                    f"{auth_policy[stage]!r}"
                )
            if stage in ea_policy:
                expected = ea_policy[stage]
                action = forge.get("action")
                if action != expected.get("action"):
                    errors.append(
                        f"  {stage}: forge.action {action!r} != "
                        f"{expected.get('action')!r}"
                    )
                if action is not None and action not in FORGE_ACTION_ENUM:
                    errors.append(
                        f"  {stage}: forge.action must be in "
                        f"{sorted(FORGE_ACTION_ENUM)}"
                    )
                if "draft" in expected and forge.get("draft") != expected.get("draft"):
                    errors.append(f"  {stage}: forge.draft mismatch policy")
                if "apply_labels" in expected and list(forge.get("apply_labels") or []) != list(
                    expected.get("apply_labels") or []
                ):
                    errors.append(f"  {stage}: forge.apply_labels mismatch policy")
                if list(forge.get("requires") or []) != list(
                    expected.get("requires") or []
                ):
                    errors.append(f"  {stage}: forge.requires mismatch policy")
            for label in forge.get("apply_labels") or []:
                if str(label).endswith(forbid_suffix):
                    errors.append(
                        f"  {stage}: forbid auto-apply label {label!r} "
                        f"(suffix {forbid_suffix})"
                    )
        elif "forge" in node and ntype not in {"skill", "external-action"}:
            errors.append(f"  {stage}: forge only on skill or external-action")

    for action, skill_id in skill_map.items():
        expected_id = action.replace("_", "-")
        if skill_id != expected_id:
            errors.append(
                f"  human_forge_skills: {action} → {skill_id!r} "
                f"(expected {expected_id!r})"
            )
        skill_file = ROOT / "skills" / "forge" / skill_id / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"  MISSING forge skill: skills/forge/{skill_id}/SKILL.md")
    return errors


def check_prompt_package_surface() -> list[str]:
    """Assert prompt packages for requirements + development inventory (not dispatch)."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from scripts.prompt_contract import (  # noqa: WPS433 — runtime path bootstrap
        iter_prompt_skill_dirs,
        validate_prompt_package,
    )

    errors: list[str] = []
    inventory_path = ROOT / "tests" / "fixtures" / "prompt_inventory.json"
    if not inventory_path.is_file():
        return ["  MISSING: tests/fixtures/prompt_inventory.json"]

    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    expected = {
        (entry["area"], entry["skill_id"]) for entry in inventory.get("skills") or []
    }
    found = {(area, skill_id) for area, skill_id, _ in iter_prompt_skill_dirs(ROOT)}

    if expected != found:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        if missing:
            errors.append(f"  inventory lists missing skill dirs: {missing}")
        if extra:
            errors.append(f"  skill dirs not in prompt inventory: {extra}")

    for area, skill_id, skill_root in iter_prompt_skill_dirs(ROOT):
        if (area, skill_id) not in expected:
            continue
        for line in validate_prompt_package(skill_root, skill_id=skill_id):
            errors.append(f"  {area}/{skill_id}: {line}")

    # Fail closed if engg-reviews accidentally gains prompt packages in inventory.
    for entry in inventory.get("skills") or []:
        if entry.get("area") == "engg-reviews":
            errors.append("  engg-reviews must not appear in prompt inventory")
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

    errors = check_forge_profile_registry()
    if errors:
        all_errors.append(
            ("Every skills/forge/*/ must be listed in every profiles/*.yaml forge_skills:", errors)
        )

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

    errors = check_workflow_dispatch_and_purpose()
    if errors:
        all_errors.append(
            ("Workflow dispatch/purpose must match policy fixture", errors)
        )

    errors = check_workflow_forge()
    if errors:
        all_errors.append(
            ("Workflow forge policy must match fixture and forbid *-lgtm", errors)
        )

    errors = check_prompt_package_surface()
    if errors:
        all_errors.append(
            (
                "Prompt packages required for skills/requirements/*, "
                "skills/development/*, and skills/forge/* (independent of dispatch)",
                errors,
            )
        )

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
