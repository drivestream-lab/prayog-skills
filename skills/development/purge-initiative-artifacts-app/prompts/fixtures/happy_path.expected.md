# Invoke: purge-initiative-artifacts-app

You are executing the **purge-initiative-artifacts-app** skill (Delete allowlisted
app working papers after initiative-closure.).

## Bound context
- ticket: PURGE-APP-1001
- initiative: INIT-PURGE-DEMO
- handoff_path: /tmp/handoff-baton.yaml
- workspace: /workspace/example-repo
- skill_id: purge-initiative-artifacts-app

## Instruction
Follow the full procedure in this skill's `SKILL.md`. Treat `SKILL.md` as the
procedure SSOT; this brief is the invocation package only.

Initiative-closure lane hop: delete only the app PURGE allowlist for this
initiative; refuse KEEP paths. Do not open the closure PR here. Do not merge.
Never apply `*-lgtm`. No authorize-before-delete — allowlist is the safety gate.

Publish is walker forge executor when pin `forge.commit_workspace` applies —
recommend `/commit-workspace` when needed.

## Envelope navigation (required)
Derive `next_candidates` and `human_checkpoint` from pinned `workflow.yaml` for
`(stage: purge-initiative-artifacts-app, outcome)`. `human_checkpoint` is `true`
only when the resolved next node's `type` is `human-checkpoint`. Happy path
`pass` → `purge-initiative-artifacts-meta`.

## Workspace
Root: `/workspace/example-repo`.

## Handoff baton (required)
1. Persist the purge note under `/workspace/example-repo` and append the `handoff:`
   envelope.
2. Then **overwrite** the file at exactly `/tmp/handoff-baton.yaml` with the same
   `handoff:` envelope (plain YAML or a single fenced yaml block).
3. Do not leave `/tmp/handoff-baton.yaml` empty when bound.
