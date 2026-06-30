---
name: pre-implement
description: >-
  Before implementing one spec slice, produce a read-and-update checklist from
  AGENTS.md, ADRs, MDC rules, product specs, as-built, and tests. Use when
  starting implementation, opening a feature branch, or when asked what to read
  before coding.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
---

# Pre-implement

Design the **pre-flight checklist** for one implementation slice. **Do not write product code** unless the user explicitly asks after the checklist.

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present; else [references/layout-defaults.md](references/layout-defaults.md).
2. Read `rules_glob` — do not edit rules in the app repo.
3. Read relevant ADRs from `adr_dir` per [../references/governance.md](../references/governance.md) — list ids in output.
4. Output the checklist only unless the user asks to implement.
5. Cite concrete file paths for this repo and slice.

## Read order

1. `AGENTS.md` — constitution pin, verify summary, process links
2. `rules_glob` — how to build (MDC)
3. **Relevant ADRs** — from `adr_dir`; include cross-cutting ADRs from `AGENTS.md`; match slice scope (API, auth, BFF, data, deployment, …)
4. Initiative / slice spec — path from user or tracker **Spec path** (e.g. `product/<initiative>.md`), then canon docs as listed in profile or spec
5. `as-built/implementation-status.md` — live/deferred + verification matrix
6. `tests_readme` — when the slice adds or changes tests (commands, feature map)

**Testing harness (conditional):** read the harness section in as-built only when changing test layout, CI vs live boundaries, or unit/live-verify overlap policy.

**Cross-service:** read cross-service / integration product docs when peer services or shared contracts are touched.

**Prior plan:** if `reports/Implementation-Plan-<initiative>.md` exists, read the wave/section for this slice; carry forward **MDC notes** and **ADR notes** from TASK rows.

## Output format

Use [references/output-template.md](references/output-template.md). Fill concrete paths for the user's repo and slice.
