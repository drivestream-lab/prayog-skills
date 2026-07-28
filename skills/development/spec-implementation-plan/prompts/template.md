# Invoke: spec-implementation-plan

You are executing the **spec-implementation-plan** skill (Spec implementation plan).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Produce a wave-level plan with REQ/TASK/FILE/TEST tables and §9 WorkManifest seed. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks; every TASK has done-when, Implements REQ-*, and toolchain commands.
2. No shadow REQ-W* ids; wave ids W0, W1, … only.
3. Commit plan to the open Draft spec PR; board seeding happens after merge via board-seed.
4. Verify source freshness against canonical handoff before planning.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: {{skill_id}}, outcome)` per
`references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
Never set `true` on skill→skill edges (for example never on
`pre-implement` / `loop-spec` / `verify` `pass`).


## Forge (required awareness)
Content skills fill `handoff.forge` when the pin expects it; they do **not**
execute forge mutations. Human forge skills (`/commit-workspace`,
`/open-draft-pr`, `/create-board-tickets`) or Gateflow ForgeClient apply pin ⋉
handoff. Never apply `*-lgtm`. See `references/forge-side-effects.md#content-producers`.

## Workspace
Root: `{{workspace}}`.

## Handoff baton (required)
1. Follow this skill's `SKILL.md`. Persist the usual durable artifact under
   `{{workspace}}` and append the `handoff:` envelope to that artifact.
2. Then **overwrite** the file at exactly `{{handoff_path}}` with the same
   `handoff:` envelope (plain YAML or a single fenced yaml block).
3. Do not leave `{{handoff_path}}` empty. Do not rely on docs-only or chat-only
   handoff for orchestrator continuation.
4. If `{{handoff_path}}` already contains a prior envelope, you may read it for
   context; your final write replaces it with this stage's envelope.
