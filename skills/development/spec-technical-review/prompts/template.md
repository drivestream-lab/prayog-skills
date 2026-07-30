# Invoke: spec-technical-review

You are executing the **spec-technical-review** skill (Spec technical review (TDD / ADRs)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Resolve engineering decisions that block planning. Produce TDD and draft ADRs. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks in references/checks.md (T1–T12).
2. Every engineering decision resolved or explicitly deferred with risk + default.
3. Route only product-scope questions to the meta PRD PR — do not ask PM for architecture choices. ADR acceptance requires approved REQ-* bindings; never invent user-visible behavior (T12).
4. Persist TDD/ADRs locally and fill Forge readiness (`/commit-workspace`); never commit/push/open PRs/apply labels. Gate 2 stays spec-pending until plan exists.
5. Select workflow outcome from the stage rubric (`pass` / `findings` / `needs-input` / `blocked` / `stale` / `failed`).

## Envelope navigation (required)
After choosing `outcome`, derive `next_candidates` and `human_checkpoint` from
pinned `workflow.yaml` for `(stage: {{skill_id}}, outcome)` per
`references/handoff-envelope.md` (**Derive from pinned workflow**).
`human_checkpoint` is `true` only when the resolved next node's `type` is
`human-checkpoint` — never because the artifact should be reviewed.
Never set `true` on skill→skill edges (for example never on
`pre-implement` / `loop-spec` / `verify` `pass`).


## Forge (required awareness)
Content skills write local artifacts and fill `handoff.forge` when the pin
expects it; they do **not** execute forge mutations. Human forge skills
(`/commit-workspace`, `/open-draft-pr`, `/create-board-tickets`) or Gateflow
ForgeClient apply pin ⋉ handoff. Never apply `*-lgtm`. See
`references/forge-side-effects.md#content-producers`.

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
