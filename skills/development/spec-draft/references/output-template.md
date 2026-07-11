# {INIT-id} — spec slice for {REPO}

| Field | Value |
|-------|-------|
| Initiative | {INIT-id} |
| PRD | `{client-meta}/prd/{INIT-id}.md` |
| PRD digest | `sha256:{hex}` |
| Meta PR | {URL} |
| Meta PR approved head | `{SHA}` |
| Impact map | `{client-meta}/prd/reports/Impact-Map-{INIT-id}.md` |
| Impact-map revision | `{N}` |
| Repo scope digest | `sha256:{hex}` |
| Tech-lead approval | {review URL/id, approver, submitted_at; review commit_id must equal approved head} |
| Repo | {REPO} |
| Date | {YYYY-MM-DD} |
| Status | Draft — dev review required before committing |

## Overview

{2–3 sentences: what this repo delivers for this initiative.
Scope boundary: what is OUT of scope for this repo.}

## Functional requirements

| ID | Requirement | PRD source | Acceptance criteria | Evidence type |
|----|-------------|-----------|---------------------|---------------|
| FR-{n} | {engineering statement, not user story} | PRD §{section} | {observable, testable} | unit / integration / live verify / inspection |

## Negative and failure paths

| FR | Condition | Required behavior | Evidence |
|----|-----------|-------------------|----------|
| FR-{n} | {invalid/empty/unavailable/timeout/unauthorized/partial} | {observable outcome, retry/idempotency rule} | {test/verify/inspection} |

## Out of scope for this repo

- {capability that belongs to another repo — name which one}

## Cross-service contracts

Use “None — no cross-repository boundary” when not applicable.

| Contract ID | Provider / owner | Consumer / owner | Entry point | Input shape | Output shape | Invariants | Errors | Compatibility / versioning | Contract-test location |
|-------------|------------------|------------------|-------------|-------------|--------------|------------|--------|----------------------------|------------------------|
| CTR-{n} | {repo / team} | {repo / team} | {endpoint/event/command/callable} | {accepts} | {returns/emits} | {guarantees} | {failure semantics} | {policy} | {path or planned path} |

## Non-functional requirements

Every row is required. Use N/A only with a concrete reason.

| Area | Requirement or N/A rationale | Acceptance / evidence |
|------|------------------------------|-----------------------|
| Security | | |
| Reliability | | |
| Performance / capacity | | |
| Observability | | |
| Privacy / data handling | | |
| Migration / compatibility | | |
| Rollback / recovery | | |
| Operations / support | | |

## Assumptions

| ID | Assumption | Evidence | Owner | Status | Invalidated when |
|----|------------|----------|-------|--------|------------------|
| A-{n} | {statement} | {source or “unverified”} | {owner} | confirmed / open | {condition} |

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

| ID | Lane | Question | Owner | Blocking | Required by | Default if deferred | Status | Resolution link |
|----|------|----------|-------|----------|-------------|---------------------|--------|-----------------|
| Q-{n} | PM / PE / domain | {plain-English question + PRD ref} | {owner} | yes/no | feasibility / technical review / plan | {safe default or none} | open/resolved | {URL/path or pending} |

## Draft check summary (D1–D12)

| Check | Status | Evidence / findings |
|-------|--------|---------------------|
| D1 Approved handoff current | PASS/FAIL/NEEDS INPUT | |
| D2 Complete PRD traceability | | |
| D3 Repo-bounded scope | | |
| D4 Observable acceptance | | |
| D5 Negative/failure paths | | |
| D6 Assumptions/questions | | |
| D7 Cross-repository contracts | | |
| D8 NFR applicability | | |
| D9 As-built alignment | | |
| D10 Dependency order | | |
| D11 Zero unresolved blockers | | |
| D12 Output completeness | | |

**Draft verdict:** PASS / FAIL / NEEDS INPUT

Do not advance to `/initiative-feasibility` unless the verdict is PASS and the
developer review below is complete.

## Developer review

- [ ] Scope matches the approved impact-map repo scope digest
- [ ] FRs and acceptance criteria are complete
- [ ] Contracts and NFR applicability are explicit
- [ ] No blocking question remains
- [ ] Developer confirmed draft is ready for feasibility

## References

- PRD: `{client-meta}/prd/{INIT-id}.md`
- Meta PRD PR: #{PR number or URL}
- Spec PR: #{PR number or URL}
- Service profile: `docs/specification/product/00-service-profile.md`
