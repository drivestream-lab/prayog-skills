---
name: pre-implement
description: >-
  Before implementing one spec slice in a Python backend service, produce a
  read-and-update checklist from AGENTS.md, product specs, as-built, and tests.
  Use when starting implementation, opening a feature branch, or when asked
  what to read before coding.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**
---

# Pre-implement (Python backend)

Design the **pre-flight checklist** for one implementation slice. **Do not write product code** unless the user explicitly asks after the checklist.

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present; else [references/layout-defaults.md](references/layout-defaults.md).
2. Read `.cursor/rules/*.mdc` — do not edit rules in the app repo.
3. Output the checklist only unless the user asks to implement.
4. Cite concrete file paths for this repo and slice.

## Read order

1. `AGENTS.md` — constitution pin, verify summary, process links
2. `.cursor/rules/*.mdc` — how to build
3. Initiative / slice spec — path from user or tracker **Spec path** (e.g. `product/<initiative>.md`), then canon docs (`00-service-profile.md`, `02-api-contract.md`, domain specs as needed)
4. Relevant `adr/` if architecture or contracts change
5. `as-built/implementation-status.md` — live/deferred + verification matrix
6. `tests/README.md` — when the slice adds or changes tests (commands, feature map)

**Testing harness (conditional):** read the harness section in as-built only when changing `tests/` layout, `testpaths`, CI vs live boundaries, or unit/verify overlap policy.

**Cross-service:** read cross-service / integration product docs when peer services or shared contracts are touched.

**Prior plan:** if `reports/Implementation-Plan-<initiative>.md` exists, read the wave/section for this slice.

## Output format

Use [references/output-template.md](references/output-template.md). Fill concrete paths for the user's repo and slice.
