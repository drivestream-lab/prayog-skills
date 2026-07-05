# Feasibility report — {INITIATIVE}

| Field | Value |
|-------|-------|
| Initiative | {INITIATIVE} |
| Spec | {SPEC_PATH} |
| Repo | {REPO} |
| Date | {YYYY-MM-DD} |
| Branch | `chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}` — spec PR (single review surface) |
| Initiative segment | `INIT-{COMPONENT}-{NUMBER}` — COMPONENT is service branch_code from service-catalog.yaml |
| Status | Draft |
| Review deadline | {YYYY-MM-DD + 3 business days} |
| Deciders | PM: {name} · Domain SME: {name or team} |

## Summary

{2–4 sentences: buildable? main gaps? merge recommendation}

**Findings:** {N} total ({critical} Critical, {should} Should fix, …)

## Baseline snapshot (F1)

| Area | Current state | Evidence |
|------|---------------|----------|
| Unit tests | | |
| Live verify | | |
| As-built | | |

## Traceability matrix

| Spec ref / wave | Spec claim | Code evidence | Unit | Verify | Status |
|-----------------|------------|---------------|------|--------|--------|
| | | | | | exists / gap / partial / drift |

## ADR traceability (F13)

| Spec ref / wave | Relevant ADR(s) | Status | Finding |
|-----------------|-----------------|--------|---------|
| | ADR-… / NEW-ADR / N/A | aligned / conflict / missing ADR | |

## Governance findings (F13–F14)

| ID | Check | Spec quote | Governing doc | Finding |
|----|-------|------------|---------------|---------|
| | F13 / F14 | | ADR-… / rule file | |

## Findings by severity

### Critical
| ID | Check | Finding | Evidence |
|----|-------|---------|----------|

### Should fix
| ID | Check | Finding | Evidence |
|----|-------|---------|----------|

## Impact surface

| Wave / area | Likely files/modules | Test touch |
|-------------|----------------------|------------|
| | | |

## Risks & assumptions

| ID | Risk / assumption | Mitigation |
|----|-------------------|------------|

## Recommended spec edits

- (bullet list for PR branch — no silent fixes)

---

## Open items by lane

> Routing rubric: product scope / UX → PM · engineering decisions / ADR → PE ·
> business source-of-truth → Domain SME · naming drift / inferred fixes → Auto-fix.
> Full rubric: `.agents/skills/spec-technical-review/references/governance.md`

### PM questions (product scope, UX, priority)

#### Blocking — must resolve before spec merge
1. …

#### Defer — can proceed with documented assumption
1. …

### PE questions (engineering decisions — resolved by `/spec-technical-review`)

> These are **not** for PM. Run `/spec-technical-review` to produce a Technical
> Design Document that resolves these before `/spec-implementation-plan`.

#### Blocking for implementation plan
1. …

#### Defer with default
1. …

### Domain clarifications (business source-of-truth)

> Route to the named SME or BU team, not to PM and not to engineering.

| # | Question | Suggested SME | Blocks |
|---|----------|---------------|--------|
| D-1 | … | | |

### Auto-fixable (agent resolves — no human needed)

> These items can be corrected by the agent during `/spec-technical-review` or
> `/spec-implementation-plan`. No human escalation required.

| # | Item | Fix |
|---|------|-----|
| AF-1 | … | align to existing enum / schema doc |

---

## Check summary

| Check | Status | Findings |
|-------|--------|----------|
| F1–F14 | PASS/FAIL/SKIPPED | |

---

## Next steps

> This report lives on the spec PR branch alongside the spec draft.
> The spec PR is the engineering review surface; product Q&A uses the meta PRD PR.

**PM questions** → post as numbered comments on the **meta PRD PR** (plain English).
  Link from a spec PR comment if helpful. PM answers on meta PRD PR.

**PE questions** → discuss on the **spec PR**; run `/spec-technical-review` next.
  Commit TDD to spec branch; PE Approve on the same spec PR.

**Domain clarifications** → meta PRD PR comment or tracked issue; record answers in
  `open-questions.md` and commit to spec branch.

**Auto-fixable items** → fix and commit to spec branch now.

```
Spec branch: chore/INIT-{COMPONENT}-{NUMBER}-spec-{repo}
When ready:
  [ ] All blocking PM questions answered on meta PRD PR
  [ ] All blocking Domain clarifications answered and committed
  [ ] Spec updated to reflect answers (same branch)
  [ ] Incremental re-run of /initiative-feasibility on updated spec is clean
  [ ] Proceed: /spec-technical-review (PE questions exist)
               OR /spec-implementation-plan (no PE questions)
  [ ] After spec + feasibility + TDD (if any) + plan on branch: merge spec PR
  [ ] After merge: seed board from plan §9 — then start wave coding
```
