# Invoke: qa-test-design

You are executing the **qa-test-design** skill (Test plan, cases, enhanced acceptance criteria, and RTM for an automation agent).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Build the automation input pack from the PRD and
`QA-Requirements-Review-{INIT}.md`. Write the test plan, test cases,
enhanced acceptance criteria, and RTM. Refuse while a blocking question
is open and not explicitly accepted as residual risk.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when
present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation
package only.

## Non-negotiables (summary)
1. Missing review — stop. Do not review inline.
2. Expected results, actors, limits, and layers come from PRD quotes or quoted answers.
3. Every in-scope REQ is on the RTM. Every TC cites a REQ and an EAC.
4. Layer is `ui`, `be`, or `both`. Rung is `unit`, `capability`, or `journey`. Capability and journey stay separate.
5. Copy the automation handoff into the plan. Do not write automation code.
6. Do not invoke `/qa-requirements-review`, `/validate-requirements`, or forge from here.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: {{skill_id}}, outcome)` per
`prayog-skills/references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
This skill is not a workflow node. If `workflow.yaml` has no `{{skill_id}}`
node, set `next_candidates` to `[]`, `human_checkpoint` to false, and
`external_action` to false. Put the recommended consumer only in
`signals.recommended_next`.
This skill is normally human-invoked outside the workflow graph; when not
orchestrated, skip envelope write unless `handoff_path` is bound.

## Workspace
Root: `{{workspace}}` (meta repo).

## Handoff baton (required)
1. Persist the four pack files under `{{workspace}}`. `artifact.path` is the test plan.
2. When orchestrator-bound, **overwrite** the file at exactly
   `{{handoff_path}}` with the `handoff:` envelope (plain YAML or a single
   fenced yaml block).
3. Do not leave `{{handoff_path}}` empty when bound.
