# Invoke: board-seed

You are executing the **board-seed** skill (Board seed).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
After spec PR merge, seed the programme engineering board from plan §9 WorkManifest. Do not write product code.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Spec merge gate first (Implementation-Plan on integration branch; spec-lgtm when verifiable).
2. Resolve board binding from read-only meta governance; governance wins over plan free text.
3. Idempotent create of EPIC + wave sub-issues; no GitHub mutations without explicit authorization.
4. If gh/project scope missing, print exact commands and stop — do not claim seeded.

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
