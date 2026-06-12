---
name: verify
description: >-
  Define or run live verify discipline for a Python backend feature — one verify
  script per product area, no overlap with unit tests. Use when finishing a slice,
  adding tests/verify/, or when asked what command proves the feature on a running stack.
disable-model-invocation: true
paths: AGENTS.md, tests/**, docs/specification/as-built/**
---

# Verify (Python backend)

Clarify **live verify** vs **unit** for one feature, or run verify when asked.

Read `AGENTS.md`, `tests/README.md`, and `.cursor/rules/testing-verify-flows.mdc`. Policy: [references/verify-policy.md](references/verify-policy.md). Paths: `.harness/profile.yaml` or [references/layout-defaults.md](../pre-implement/references/layout-defaults.md).

## Rules

| Layer | Location | Proves |
|-------|----------|--------|
| Unit | `tests/unit/` | Logic, branches, edge cases |
| Verify | `tests/verify/` | Product feature on **running** service |
| Debug | `tests/debug/` | Exploration — not gating |

**No overlap:** do not assert the same behavior in unit and verify for the same feature.

## Toolchain vs live verify

| Task | Typical command |
|------|-----------------|
| Toolchain (no live server) | `make check`, `make test` |
| Live verify | See `tests/README.md` |

Do not skip prerequisites (running server, config files, bootstrap scripts) documented in `tests/README.md`.

## Output format (plan mode)

```markdown
## Verify plan — FEATURE

### Unit scope
- What to test in tests/unit/ (no live server)

### Verify script
- Path: tests/verify/...
- Prerequisites: (from tests/README.md)
- Command: ...
- Pass criteria: exit 0, response shape

### As-built row
- Update implementation-status.md: unit-tested / live-verified

### Overlap check
- Confirm no duplicate assertions vs unit
```

## Run mode

If the user asks to **run** verify: state the exact command from `tests/README.md` and tracker **Verify command**; run it when the environment is available; report pass/fail.
