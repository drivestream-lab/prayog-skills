# Invoke: pre-implement

You are executing the **pre-implement** skill (Pre-implement (wave pre-flight)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: pre-implement

## Instruction
Produce the pre-flight checklist for one wave slice. Do not write product code unless explicitly asked after the checklist.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Gate check first — prior wave Ground Report exists and as-built row is human_approved.
2. Read domain-filtered rules and relevant ADRs; cite concrete paths for this slice.
3. Resolve check/test/verify/ground commands; stop on MISSING command. When P15 applies, live `verify_command` under `live_verify_dir` is required (not unit / N/A).
4. Stop if plan source-freshness or impact-map revision/scope digest is stale.
5. Human runs the co-shipped live script at checkpoint `live-verify`; this skill does not execute it.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: pre-implement, outcome)` per
`references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
Never set `true` on skill→skill edges (for example never on
`pre-implement` / `loop-spec` / `verify` `pass`).
Example: `pre-implement` + `pass` → `loop-spec` → `human_checkpoint: false`.


## Forge (required awareness)
Content skills fill `handoff.forge` when the pin expects it; they do **not**
execute forge mutations. Human forge skills (`/commit-workspace`,
`/open-draft-pr`, `/create-board-tickets`) or Gateflow ForgeClient apply pin ⋉
handoff. Never apply `*-lgtm`. See `references/forge-side-effects.md#content-producers`.

## Workspace
Root: `/workspace/example-repo`.

## Handoff baton (required)
1. Follow this skill's `SKILL.md`. Persist the usual durable artifact under
   `/workspace/example-repo` and append the `handoff:` envelope to that artifact.
2. Then **overwrite** the file at exactly `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` with the same
   `handoff:` envelope (plain YAML or a single fenced yaml block).
3. Do not leave `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` empty. Do not rely on docs-only or chat-only
   handoff for orchestrator continuation.
4. If `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` already contains a prior envelope, you may read it for
   context; your final write replaces it with this stage's envelope.
