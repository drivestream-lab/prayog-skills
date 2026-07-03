---
name: pre-implement
description: >-
  Before implementing one wave slice, produce a pre-flight checklist: verify
  the prior wave's human gate is satisfied, confirm contracts consumed from
  prior Ground Reports match what was actually built, then read specs/ADRs/rules.
  Use when starting implementation, opening a branch, or asked what to read
  before coding.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
background_eligible: true
background_trigger: "wave issue moved to In Progress on board"
---

# Pre-implement

Produce the **pre-flight checklist** for one wave slice. **Do not write
product code** unless the user explicitly asks after the checklist.

## NON-NEGOTIABLE

1. Resolve paths from `.harness/profile.yaml` when present; else
   [references/layout-defaults.md](references/layout-defaults.md).
2. **Gate check first** — before reading anything else, confirm the prior
   wave's Ground Report exists and its as-built row is `human_approved`.
   If not: stop and state which gate is unsatisfied. Do not produce a
   checklist for a wave whose predecessor is not approved.
3. Read `rules_glob` per the domain-filter approach in
   [references/governance.md](references/governance.md) — not all files.
4. Read relevant ADRs (keyword-match, then deep-read matched Accepted ADRs).
5. Output the checklist only unless the user asks to implement.
6. Cite concrete file paths for this repo and slice.
7. Describe contracts in engineering terms — entry points, input/output shapes,
   invariants. Do not use language-specific syntax.

## Chain position

```
/ground-spec (prior wave) → human_approved in as-built
    ↓
/pre-implement               ← YOU ARE HERE
  gate: prior wave = human_approved?
  reads: Ground-Report-W{N-1}.md §Contracts produced
  produces: pre-flight checklist with confirmed contract baselines
    ↓
  developer: checklist reviewed, branch opened
    ↓
[implementation]
    ↓
/loop-spec → /ground-spec (this wave)
```

## Read order

1. **Gate check** — `as-built/implementation-status.md`: prior wave =
   `human_approved`? If no: stop.
2. **Contracts consumed** — `reports/Ground-Report-W{N-1}.md` §Contracts
   produced: for each contract this wave depends on, read the entry point,
   input shape, output shape, and invariants as verified by the prior Ground
   Report. Confirm against actual source (scan `source_roots`) — not against
   spec alone.
3. `AGENTS.md` — constitution pin, verify commands, process links
4. **Domain-filtered MDC rules** — per [references/governance.md](references/governance.md)
5. **Relevant ADRs** — keyword-match slice scope; read matched Accepted ADRs
6. Initiative / slice spec — path from tracker Spec path or plan wave section
7. Plan wave section — `reports/Implementation-Plan-{initiative}.md` W{N}:
   carry forward MDC notes and ADR notes from TASK rows
8. `tests_readme` — when the slice adds or changes verification

**Gate for W0 (first wave):** no prior Ground Report exists. The gate is
the implementation plan PE sign-off (§0 of the plan). Confirm it is marked
complete before producing the W0 checklist.

**Cross-service / cross-module:** when this slice calls a module from another
service or a prior wave that has NOT yet been grounded, flag it explicitly in
the checklist under "Unconfirmed contracts" — do not silently assume the
interface.

## Output format

Use [references/output-template.md](references/output-template.md). Fill
concrete paths for this repo and slice.
