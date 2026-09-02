# Candidate PRD schema

Write the path T0 resolved: `{reports_dir}/{INIT}-prd-think.md` or
`{INIT}-prd-think-N.md` (live name `prd/{INIT}.md` + suffix `-prd-think`,
under `reports_dir`). Never overwrite an earlier think candidate. Never
write `*-revN`. Score with `/prd-quality`, not this file.

**Ids:** read `prayog-skills/references/id-conventions.md` and assign only
product ids defined there (`CAP-*`, `REQ-*` canonical, `CTR-*`, `OQ-*`).
Do not mint `FR-*` or `D-*`. Locked decisions are a numbered statement table
until they become a CAP/REQ; unresolved product calls are `OQ-*`.

```markdown
# {INIT}: {short name} (prd-think candidate)

| Field | Value |
|-------|-------|
| Initiative | {INIT} |
| Status | candidate |
| Brief | {path or "conversation"} |
| Existing PRD | `prd/{INIT}.md` or none — not modified |
| Candidate path | {this file} |
| Score | `/prd-quality` — not written by this skill |

## 1. Job and outcome

- **Job:** {who, when, done-in-the-world — from T1}
- **Why now:**
- **If we do nothing:**
- **Kill assumption:** Fails if ___

## 2. Locked decisions

Numbered statements from this grill (1, 2, …). Not a new id namespace.
Empty = T1 is not done — do not draft REQs.

## 3. In scope / non-goals

### In scope
### Non-goals (load-bearing)

## 4. Actors

| Actor | Can actually | Cannot / OQ |
|-------|----------------|-------------|

## 5. Capabilities

| ID | Capability | Journeys covered | Notes |
|----|------------|------------------|-------|
| CAP-01 | | | |

## 6. Requirements

| ID | CAP | Requirement (WHAT) | Condition / event | Observable result | Evidence |
|----|-----|--------------------|-------------------|-------------------|----------|
| REQ-01 | CAP-01 | | | | unit / live / inspection |

## 7. Negative and failure paths

| REQ | Condition | Required behavior | Why it matters |
|-----|-----------|-------------------|----------------|

## 8. Contract seeds (semantic)

None — no cross-repo boundary.

**or**

| ID | Provider | Consumer | Logical operation | Field meaning | Invariants | Errors |
|----|----------|----------|-------------------|---------------|------------|--------|
| CTR-01 | {service} | {service} | | | | |

## 9. NFR applicability

| Area | Requirement or N/A rationale |
|------|------------------------------|
| Security | |
| Reliability | |
| Performance / capacity | |
| Observability | |
| Privacy / data handling | |
| Migration / compatibility | |
| Rollback / recovery | |
| Operations / support | |

## 10. Assumptions

| ID | Assumption | Status | Dependent REQs | Default if false |
|----|------------|--------|----------------|------------------|

## 11. Open questions

| ID | Question | Owner | Blocking | Required-by | Default if deferred |
|----|----------|-------|----------|-------------|---------------------|
| OQ-01 | | PM / PE | yes / no | spec-draft / feasibility / tech-review / later | |

## 12. Journeys

Actor, trigger, main flow, primary edge, abandon. At least one path the
brief did not list, or explicit "brief already complete" with T2 evidence.

## 13. Domain terms

| Term | Meaning in this INIT | Collision with existing product? |
|------|----------------------|----------------------------------|
```

## Writing rules

1. REQ is observable WHAT — id-conventions: testable requirement, not a story.
2. If a sentence needs a route, payload layout, or module to be true, it is
   not a REQ — `OQ-*` or drop.
3. No `[TBD]` inside a REQ. Split: known REQ + `OQ-*`.
4. Honest `OQ-*` beats fluent invention.
