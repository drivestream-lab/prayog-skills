---
name: spec-technical-review
description: >-
  After feasibility, produce a principal-engineer design document: resolve all
  engineering decisions (ADRs, interface contracts, test policy, module
  boundaries), draft any required ADRs, and route only true product questions
  back to PM. Use before /spec-implementation-plan when the feasibility report
  contains NEW-ADR findings, Critical/Should-fix engineering items, or unclear
  module boundaries.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "spec-handoff PR opened and feasibility report produced"
---

# Spec technical review

Resolve all **engineering decisions** that block the implementation plan.
**Do not implement.** Produce a Technical Design Document (TDD) and draft ADRs.

Benchmarked against: Stripe/Cloudflare/Oxide RFC process, Sentry design-first
gate, `agentic_development_workflow` multi-role review (Phase 2), GitHub
Spec Kit `/speckit.plan` architectural artifact pattern.

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Every engineering decision in the output must be **resolved** (recommendation
   recorded) or **explicitly deferred** with a named risk and default assumption.
3. Do not ask PM to choose architecture. Route only product-scope and
   user-visible behaviour questions to PM. See
   [references/governance.md](references/governance.md) for the routing rubric.
4. Every `NEW-ADR` from the feasibility report must map to a **draft ADR** or
   an explicit defer entry in this document.
5. Dual output: chat summary + saved TDD file.
6. Run T0–T5 control loop (Gather → Understand → Analyze → Design → Execute → Verify).
7. Human PE sign-off is **required** before the implementation plan runs — this
   document is a gate artifact, not auto-approved.

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
- PE wants to document interface contracts before agent starts coding

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
5. **T4 Execute** — write TDD; run T1–T10 checks
6. **T5 Verify** — all engineering blockers resolved or deferred with defaults;
   only genuine PM/domain questions remain outstanding

## Output

Save to `{reports_dir}/Technical-Review-{initiative}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## Routing rubric

See [references/governance.md](references/governance.md) for the full table.

Quick rule:
- **Engineering** — module boundaries, interface contracts, ADR gaps, test
  policy, error propagation, observability, data contract ownership → PE resolves
- **Product** — user-visible behaviour choices, scope cuts, priority → PM
- **Domain** — business source-of-truth (tab names, BU process, data ownership)
  → named domain SME
- **Auto-fixable** — naming drift, enum value mismatches with spec → agent fixes
  without human, note in TDD

## Draft ADR format

For each NEW-ADR finding, produce a draft section (not a file — the PE or human
commits the ADR file after sign-off):

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
