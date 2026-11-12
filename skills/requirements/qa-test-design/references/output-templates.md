# QA test pack — output shapes

Overwrite the four files together. Illustration rows are not content for
a real PRD.

Shared header fields on every file:

| Field | Value |
|-------|--------|
| pack_revision | 1 |
| review_revision | 1 |
| prd | prd/{INIT}.md |
| prd_status | promoted |

## QA-Test-Plan-{INIT}.md

```markdown
# QA test plan — {INIT}

| Field | Value |
|-------|--------|
| pack_revision | 1 |
| review_revision | 1 |
| prd | prd/{INIT}.md |
| prd_status | promoted |

## Purpose

This pack is the input for an automation-design agent. It covers the
reviewed PRD. It does not cover automation code.

## Scope

| | Items |
|--|-------|
| In | REQ ids from the review inventory, minus accepted-risk |
| Out | PRD non-goals, quoted; accepted-risk REQ ids |

## Surfaces

| Surface | Evidence quote | REQ ids |
|---------|----------------|---------|
| ui | "…" | REQ-01 |

## Layer plan

| REQ | Layer | Evidence quote |
|-----|-------|----------------|
| REQ-01 | ui | "…" |

## Rung plan

| REQ | CAP | J | Rungs | Evidence quote |
|-----|-----|---|-------|----------------|
| REQ-01 | CAP-01 | J-01 | capability, journey | "…" |

## Case inventory

| TC | REQ | EAC | Layer | Rung | Type | Priority |
|----|-----|-----|-------|------|------|----------|
| TC-01 | REQ-01 | EAC-01 | ui | capability | positive | P0 |

## Entry

Review `ready_for_test_design: yes`, or the accepted-risk list below.

## Exit

D1–D8 pass. RTM has every inventory REQ. Every non-risk REQ has at least
one EAC and one TC.

## Residuals

| QQ | Blocking | Disposition |
|----|----------|-------------|
| QQ-02 | no | open, not used in expected results |
| QQ-03 | yes | accepted-risk, no TC |

## Environments

Unit cases: process and mocks. Capability and journey cases: real infra
and fixture stimulus, capability and journey kept separate. Stack choice
belongs to the automation agent. See
`prayog-skills/references/quality-confidence-ladder.md`.

## Automation handoff
```

Replace this heading's body with the handoff block from
`references/automation-input.md`, with paths, `{INIT}`, `pack_revision`,
and `review_revision` filled in. Do not leave the pin-file instruction in
the published plan.

Omit a surface row that has no evidence. Case types are `positive`,
`negative`, `boundary`, `error`, `permission`, `empty`.

## QA-Acceptance-Criteria-{INIT}.md

One section per `EAC-{nn}` after a summary table.

```markdown
# Enhanced acceptance criteria — {INIT}

| EAC | REQ | Source | Cites |
|-----|-----|--------|-------|
| EAC-01 | REQ-01 | answer | QQ-01 |

## EAC-01

| Field | Value |
|-------|--------|
| req | REQ-01 |
| source | answer |
| cites | QQ-01 |
| given | … |
| when | … |
| then | … |
| quote | "…" |
```

`source` is `prd` or `answer`. `cites` is `—` or one or more `QQ-*`.
The Given / When / Then statement adds no rule beyond the quote.

## QA-Test-Cases-{INIT}.md

Summary table, then one section per case.

```markdown
# QA test cases — {INIT}

| TC | Title | REQ | EAC | Layer | Rung | Type | Priority | Automation ready |
|----|-------|-----|-----|-------|------|------|----------|------------------|
| TC-01 | … | REQ-01 | EAC-01 | ui | capability | positive | P0 | yes |

## TC-01 …

| Field | Value |
|-------|--------|
| req | REQ-01 |
| eac | EAC-01 |
| cap | CAP-02 |
| journey | — |
| layer | ui |
| rung | capability |
| type | positive |
| priority | P0 |
| automation_ready | yes |
| cites | QQ-01 |

### Preconditions

…

### Data

…

### Steps

1. …

### Expected

…
```

`layer: both` splits Expected into `ui:` and `be:` observations.
Data is a concrete value from a quote. "Valid user" is not data. One case
has one primary expected result.

## QA-RTM-{INIT}.md

```markdown
# Requirements traceability matrix — {INIT}

| REQ | Stated acceptance (quote or —) | EAC | TC | Layer | Rung | Status |
|-----|--------------------------------|-----|----|-------|------|--------|
| REQ-01 | "…" | EAC-01 | TC-01 | ui | capability | covered |
| REQ-09 | — | — | — | — | — | accepted-risk |
```

Accepted-risk rows name the `QQ-*` in a note under the table.
Status is `covered`, `partial`, or `accepted-risk`.

## Illustration (do not copy)

Answer to QQ-01: "Results appear within 2 seconds." That sentence is the
only source of the 2 second bound in EAC-01 and TC-01. The PRD's
"quickly" is the stated-acceptance quote on the RTM, not the expected
result.
