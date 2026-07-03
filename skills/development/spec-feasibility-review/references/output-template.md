# Feasibility report — {INITIATIVE}

| Field | Value |
|-------|-------|
| Initiative | {INITIATIVE} |
| Spec | {SPEC_PATH} |
| Repo | {REPO} |
| Date | {YYYY-MM-DD} |
| Branch | `chore/{sc}-feasibility` |
| Short-code | {sc} — see WorkManifest `short_code:` field |
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

## PR instructions

> Commit this report, then open a PR to get blocking items resolved.
> The gate is satisfied when the PR is merged.

```
Branch:   chore/{sc}-feasibility
PR title: "[{sc}] Feasibility report — {N} blocking items"
PR body:  paste the "Open items by lane" section above as the description
          so PM/Domain SME see their questions without opening the file

Required reviewers (set in PR):
  PM lane questions    → @{pm-name}
  Domain clarifications → @{domain-sme-name-or-team}
  (PE questions need no reviewer here — they go to /spec-technical-review)

Review deadline: {date from report header}
Merge when:
  [ ] All blocking PM questions answered in PR comments
  [ ] All blocking Domain clarifications answered in PR comments
  [ ] Spec updated to reflect answers (committed to same branch)
  [ ] Incremental re-run of feasibility on updated spec is clean
```

After merge: proceed to `/spec-technical-review` (if PE questions exist)
or `/spec-implementation-plan` (if no PE questions).
