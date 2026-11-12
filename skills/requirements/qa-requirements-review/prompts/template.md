# Invoke: qa-requirements-review

You are executing the **qa-requirements-review** skill (QA expert review of one PRD: gaps and questions).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Read one PRD. Inventory stated requirements and acceptance criteria, record
testability gaps, and ask clarifying questions plus follow-ups. Write
`QA-Requirements-Review-{INIT}.md`. Ask open questions in the chat reply.
Do not write test cases. Do not edit the PRD.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when
present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation
package only.

## Non-negotiables (summary)
1. One PRD — do not blend files.
2. Quote the PRD. Do not invent behavior, routes, payloads, or selectors.
3. A question is blocking when a test would guess actor, expected result, layer (`ui` / `be` / `both`), or a numeric or time bound.
4. Follow-ups only when an answer opens a new decision. Keep `QQ-*` ids.
5. `ready_for_test_design` is yes only when zero blocking questions are open.
6. Do not invoke `/qa-test-design`, `/prd-quality`, `/validate-requirements`, or forge from here.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: {{skill_id}}, outcome)` per
`prayog-skills/references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
This skill is not a workflow node. If `workflow.yaml` has no `{{skill_id}}`
node, set `next_candidates` to `[]`, `human_checkpoint` to false, and
`external_action` to false. Put the recommended command only in
`signals.recommended_next`.
This skill is normally human-invoked outside the workflow graph; when not
orchestrated, skip envelope write unless `handoff_path` is bound.

## Workspace
Root: `{{workspace}}` (meta repo).

## Handoff baton (required)
1. Persist `QA-Requirements-Review-{INIT}.md` under `{{workspace}}`.
2. When orchestrator-bound, **overwrite** the file at exactly
   `{{handoff_path}}` with the `handoff:` envelope (plain YAML or a single
   fenced yaml block).
3. Do not leave `{{handoff_path}}` empty when bound.
