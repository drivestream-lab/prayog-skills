# Invoke: verify

You are executing the **verify** skill (Verify (live verify discipline)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Clarify or run live-verify vs unit for one feature. Write
`Live-Verify-{INIT}-W{N}.md` with expected-versus-observed evidence. Bind
environment and build at runtime. No overlap between unit and verify for the
same behavior. Command execution is verification tooling — never commit,
update PR/tracker, or apply labels; emit Forge readiness when publication is
needed.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Resolve unit_tests_dir / live_verify_dir / debug_tests_dir from profile. Follow verify-policy layer ownership (unit, integration/contract, smoke, sandbox, debug).
2. Live verify proves the feature on a running stack; human runs at checkpoint `live-verify`; debug is not gating. Sandbox runs require cleanup and stop conditions.
3. Require expected-versus-observed human evidence in `Live-Verify-*`. Forbid duplicating unit-only assertions in smoke/sandbox.
4. Use toolchain commands from tests_readme/profile — do not hardcode stack commands. Live verify_command is not unit / make test.
5. Do not skip documented prerequisites (running server, bootstrap, config).
6. This skill is optional (`dispatch: manual`); Pass-1 stop is human-checkpoint `live-verify`, not auto `/verify`.
7. Select outcome deterministically (`pass` / `skipped` / `findings` / `blocked` / `failed`) per `SKILL.md`.

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: {{skill_id}}, outcome)` per
`references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
Never set `true` on skill→skill edges (for example never on
`pre-implement` / `loop-spec` / `verify` `pass`).
Example: `verify` + `pass`/`skipped` → `learning-extract` → `human_checkpoint: false`.


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
