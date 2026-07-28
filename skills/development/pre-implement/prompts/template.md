# Invoke: pre-implement

You are executing the **pre-implement** skill (Pre-implement (wave pre-flight)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Produce the pre-flight checklist for one wave slice. Do not write product code unless explicitly asked after the checklist.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Gate check first — prior wave Ground Report exists and as-built row is human_approved.
2. Read domain-filtered rules and relevant ADRs; cite concrete paths for this slice.
3. Resolve check/test/verify/ground commands; stop on MISSING command.
4. Stop if plan source-freshness or impact-map revision/scope digest is stale.

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
