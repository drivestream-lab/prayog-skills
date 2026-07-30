# Invoke: pre-implement

You are executing the **pre-implement** skill (Pre-implement (wave pre-flight)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: /tmp/handoff-baton.yaml
- workspace: /workspace/example-repo
- skill_id: pre-implement

## Instruction
Produce the gate-only pre-flight checklist for one wave slice. Write
`{reports_dir}/Pre-Implement-{INIT}-W{N}.md`. Never open a branch and never
implement product code — even if asked; implementation belongs to `/loop-spec`.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Gate check first — prior wave Ground Report exists and as-built row is human_approved. Board/branch/PR state is read-only.
2. Consume canonical §9 WorkManifest (`prayog/v1`); fail closed when `workmanifest_contract` fails, a TASK lacks exit proof, or an applicable wave lacks live-verification contract/script.
3. Read domain-filtered rules and relevant ADRs; cite concrete paths for this slice.
4. Resolve check/test/verify/ground commands; stop on MISSING command. When P15 applies, live `verify_command` under `live_verify_dir` is required (not unit / N/A).
5. Stop if plan source-freshness or impact-map revision/scope digest is stale.
6. When board/wave-head readiness is absent: emit Forge/external-action readiness — do not invoke mutation.
7. Human runs the co-shipped live script at checkpoint `live-verify`; this skill does not execute it.
8. Select outcome deterministically (`pass` / `needs-input` / `blocked` / `stale` / `failed`) per `SKILL.md`.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: pre-implement, outcome)` per
`references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
Never set `true` on skill→skill edges (for example never on
`pre-implement` / `loop-spec` / `verify` `pass`).
Example: `pre-implement` + `pass` → `wave-pr-action` (`external-action`) →
`human_checkpoint: false`, `external_action: true`. On pass, fill complete
`handoff.forge` for wave Draft-PR (`title`, `body_path`, `head_ref`, `base_ref`).


## Forge (required awareness)
Content skills fill `handoff.forge` when the pin expects it; they do **not**
execute forge mutations. Human forge skills (`/commit-workspace`,
`/open-draft-pr`, `/create-board-tickets`) or Gateflow ForgeClient apply pin ⋉
handoff. Never apply `*-lgtm`. Never merge. See `references/forge-side-effects.md#content-producers`.

## Workspace
Root: `/workspace/example-repo`.

## Handoff baton (required)
1. Follow this skill's `SKILL.md`. Persist the usual durable artifact under
   `/workspace/example-repo` and append the `handoff:` envelope to that artifact.
2. Then **overwrite** the file at exactly `/tmp/handoff-baton.yaml` with the same
   `handoff:` envelope (plain YAML or a single fenced yaml block).
3. Do not leave `/tmp/handoff-baton.yaml` empty. Do not rely on docs-only or chat-only
   handoff for orchestrator continuation.
4. If `/tmp/handoff-baton.yaml` already contains a prior envelope, you may read it for
   context; your final write replaces it with this stage's envelope.
