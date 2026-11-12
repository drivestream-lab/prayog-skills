# Automation input contract (`prayog-qa-pack/v1`)

Normative rules for the agent that designs automation from a published
QA pack. `/qa-test-design` copies the block below into
`QA-Test-Plan-{INIT}.md` and fills the paths. The consuming agent reads
the plan in the consumer repo. It does not need this pin file.

The consumer designs automation. It does not reinterpret the PRD, add
cases, or change expected results.

## Handoff block to copy into the plan

```markdown
## Automation handoff

Consumer: an agent that designs test automation from this pack.
`layer: ui` is UI automation. `layer: be` is backend automation.
`layer: both` is both, with each expected observation kept on the layer
the case names.

Contract: `prayog-qa-pack/v1`

Read in this order:

1. This plan (scope, surfaces, rungs, residuals, this handoff)
2. `QA-Acceptance-Criteria-{INIT}.md`
3. `QA-Test-Cases-{INIT}.md`
4. `QA-RTM-{INIT}.md`

Design from cases where `automation_ready` is `yes`.

- `rung: unit` — process and mocks.
- `rung: capability` — black box, real infra, fixture stimulus. Cite `CAP-*` when the case has one.
- `rung: journey` — multi-step orchestration on real infra. Cite `J-*` when the case has one.
- Capability and journey stay separate. Passing one does not drop the other.
- `automation_ready: no` — do not automate. Report the blocker.
- Accepted-risk RTM rows have no case. Do not invent one.
- Preserve `REQ-*`, `EAC-*`, `TC-*`, `CAP-*`, and `J-*`. Do not add, drop, merge, or renumber them.
- Do not invent selectors, routes, payloads, status codes, or expected results.
```

Then append this yaml block with the pack's paths and revisions:

```yaml
automation_input:
  contract: prayog-qa-pack/v1
  initiative: {INIT}
  pack_revision: 1
  review_revision: 1
  consumer: automation-design-agent
  files:
    plan: prd/reports/QA-Test-Plan-{INIT}.md
    acceptance_criteria: prd/reports/QA-Acceptance-Criteria-{INIT}.md
    cases: prd/reports/QA-Test-Cases-{INIT}.md
    rtm: prd/reports/QA-RTM-{INIT}.md
```

Use the workspace-relative `{reports_dir}` paths from the profile, not a
hardcoded `prd/reports/` when the profile says otherwise.

## What the pack already decided

| Decision | Where it lives |
|----------|----------------|
| Scope in and out | Plan |
| Layer (`ui` / `be` / `both`) | Layer plan and each case |
| Rung (`unit` / `capability` / `journey`) | Rung plan and each case |
| Expected result | `EAC-*` and the case |
| Traceability | RTM |
| Unresolved product risk | Accepted-risk rows |

## What the pack leaves to the automation agent

- Driver shape, fixtures, and probes for the chosen rung
- UI structure only as far as the case's observable steps require
- Backend assertions only as far as the case's observable expected result requires
- Environment preflight for capability and journey (real infra, per the quality confidence ladder)

Logs alone are not the pass condition unless the case says so.
