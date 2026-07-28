#!/usr/bin/env python3
"""Prompt-package contract helpers for skill invocation briefs.

Layout (per skill under skills/requirements/ or skills/development/):

    prompts/
      template.md
      schema.yaml
      fixtures/
        happy_path.inputs.yaml
        happy_path.expected.md

Simple ``{{var}}`` substitution only — no filters, conditionals, or partials.
Coverage is directory-based and independent of workflow ``dispatch``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover — CI installs PyYAML
    yaml = None  # type: ignore[assignment]

# Normative v1 shared variable dictionary (PRD INIT-PRAYOG-SKILLS-003-PROMPTS).
SHARED_VARIABLES: dict[str, dict[str, Any]] = {
    "ticket": {"required": True, "type": "string"},
    "initiative": {"required": False, "type": "string"},
    "handoff_path": {"required": True, "type": "string"},
    "workspace": {"required": True, "type": "string"},
    "skill_id": {"required": True, "type": "string"},
}

PROMPT_AREAS = frozenset({"requirements", "development", "forge"})

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
VAR_RE = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
# Reject template engines beyond simple {{var}}.
FORBIDDEN_TEMPLATE_RE = re.compile(
    r"(\{\%|\%\}|\{\#|\#\}|\{\{[^{}]*\|[^{}]*\}\}|\{\{[^{}]*\?[^{}]*\}\})"
)


def normalize_text(text: str) -> str:
    """Normalize rendered text for golden fixture comparison."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in normalized.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    while lines and lines[0] == "":
        lines.pop(0)
    return "\n".join(lines)


def extract_template_vars(template: str) -> list[str]:
    """Return ordered unique ``{{var}}`` names from a template."""
    seen: set[str] = set()
    ordered: list[str] = []
    for match in VAR_RE.finditer(template):
        name = match.group(1)
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def is_semver(revision: str) -> bool:
    return bool(SEMVER_RE.fullmatch(revision))


def load_yaml(path: Path) -> Any:
    if yaml is None:
        raise RuntimeError("PyYAML is required for prompt package checks")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render(template: str, bound_inputs: dict[str, str]) -> str:
    """Substitute simple ``{{var}}`` placeholders; missing optional → empty."""

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        value = bound_inputs.get(name)
        if value is None:
            return ""
        return str(value)

    return VAR_RE.sub(repl, template)


def validate_bound_inputs(
    variables: dict[str, Any],
    bound_inputs: dict[str, Any],
) -> list[str]:
    """Fail closed when required bound inputs are missing or empty."""
    errors: list[str] = []
    for name, spec in variables.items():
        required = bool(spec.get("required"))
        raw = bound_inputs.get(name)
        if required and (raw is None or str(raw).strip() == ""):
            errors.append(f"missing required bound input: {name}")
    return errors


def validate_schema(
    schema: dict[str, Any],
    *,
    expected_prompt_id: str | None = None,
) -> list[str]:
    """Validate schema.yaml shape and normative v1 shared-variable defaults."""
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["schema must be a mapping"]

    prompt_id = schema.get("prompt_id")
    if not isinstance(prompt_id, str) or not prompt_id.strip():
        errors.append("schema.prompt_id must be a non-empty string")
    elif expected_prompt_id is not None and prompt_id != expected_prompt_id:
        errors.append(
            f"schema.prompt_id {prompt_id!r} != skill id {expected_prompt_id!r}"
        )

    revision = schema.get("revision")
    if not isinstance(revision, str) or not is_semver(revision):
        errors.append(
            f"schema.revision must be semver MAJOR.MINOR.PATCH, got {revision!r}"
        )

    variables = schema.get("variables")
    if not isinstance(variables, dict) or not variables:
        errors.append("schema.variables must be a non-empty mapping")
        return errors

    expected_names = set(SHARED_VARIABLES)
    actual_names = set(variables)
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        if missing:
            errors.append(f"schema.variables missing shared names: {missing}")
        if extra:
            errors.append(f"schema.variables has unknown names: {extra}")

    for name, expected in SHARED_VARIABLES.items():
        if name not in variables:
            continue
        spec = variables[name]
        if not isinstance(spec, dict):
            errors.append(f"variables.{name} must be a mapping")
            continue
        if bool(spec.get("required")) != bool(expected["required"]):
            errors.append(
                f"variables.{name}.required must be {expected['required']} (v1 normative)"
            )
        if spec.get("type") != expected["type"]:
            errors.append(
                f"variables.{name}.type must be {expected['type']!r} (v1 normative)"
            )
    return errors


def validate_template(template: str, variables: dict[str, Any]) -> list[str]:
    """Reject advanced template syntax; require declared variables only."""
    errors: list[str] = []
    if FORBIDDEN_TEMPLATE_RE.search(template):
        errors.append(
            "template uses forbidden syntax (filters/conditionals/partials); "
            "simple {{var}} only"
        )
    declared = set(variables)
    for name in extract_template_vars(template):
        if name not in declared:
            errors.append(f"template references undeclared variable: {{{{{name}}}}}")
    return errors


def package_dir(skill_root: Path) -> Path:
    return skill_root / "prompts"


def validate_prompt_package(skill_root: Path, *, skill_id: str) -> list[str]:
    """Validate one skill prompt package. Returns human-readable error lines."""
    errors: list[str] = []
    prompts = package_dir(skill_root)
    template_path = prompts / "template.md"
    schema_path = prompts / "schema.yaml"
    fixtures = prompts / "fixtures"
    inputs_path = fixtures / "happy_path.inputs.yaml"
    expected_path = fixtures / "happy_path.expected.md"

    if not prompts.is_dir():
        return [f"missing prompts/ directory under {skill_root}"]
    for path, label in (
        (template_path, "prompts/template.md"),
        (schema_path, "prompts/schema.yaml"),
        (inputs_path, "prompts/fixtures/happy_path.inputs.yaml"),
        (expected_path, "prompts/fixtures/happy_path.expected.md"),
    ):
        if not path.is_file():
            errors.append(f"missing {label}")

    if errors:
        return errors

    try:
        schema = load_yaml(schema_path)
    except Exception as exc:  # noqa: BLE001 — surface parse errors to callers
        return [f"schema.yaml parse error: {exc}"]

    schema_errors = validate_schema(schema, expected_prompt_id=skill_id)
    errors.extend(schema_errors)
    if schema_errors:
        return errors

    template = template_path.read_text(encoding="utf-8")
    variables = schema["variables"]
    errors.extend(validate_template(template, variables))

    # Orchestrator baton dual-write must be explicit in packaged templates.
    if "Prefer the latest handoff artifact" in template:
        errors.append(
            "template treats handoff_path as read-only preference; "
            "must require overwrite of {{handoff_path}}"
        )
    if "## Handoff baton" not in template:
        errors.append("template missing ## Handoff baton section")
    if "overwrite" not in template.lower() or "{{handoff_path}}" not in template:
        errors.append(
            "template must instruct overwrite of {{handoff_path}} with handoff envelope"
        )
    if "## Envelope navigation (required)" not in template:
        errors.append("template missing ## Envelope navigation (required) section")
    if "human-checkpoint" not in template or "workflow.yaml" not in template:
        errors.append(
            "template must instruct deriving human_checkpoint from workflow.yaml "
            "next node type"
        )

    try:
        bound = load_yaml(inputs_path) or {}
    except Exception as exc:  # noqa: BLE001
        errors.append(f"happy_path.inputs.yaml parse error: {exc}")
        return errors

    if not isinstance(bound, dict):
        errors.append("happy_path.inputs.yaml must be a mapping")
        return errors

    bound_str = {str(k): "" if v is None else str(v) for k, v in bound.items()}
    errors.extend(validate_bound_inputs(variables, bound_str))

    rendered = normalize_text(render(template, bound_str))
    expected = normalize_text(expected_path.read_text(encoding="utf-8"))
    if rendered != expected:
        errors.append(
            "golden fixture mismatch: render(template, happy_path.inputs) "
            "!= happy_path.expected.md (after normalize)"
        )
    return errors


def iter_prompt_skill_dirs(root: Path) -> list[tuple[str, str, Path]]:
    """Return (area, skill_id, skill_root) for requirements + development + forge."""
    skills_dir = root / "skills"
    found: list[tuple[str, str, Path]] = []
    for area in sorted(PROMPT_AREAS):
        area_dir = skills_dir / area
        if not area_dir.is_dir():
            continue
        for skill_root in sorted(p for p in area_dir.iterdir() if p.is_dir()):
            if not (skill_root / "SKILL.md").is_file():
                continue
            found.append((area, skill_root.name, skill_root))
    return found
