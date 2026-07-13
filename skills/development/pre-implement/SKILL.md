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
metadata:
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
8. Verify the plan's source-freshness table is CURRENT and its impact-map
   revision/scope digest still match the canonical handoff. Stop on stale input.
9. Resolve `check_command` and `test_command`; resolve `verify_command` and
   `ground_command` when applicable. If the plan/profile/`AGENTS.md`/
   `tests_readme` cannot supply a required command, stop with MISSING command.
10. Confirm the current wave has a GitHub issue created from plan §9 and every
    declared predecessor wave issue exists. A missing/partial board seed blocks
    pre-implementation.
11. **Spec merge gate** — before W0 (and before any `/loop-spec`), confirm:
    - current branch is the **integration branch** (`develop`) or a
      `feature/INIT-*-w{N}-*` wave branch cut from it — **not** an open
      `chore/*-spec-*` Draft spec PR branch;
    - `docs/specification/reports/Implementation-Plan-{initiative}.md` exists on
      the integration branch (spec PR was merged);
    - the merged spec PR head carried **`spec-lgtm`** (verify via `gh pr view`
      on the closed spec PR: label present and `mergeCommit`/`headRefOid`
      matches attestation or Approve `commit_id`);
    - board-seed completed (wave issues exist per rule 10).
    If any check fails: stop — do not produce a checklist or write product code.

## Chain position

```
spec merge (spec-lgtm on head) → board-seed → wave issue In Progress
    ↓
/ground-spec (prior wave) → human_approved in as-built   [Wn>0 only]
    ↓
/pre-implement               ← YOU ARE HERE
  gate: spec merged + board seeded + prior wave human_approved?
  reads: Ground-Report-W{N-1}.md §Contracts produced
  produces: pre-flight checklist with confirmed contract baselines
    ↓
  developer: checklist reviewed, branch opened (feature/INIT-*-w{N}-*)
    ↓
/loop-spec → /ground-spec (this wave)
```

**Do not run on an open Draft spec PR branch** (`chore/*-spec-*`). Coding
starts only after the spec package is merged to `develop`.

## Read order

1. **Source and gate check** — spec merge gate (rule 11); plan on integration
   branch; plan sources CURRENT; impact-map scope current; canonical commands
   resolved; board issues exist; `as-built/implementation-status.md` prior wave
   = `human_approved` (Wn>0)? If any answer is no: stop.
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
   carry forward source digests, command contract, MDC notes, and ADR notes
   from TASK rows
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

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md` to the
checklist output. Use stage `pre-implement`.

- `pass` → `loop-spec`
- `needs-input` / `blocked` → human decision
- `stale` → `spec-implementation-plan`
- `failed` → stop

Record the board issue URL/id and resolved command contract in `signals`.
