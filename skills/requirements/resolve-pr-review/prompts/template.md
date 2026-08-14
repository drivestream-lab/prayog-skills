# Invoke: resolve-pr-review

You are executing the **resolve-pr-review** skill (Gate 1 PR comment resolution).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Parse a PE/tech-lead review comment on a Gate 1 meta PR; fix PRD and satellite
docs; re-validate; regenerate impact map from scratch; run consistency checks;
prepare a draft reply. Do not post without user approval.

Follow the full procedure in this skill's `SKILL.md`. Treat `SKILL.md` as the
procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Address every numbered finding in the reviewer comment.
2. PRD is SSOT — regenerate impact map; never patch inline.
3. Re-run validation with incremented `report_revision` after PRD edits.
4. Compute H2/artifact digests from committed map text; verify reproducibility.
5. Derive map handoff routing from pinned `workflow.yaml` (BLOCKED vs READY).
6. Sync outline, validation report, PR body; update live PR body via REST API.
7. Never claim authorization without in-thread evidence.

## Envelope navigation (required)
After choosing map `outcome`, derive `next_candidates` and `human_checkpoint`
from pinned `workflow.yaml` for `(stage: prd-impact-map, outcome)` per
`prayog-skills/references/handoff-envelope.md` (**Derive from pinned workflow**).
Set `human_checkpoint: true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.

## Forge (required awareness)
Content skills fill `handoff.forge` when the pin expects it; they do **not**
execute forge mutations. Human forge skills (`/commit-workspace`,
`/open-draft-pr`, `/create-board-tickets`) or Gateflow ForgeClient apply pin ⋉
handoff. Never apply `*-lgtm`. See
`prayog-skills/references/forge-side-effects.md#content-producers`.

## Workspace
Root: `{{workspace}}`.

## Handoff baton (required)
1. Follow this skill's `SKILL.md`. Persist initiative artifacts under
   `{{workspace}}`.
2. Then **overwrite** the file at exactly `{{handoff_path}}` with the map stage
   `handoff:` envelope (plain YAML or a single fenced yaml block).
3. Do not leave `{{handoff_path}}` empty. Do not rely on chat-only handoff for
   orchestrator continuation.
