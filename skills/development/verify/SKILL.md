---
name: verify
description: >-
  Define or run live verify discipline for a feature — one live-verify artifact
  per product area, no overlap with unit tests. Use when finishing a slice, adding
  live-verify tests, or when asked what command proves the feature on a running stack.
disable-model-invocation: true
paths: AGENTS.md, tests/**, docs/specification/as-built/**
---

# Verify

Clarify **live verify** vs **unit** for one feature, or run verify when asked.

Read `AGENTS.md`, `tests_readme`, and `rules_glob` (include testing-verify rule when present). Policy: [references/verify-policy.md](references/verify-policy.md). Paths: `.harness/profile.yaml` or [references/layout-defaults.md](../pre-implement/references/layout-defaults.md).

## Rules

Resolve `unit_tests_dir`, `live_verify_dir`, `debug_tests_dir` from profile.

| Layer | Location (profile key) | Proves |
|-------|------------------------|--------|
| Unit | `unit_tests_dir` | Logic, branches, edge cases |
| Verify | `live_verify_dir` | Product feature on **running** stack |
| Debug | `debug_tests_dir` | Exploration — not gating |

**No overlap:** do not assert the same behavior in unit and verify for the same feature.

## Toolchain vs live verify

Commands come from `tests_readme` and profile toolchain — do not hardcode stack-specific commands in the skill.

Do not skip prerequisites (running server, config files, bootstrap scripts) documented in `tests_readme`.

## Output format (plan mode)

```markdown
## Verify plan — FEATURE

### Unit scope
- What to test in {unit_tests_dir} (no live stack)

### Verify script
- Path: {live_verify_dir}/...
- Prerequisites: (from tests_readme)
- Command: ...
- Pass criteria: exit 0, expected shape / behavior

### As-built row
- Update implementation-status.md: unit-tested / live-verified

### Overlap check
- Confirm no duplicate assertions vs unit
```

## Run mode

If the user asks to **run** verify: state the exact command from `tests_readme` and tracker **Verify command**; run it when the environment is available; report pass/fail.

## Workflow handoff

Emit the envelope from `../../../references/handoff-envelope.md` in the verify
result and persist the command/evidence in the tracker or report. Use stage
`verify`.

- `pass` / justified `skipped` → `ground-spec`
- `findings` / `failed` → `loop-spec`
- `blocked` → human decision

Never mark `pass` without command output or equivalent reproducible evidence.
