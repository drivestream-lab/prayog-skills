---
name: spec-feasibility-review
description: >-
  Review a product spec against the current codebase before merge — baseline,
  gaps, impact, test harness, architecture governance (ADR + MDC), risks, and PM
  questions. Use on spec handoff PRs or when asked about feasibility, impact, or
  what it takes to build.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
---

# Spec feasibility review

Assess whether an initiative spec is **buildable in this repo as it exists today**. **Do not implement** — flag only.

Pattern borrowed from awesome-copilot `create-github-issues-for-unmet-specification-requirements` (extract → search code → classify). Evaluation discipline aligned with `validate-requirements`.

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Evidence for every finding — spec quote + repo path (file, symbol, or test name).
3. Don't fix — flag. Do not edit product source or product specs unless the user explicitly asks after the report.
4. Dual output: chat summary + saved report file + numbered PM questions.
5. Run T0–T5 control loop (Gather → Understand → Analyze → Plan → Execute → Verify).

## Inputs

Gather before starting. Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **Initiative spec** — primary doc (REQUIRED), usually under `product_spec_dir`
2. **Upstream requirements** — PRD or parent doc if user provides path (OPTIONAL for conformance context)
3. **As-built** — `implementation-status.md` (REQUIRED)
4. **Tests** — `tests_readme`, `unit_tests_dir`, `live_verify_dir`, and toolchain config from profile (REQUIRED)
5. **Source** — modules under `source_roots` from profile, named or implied by spec (REQUIRED)
6. **Prior feasibility report** — for incremental re-run (OPTIONAL)
7. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)
8. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
9. **`adr_dir`** — architecture decision records (REQUIRED). Run relevant-ADR pass per [../references/governance.md](../references/governance.md) before T2 Analyze.

## When to use

- Dev reviewing a spec handoff PR before merge
- After PM updates spec — re-run on changed sections
- User asks: feasibility, impact, gap analysis, spec vs code

## Process

1. **T0 Gather** — inventory inputs; note missing paths
2. **T1 Understand** — initiative id, spec branch, review objective
3. **T2 Analyze** — read spec waves/capabilities; scan repo evidence; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs
4. **T3 Plan** — which checks run (full vs incremental)
5. **T4 Execute** — run checks F1–F14 per [references/checks.md](references/checks.md)
6. **T5 Verify** — save report; publish summary + PM questions (blocking vs defer)

## Output

Save to `{reports_dir}/{feasibility_prefix}-{initiative}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## PM questions

End with numbered questions:

- **Blocking** — must resolve before spec merge
- **Defer** — can proceed with documented assumption
