# QA requirements review — output shape

Overwrite `{reports_dir}/QA-Requirements-Review-{INIT}.md` with this shape.
The illustration at the bottom is not content for a real PRD.

```markdown
# QA requirements review — {INIT}

| Field | Value |
|-------|--------|
| review_revision | 1 |
| prd | prd/{INIT}.md |
| prd_status | promoted |
| ready_for_test_design | no |
| blocking_open | QQ-01 |

## Inventory

| Kind | Id | Quote |
|------|----|-------|
| REQ | REQ-01 | "…" |
| Acceptance | — | "…" |
| CAP | CAP-01 | "…" |
| Journey | J-01 | "…" |
| Actor | — | "…" |

## Notes

## Gaps

| QG | Check | REQ | Blocking | Quote |
|----|-------|-----|----------|-------|
| QG-01 | R3 | REQ-01 | yes | "…" |

## Questions

| QQ | QG | Follows | Blocking | Status | Question | Answer |
|----|----|---------|----------|--------|----------|--------|
| QQ-01 | QG-01 | — | yes | open | What observation means this passes? | |

## Follow-ups this revision
```

Acceptance rows use no id. The quote is the key. `EAC-*` is minted later
by `/qa-test-design`. Notes that need no decision get no `QG` or `QQ` id.
Question status is `open` or `answered`. Follows is `—` or a parent `QQ-*`.
The follow-ups section lists only `QQ-*` minted in this revision. Leave it
empty when there are none.

## Handoff

Append this envelope. The sample `outcome` is `needs-input`.

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: qa-requirements-review
  outcome: needs-input
  artifact:
    path: prd/reports/QA-Requirements-Review-{INIT}.md
  blockers:
    - QQ-01
  signals:
    ready_for_test_design: false
    recommended_next: answer-questions
    review_revision: 1
  next_candidates: []
  human_checkpoint: false
  external_action: false
```

`outcome` is `pass` and `blockers` is `[]` when `ready_for_test_design` is
`yes`. Then `signals.recommended_next` is `qa-test-design`.

`recommended_next` is a signal. It is not a `workflow.yaml` edge.

## Illustration (do not copy into a real review)

REQ quote: "The user can search quickly."

| QG | Check | REQ | Blocking | Quote |
|----|-------|-----|----------|-------|
| QG-01 | R3 | REQ-04 | yes | "The user can search quickly." |

| QQ | Question |
|----|----------|
| QQ-01 | Which observation means search passes: results visible within a stated time, or any completed search with no time limit? |
