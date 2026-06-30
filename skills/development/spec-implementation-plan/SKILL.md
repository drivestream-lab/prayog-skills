---
name: spec-implementation-plan
description: >-
  After feasibility sign-off, produce a wave-level implementation plan with
  REQ/TASK/FILE/TEST tables for an initiative. Use when the dev needs an execution
  plan before feature branches, or after spec merge.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
---

# Spec implementation plan

Turn an accepted initiative spec (+ feasibility report) into an **executable plan**. **Do not implement** — plan only.

Table shape borrowed from awesome-copilot `create-implementation-plan` (REQ/TASK/FILE/TEST/RISK).

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Every TASK has **done when** criteria and test/verify command from profile toolchain where applicable.
3. Plan scope must not exceed the initiative spec.
4. Dual output: chat summary + saved plan file.
5. Run T0–T5 control loop.

## Inputs

Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **Initiative spec** — merged or final (REQUIRED)
2. **Feasibility report** — if exists (RECOMMENDED)
3. **As-built**, **tests_readme**, **live_verify_dir** layout (REQUIRED for test tasks)
4. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)
5. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
6. **`adr_dir`** — architecture decision records (REQUIRED). Run relevant-ADR pass per [../references/governance.md](../references/governance.md) before T2 Analyze.

## Prerequisite

Run **after** feasibility is accepted (no blocking PM questions), ideally after spec is on `develop`.

## Process

1. **T0 Gather** — spec waves, feasibility findings, repo layout
2. **T1 Understand** — initiative id, wave boundaries, PR granularity from spec
3. **T2 Analyze** — map each wave to concrete files and tests; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs as **MDC notes** / **ADR notes** in the TASK table
4. **T3 Plan** — build REQ/TASK/FILE tables per wave; add draft-ADR TASK when plan flags `NEW-ADR`
5. **T4 Execute** — write plan; run P1–P12 checks
6. **T5 Verify** — self-contained plan readable by a fresh session

## Output

Save to `{reports_dir}/{plan_prefix}-{initiative}.md`.

Use [references/output-template.md](references/output-template.md).
