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

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
