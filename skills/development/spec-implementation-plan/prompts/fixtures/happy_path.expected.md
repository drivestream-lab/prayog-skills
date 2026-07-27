# Invoke: spec-implementation-plan

You are executing the **spec-implementation-plan** skill (Spec implementation plan).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: spec-implementation-plan

## Instruction
Produce a wave-level plan with REQ/TASK/FILE/TEST tables and §9 WorkManifest seed. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks; every TASK has done-when, Implements REQ-*, and toolchain commands.
2. No shadow REQ-W* ids; wave ids W0, W1, … only.
3. Commit plan to the open Draft spec PR; board seeding happens after merge via board-seed.
4. Verify source freshness against canonical handoff before planning.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
