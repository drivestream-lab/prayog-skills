---
name: spec-technical-review
description: >-
  After feasibility, produce a principal-engineer design document: resolve all
  engineering decisions (ADRs, interface contracts, test policy, module
  boundaries), draft any required ADRs, and route only true product questions
  back to PM on the meta PRD PR. Use before /ui-variations (then plan) when the
  feasibility report contains NEW-ADR findings, Critical/Should-fix engineering
  items, or unclear module boundaries. Commits TDD and Draft ADRs to the Draft
  spec PR; PE accepts architecture in files before planning. Final Gate 2
  unlock (spec-lgtm) happens only after the implementation plan exists.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "spec PR branch: spec slice committed + initiative-feasibility report produced"
---

# Spec technical review

Resolve all **engineering decisions** that block the implementation plan.
**Do not implement.** Produce a Technical Design Document (TDD) and draft ADRs.

Runs **while the Draft spec PR is open** — commit TDD and ADR files to the spec
branch. Gate 2 label remains **`spec-pending`**. PE architecture acceptance is
recorded in **artifact metadata** (`Draft` → `Accepted`); **`spec-lgtm`** is
set only after the full spec package (including plan) is on head.

Benchmarked against: Stripe/Cloudflare/Oxide RFC process, Sentry design-first
gate, `agentic_development_workflow` multi-role review, GitHub Spec Kit
`/speckit.plan` architectural artifact pattern.

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Every engineering decision in the output must be **resolved** (recommendation
   recorded) or **explicitly deferred** with a named risk and default assumption.
3. Do not ask PM to choose architecture. Route only product-scope and
   user-visible behaviour questions to the **meta PRD PR**. See
   [references/governance.md](references/governance.md) for the routing rubric.
4. Every `NEW-ADR` from feasibility maps to exactly one disposition:
   `ADR_REQUIRED` with a Draft file under `adr_dir`, `TDD_ONLY` with rationale,
   or `DEFERRED_WITH_DEFAULT` with risk and revisit trigger.
5. Dual output: chat summary + saved TDD file committed to spec branch.
6. Run T0–T5 control loop (Gather → Understand → Analyze → Design → Execute → Verify).
7. Human PE acceptance is **required** before the implementation plan runs.
   Technical review creates Draft ADR files first; planning consumes only
   **Accepted** files in `{adr_dir}`. Mid-lane PE work updates files on the
   spec branch — it does **not** set `spec-lgtm`.
8. Verify that spec, feasibility report, PRD digest, impact-map revision, repo
   scope digest, and approved meta PR head agree. Stop on stale inputs.

## Inputs

Resolve paths from `.harness/profile.yaml` or
[references/layout-defaults.md](references/layout-defaults.md).

1. **Feasibility report** — primary input (REQUIRED); source of NEW-ADR
   findings, Critical/Should-fix items, open engineering questions
2. **Initiative spec** — (REQUIRED)
3. **ADR directory** — existing accepted ADRs from `adr_dir` (REQUIRED)
4. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
5. **As-built** — `implementation-status.md` (REQUIRED)
6. **`.harness/profile.yaml`** or layout defaults (REQUIRED)
7. **Canonical handoff references** — PRD digest, impact-map revision/scope
   digest, approved meta PR head, and tech-lead review (REQUIRED)

## When to use

- Feasibility report contains one or more `NEW-ADR` findings
- Feasibility has Critical findings involving module design, interface shape,
  or test policy
- Implementation plan is blocked by engineering questions (not PM questions)
- PE wants to document interface contracts before planning

## Process

1. **T0 Gather and freshness gate** — feasibility report, spec, canonical
   handoff references, ADRs, rules_glob, as-built; stop if any source digest or
   approval reference is stale
2. **T1 Understand** — list all NEW-ADR items, Critical/Should-fix engineering
   findings, and open engineering questions from feasibility
3. **T2 Analyze** — read relevant Accepted ADRs; read rules_glob; map each
   finding to an engineering decision, a PM question, or a domain clarification
   (routing rubric in [references/governance.md](references/governance.md))
4. **T3 Design** — classify every NEW-ADR using the rubric below; for each
   `ADR_REQUIRED`, allocate a stable file path and render
   [references/adr-template.md](references/adr-template.md); produce module
   boundaries and public interface contracts
5. **T4 Execute** — write TDD + every Draft ADR file; make TDD §4 an ADR
   index; run T1–T11 checks
6. **T5 Verify** — all required ADR files exist and are linked; all engineering
   blockers are resolved/deferred; only genuine PM/domain questions remain;
   emit `ready_for_pe_review: true` and `ready_for_plan: false`

## Output

Save to `{reports_dir}/Technical-Review-{initiative}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## PE acceptance (artifact gate — not Gate 2 unlock)

Commit TDD + Draft ADR files to the Draft spec PR. PE reviews on the **same PR**:
- Discuss engineering decisions in spec PR comments
- Request changes until decisions and artifacts are correct
- CODEOWNERS on `Technical-Review-*` may request PE review when the TDD file is present

When PE explicitly states decisions are ready for acceptance:

1. update required ADR files `Draft` → `Accepted` with PE/date/review evidence,
2. update the TDD `Status` field to **Accepted** and TDD §4 ADR index rows,
3. commit the acceptance package to the spec branch,
4. record the approved head SHA in TDD/ADR metadata when helpful.

**Do not set `spec-lgtm` at this stage.** `/spec-implementation-plan` reads
Accepted files (P12/P13). The GitHub Gate 2 unlock (`spec-lgtm` + Approve +
attestation) happens only after the plan is committed to the same PR head.

## Routing rubric

See [references/governance.md](references/governance.md) for the full table.

Quick rule:
- **Engineering** — module boundaries, interface contracts, ADR gaps, test
  policy, error propagation, observability, data contract ownership → PE resolves on spec PR
- **Product** — user-visible behaviour choices, scope cuts, priority → meta PRD PR
- **Domain** — business source-of-truth (tab names, BU process, data ownership)
  → named domain SME
- **Auto-fixable** — naming drift, enum value mismatches with spec → agent fixes
  without human, note in TDD

## ADR qualification rubric

Use `ADR_REQUIRED` when the decision is cross-module/service, security/privacy
relevant, chooses data/storage authority or deployment architecture, is hard to
reverse, constrains later initiatives, or deliberately departs from the
constitution.

Use `TDD_ONLY` for a local, easily reversible implementation choice already
bounded by rules. Use `DEFERRED_WITH_DEFAULT` only with a named risk, safe
default, and observable revisit trigger.

Every disposition remains traceable to its feasibility finding. Never satisfy
T11 with a future promotion task or a target path alone.

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md` to the TDD.
Use stage `spec-technical-review`.

- `pass` → `technical-review-approval`
- `findings` / `needs-input` / `blocked` → human decision
- `stale` → `initiative-feasibility`
- `failed` → stop

Before final approval, signals must include actual Draft ADR paths/digests,
`ready_for_pe_review: true`, and `ready_for_plan: false`. After the final
exact-head approval, the approval node—not this skill—enables planning.
