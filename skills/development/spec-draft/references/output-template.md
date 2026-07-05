# {INIT-id} — spec slice for {REPO}

| Field | Value |
|-------|-------|
| Initiative | {INIT-id} |
| PRD | `{client-meta}/prd/{INIT-id}.md` |
| Repo | {REPO} |
| Date | {YYYY-MM-DD} |
| Status | Draft — dev review required before committing |

## Overview

{2–3 sentences: what this repo delivers for this initiative.
Scope boundary: what is OUT of scope for this repo.}

## Functional requirements

| ID | Requirement | PRD source | Acceptance criteria |
|----|-------------|-----------|---------------------|
| FR-{n} | {engineering statement, not user story} | PRD §{section} | {observable, testable} |

## Out of scope for this repo

- {capability that belongs to another repo — name which one}

## Cross-service contracts

| This repo | Consumes from | Contract |
|-----------|---------------|---------|
| {this} | {other repo} | {what interface is needed} |

## Non-functional requirements

- {performance, security, observability constraints if stated in PRD}

## Spec questions (ambiguities — need PM or domain confirmation before feasibility)

1. {Question — plain English. Link to PRD section that is unclear.}

## References

- PRD: `{client-meta}/prd/{INIT-id}.md`
- Meta PRD PR: #{PR number or URL}
- Spec PR: #{PR number or URL}
- Service profile: `docs/specification/product/00-service-profile.md`
