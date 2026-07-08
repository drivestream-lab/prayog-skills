---
name: spec-technical-review
description: >-
  After feasibility, produce a principal-engineer design document: resolve all
  engineering decisions (ADRs, interface contracts, test policy, module
  boundaries), draft any required ADRs, and route only true product questions
  back to PM on the meta PRD PR. Use before /spec-implementation-plan when the
  feasibility report contains NEW-ADR findings, Critical/Should-fix engineering
  items, or unclear module boundaries. TDD commits on the spec PR branch; PE
  gives GitHub Approve on the same spec PR.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "spec PR branch: spec slice committed + initiative-feasibility report produced"
---

# Spec technical review

Resolve all **engineering decisions** that block the implementation plan.
**Do not implement.** Produce a Technical Design Document (TDD) and draft ADRs.

Runs **while the spec PR is open** — commit TDD to the spec branch. PE sign-off
is a **GitHub Approve on the spec PR** (CODEOWNERS on `Technical-Review-*`).

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
4. Every `NEW-ADR` from the feasibility report must map to a **draft ADR** or
   an explicit defer entry in this document.
5. Dual output: chat summary + saved TDD file committed to spec branch.
6. Run T0–T5 control loop (Gather → Understand → Analyze → Design → Execute → Verify).
7. Human PE sign-off is **required** before the implementation plan runs — PE
   **Approve** on the spec PR, not a separate merge gate after spec merge.

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

## When to use

- Feasibility report contains one or more `NEW-ADR` findings
- Feasibility has Critical findings involving module design, interface shape,
  or test policy
- Implementation plan is blocked by engineering questions (not PM questions)
- PE wants to document interface contracts before planning

## Process

1. **T0 Gather** — feasibility report, spec, ADRs, rules_glob, as-built
2. **T1 Understand** — list all NEW-ADR items, Critical/Should-fix engineering
   findings, and open engineering questions from feasibility
3. **T2 Analyze** — read relevant Accepted ADRs; read rules_glob; map each
   finding to an engineering decision, a PM question, or a domain clarification
   (routing rubric in [references/governance.md](references/governance.md))
4. **T3 Design** — for each engineering decision: state options, state
   recommended choice with rationale, write draft ADR if required; produce
   module boundary diagram; specify public interface contracts
5. **T4 Execute** — write TDD; run T1–T10 checks; commit to spec branch
6. **T5 Verify** — all engineering blockers resolved or deferred with defaults;
   only genuine PM/domain questions remain outstanding (routed to meta PRD PR)

## Output

Save to `{reports_dir}/Technical-Review-{initiative}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## PE sign-off

Commit TDD to the spec PR branch. PE reviews on the **same spec PR**:
- Discuss engineering decisions in spec PR comments
- Submit GitHub **Approve** when T1–T10 checks pass
- CODEOWNERS on `Technical-Review-*` enforces PE as required reviewer

After PE approves, dev runs `/spec-implementation-plan` on the same branch.

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

## Draft ADR format

For each NEW-ADR finding, produce a draft section (not a file during PE review).
After PE Approve, `/spec-implementation-plan` must include a pre-W0
`TASK-SPEC-ADR-NN` that promotes each TDD §4 draft to
`{adr_dir}/adr-NNN-{slug}.md` with status Accepted, PE name, and date. Manual
promotion by PE or human is a valid fallback if the plan has not run yet.

```markdown
### Draft ADR — {short title}
**Status:** Draft (requires PE sign-off)
**Problem:** …
**Options considered:**
  A. … (pros / cons)
  B. … (pros / cons)
**Recommendation:** Option A — {one-sentence rationale}
**Consequences:** …
**Open for review by:** {PE name or "PE checkpoint"}
```
