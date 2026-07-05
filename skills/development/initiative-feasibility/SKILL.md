---
name: initiative-feasibility
description: >-
  After the dev team has written their spec slice from the PRD, review it
  against the current codebase — baseline, gaps, impact, test harness,
  architecture governance (ADR + MDC), risks, and 4-lane triage. Use when
  the dev has drafted the spec and wants to check buildability before technical
  review and planning. Runs while the spec PR is open.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
background_eligible: true
background_trigger: "spec slice committed to spec PR branch (chore/INIT-*-spec-*)"
---

# Initiative feasibility

Assess whether the **dev team's spec slice** for this initiative is **buildable
in this repo as it exists today**. **Do not implement** — flag only.

The spec slice is written by the dev team after reading the PRD. This skill
reviews it for gaps, codebase alignment, and architecture governance.

Pattern borrowed from awesome-copilot `create-github-issues-for-unmet-specification-requirements` (extract → search code → classify). Evaluation discipline aligned with `validate-requirements`.

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Evidence for every finding — spec quote + repo path (file, symbol, or test name).
3. Don't fix — flag. Do not edit product source or product specs unless the user explicitly asks after the report.
4. Dual output: chat summary + saved report file + 4-lane triage.
5. Run T0–T5 control loop (Gather → Understand → Analyze → Plan → Execute → Verify).

## Inputs

Gather before starting. Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **Initiative spec slice** — primary doc (REQUIRED); written by dev team, lives under `product_spec_dir`
2. **PRD** — upstream requirements from `<client>-meta/prd/` (OPTIONAL; for conformance context; link from spec header)
3. **As-built** — `implementation-status.md` (REQUIRED)
4. **Tests** — `tests_readme`, `unit_tests_dir`, `live_verify_dir`, and toolchain config from profile (REQUIRED)
5. **Source** — modules under `source_roots` from profile (REQUIRED)
6. **Prior feasibility report** — for incremental re-run (OPTIONAL)
7. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)
8. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
9. **`adr_dir`** — architecture decision records (REQUIRED). Run relevant-ADR pass per [references/governance.md](references/governance.md) before T2 Analyze.

## When to use

- Dev has written spec slice and wants to check buildability before spec PR merge
- After dev updates spec — re-run on changed sections
- User asks: feasibility, impact, gap analysis, spec vs codebase

## Process

1. **T0 Gather** — inventory inputs; note missing paths
2. **T1 Understand** — initiative id, spec branch, review objective
3. **T2 Analyze** — read spec waves/capabilities; scan repo evidence; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs
4. **T3 Plan** — which checks run (full vs incremental)
5. **T4 Execute** — run checks F1–F14 per [references/checks.md](references/checks.md)
6. **T5 Verify** — save report; publish summary + 4-lane triage

## Output

Save to `{reports_dir}/{feasibility_prefix}-{initiative}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## Open items — 4-lane triage

End with four lanes (see output template):

- **PM questions** — product scope, UX, priority; comment on **meta PRD PR** (plain English)
- **PE questions** — engineering decisions, ADR gaps, test policy; comment on **spec PR**; resolved by `/spec-technical-review`
- **Domain clarifications** — business source-of-truth; route to named SME (meta PRD PR or issue)
- **Auto-fixable** — naming drift, inferred cross-references; agent resolves on spec branch

Do **not** route engineering decisions to PM. Apply the routing rubric in
the `spec-technical-review` skill's `references/governance.md`.
