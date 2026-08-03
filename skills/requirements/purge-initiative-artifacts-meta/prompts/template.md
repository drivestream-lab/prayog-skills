# Invoke: purge-initiative-artifacts-meta

You are executing the **purge-initiative-artifacts-meta** skill (Delete allowlisted
meta PM working papers after initiative-closure.).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Follow the full procedure in this skill's `SKILL.md`. Treat `SKILL.md` as the
procedure SSOT; this brief is the invocation package only.

Initiative-closure lane hop on the **meta** checkout: delete only Validation /
Resolution for this initiative; refuse PRD and Impact-Map. Do not merge.
Never apply `*-lgtm`. On pass, fill `handoff.forge` for closure `open_draft_pr`.

## Envelope navigation (required)
Derive `next_candidates` and `human_checkpoint` from pinned `workflow.yaml` for
`(stage: purge-initiative-artifacts-meta, outcome)`. `human_checkpoint` is `true`
only when the resolved next node's `type` is `human-checkpoint`. Happy path
`pass` → `initiative-closure-pr-action` (`external_action: true`).

## Workspace
Root: `{{workspace}}` (meta repo).

## Handoff baton (required)
1. Persist the purge note under `{{workspace}}` and append the `handoff:`
   envelope.
2. Then **overwrite** the file at exactly `{{handoff_path}}` with the same
   `handoff:` envelope.
3. Do not leave `{{handoff_path}}` empty when bound.
