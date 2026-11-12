---
name: qa-test-design
description: >-
  Writes the QA automation input pack from a PRD and a ready QA
  requirements review: test plan and strategy, test cases, enhanced
  acceptance criteria, and a requirements traceability matrix. Use when
  the user asks for a test plan, test strategy, test cases, enhanced
  acceptance criteria, an RTM, or UI, backend, or both test design from
  a PRD. Refuses while blocking questions are open. Writes four reports
  under reports_dir. Does not write automation code or edit the PRD.
  Human-invoked; not a workflow node.
disable-model-invocation: true
---

# QA test design

Turn a reviewed PRD into the pack a later agent uses to design test
automation. The pack decides scope, expected results, layer, and rung.
The later agent designs UI automation, backend automation, or both.
This skill writes no automation code.

Review is `/qa-requirements-review`. Do not rediscover gaps here.

**Pin contracts (read, do not fork):**

- Ids: `prayog-skills/references/id-conventions.md` (`EAC-*`, `TC-*`, `QG-*`, `QQ-*`)
- Paths: `prayog-skills/references/artifact-write-contract.md`
- Prove rungs: `prayog-skills/references/quality-confidence-ladder.md`
- Checks, consumer rules, shape:
  [references/design-checks.md](references/design-checks.md),
  [references/automation-input.md](references/automation-input.md),
  [references/output-templates.md](references/output-templates.md)

## Inputs

1. **Review** — `{reports_dir}/QA-Requirements-Review-{INIT}.md` (required).
   If it is missing, stop and name `/qa-requirements-review`. Do not review
   inline.
2. **The same PRD** the review names.
3. **Accepted risk** (optional) — the user message lists blocking `QQ-*`
   ids they accept unresolved. No assumption is attached unless they
   state one. An unstated assumption is not acceptance.
4. **Layout** — `{reports_dir}` from `.harness/profile.yaml` (meta default
   `prd/reports/`).

`ready_for_test_design: yes` means every blocking `QQ` is answered.
Otherwise every open blocking `QQ` must appear in the accepted-risk list
or this skill stops.

## Outputs

Overwrite these four files together. One `pack_revision` (start at 1,
bump by 1 on every rewrite). Never write `*-revN`.

| File | Role |
|------|------|
| `{reports_dir}/QA-Test-Plan-{INIT}.md` | Strategy and automation handoff |
| `{reports_dir}/QA-Test-Cases-{INIT}.md` | Cases |
| `{reports_dir}/QA-Acceptance-Criteria-{INIT}.md` | Enhanced acceptance criteria |
| `{reports_dir}/QA-RTM-{INIT}.md` | Requirements traceability matrix |

Record the `review_revision` consumed. If that revision does not match the
review file, rewrite the whole pack. Do not patch one file.

## NON-NEGOTIABLE

1. **Refuse** when a blocking `QQ` is open and not in the accepted-risk
   list. Name the ids. Do not publish a partial pack.
2. **Evidence for every expected result, actor, limit, and layer.** The
   evidence is a PRD quote or a quoted answer. Sharpening splits a
   compound statement or makes an already-stated outcome checkable.
   A new rule goes back to `/qa-requirements-review`. Do not mint `QQ-*`
   here.
3. **Accepted risk writes no case and no invented expected result.** The
   RTM row is `accepted-risk` with the `QQ-*` and zero `TC` ids.
4. **Trace.** Every other REQ in the review inventory has at least one
   `EAC-*` and one `TC-*`. Every `TC` cites at least one `REQ` and one
   `EAC`. Every `EAC` cites exactly one `REQ`.
5. **Layer** is `ui`, `be`, or `both`, from the layer plan. **Rung** is
   `unit`, `capability`, or `journey`, from the rung plan. A journey case
   does not replace a capability case, or the reverse.
6. **Do not mint** `CAP-*`, `J-*`, or `REQ-*`. Cite them when the PRD has
   them. Leave the cell `—` when it does not.
7. **Steps are observable.** No selectors, code, routes, payloads, or
   status codes the PRD did not state.
8. **Copy the automation handoff** from
   [references/automation-input.md](references/automation-input.md) into
   the plan so the consuming agent can read it without this pin.
9. **Do not invoke** `/qa-requirements-review`, `/prd-quality`,
   `/validate-requirements`, `/update-documents`, or forge. Do not edit
   the PRD.

## Process

### T0 Gate

Read the review and the PRD. If the gate fails, stop in chat with the
blocking `QQ` ids and do not write the four files.

### T1 Plans

Build two tables before any case prose:

- **Layer plan** — one row per in-scope REQ. Evidence quote for `ui`,
  `be`, or `both`. `both` names which observation belongs to which layer.
- **Rung plan** — rungs to write and why, quoted.
  - PRD journey that includes the REQ → a journey case citing that `J-*`.
  - PRD capability that includes the REQ → a capability case citing that
    `CAP-*`.
  - Neither, and the text is a pure rule (validation, calculation,
    permission decision with no multi-step path) → `unit`.
  - Neither, and the text is one ability → `capability` with CAP `—`.
  - Neither, and the text is a multi-step actor path → `journey` with
    J `—`.
  - User-visible behavior does not also get a unit case.
  - When both a `CAP-*` and a `J-*` apply, list both rungs.

### T2 Enhanced acceptance criteria

Mint `EAC-{nn}` from stated criteria and from **answered** `QQ-*` only.
`source` is `prd` or `answer`. Given / When / Then must be checkable
against the quote. One EAC, one REQ, one primary outcome.

### T3 Cases

Mint `TC-{nn}` to match the rung plan.

- One positive case on each rung the plan lists for that REQ.
- A negative, error, boundary, permission, or empty case only when the
  PRD or an answer states that situation.
- One primary expected result per case.
- `automation_ready: yes` when steps and the expected result are fully
  determined by quotes. `no` when a non-blocking open `QQ` would change
  the steps. Do not fill that gap yourself.
- Priority: `P0` for the primary positive case of a capability or journey,
  and for stated data-loss or permission outcomes. `P1` for other stated
  negative, boundary, or error cases. `P2` for stated empty states and
  secondary variants.

### T4 Plan and RTM

Write the plan (scope, surfaces, rung strategy, entry, exit, residuals,
automation handoff). Write the RTM so every inventory REQ appears once.

| RTM status | When |
|------------|------|
| `covered` | At least one `TC`, all of them `automation_ready: yes` |
| `partial` | At least one `TC`, and at least one `automation_ready: no` |
| `accepted-risk` | User named the blocking `QQ` and no case was written |

`untestable` is not a status this skill may assign. That finding returns
to `/qa-requirements-review`.

### T5 Checks

Run D1–D8 in [references/design-checks.md](references/design-checks.md).
Fix the pack and run them again. Publish only when all eight pass.

### T6 Reply

State `pack_revision`, the four paths, counts of `EAC` and `TC` by layer
and rung, accepted-risk ids, and that the plan's automation handoff is
the brief for the automation-design agent.

## Workflow handoff

This skill is **human-invoked**. It is not a node in pinned `workflow.yaml`.

When orchestrator-bound and the pack is published:

1. Persist the four files.
2. **Overwrite** `handoff_path` with the `handoff:` envelope when bound.
   Leaving the baton empty is a failed stage for automated consumers.
   `artifact.path` is the test plan. `signals.pack_paths` lists all four
   workspace-relative paths.
3. Derive `next_candidates` and `human_checkpoint` from pinned root
   `workflow.yaml` for `(stage: qa-test-design, outcome)` per
   `prayog-skills/references/handoff-envelope.md` (**Derive from pinned
   workflow**). Set `human_checkpoint: true` only when the resolved next
   node's `type` is `human-checkpoint`.
4. This `skill_id` is absent from `workflow.yaml`, so the derivation has
   no edge: `next_candidates: []`, `human_checkpoint: false`,
   `external_action: false`. `signals.recommended_next` is
   `automation-design` (a consumer, not a pin node).
5. `outcome: pass`. `blockers: []`.

When the gate fails, skip the pack. If `handoff_path` is bound, overwrite
it with `outcome: blocked` and `blockers` set to the open blocking `QQ-*`
ids. Same empty navigation as step 4.

When not orchestrated, skip baton write unless `handoff_path` is bound.
