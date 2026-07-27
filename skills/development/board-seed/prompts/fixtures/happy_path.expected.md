# Invoke: board-seed

You are executing the **board-seed** skill (Board seed).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: board-seed

## Instruction
After spec PR merge, seed the programme engineering board from plan §9 WorkManifest. Do not write product code.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Spec merge gate first (Implementation-Plan on integration branch; spec-lgtm when verifiable).
2. Resolve board binding from read-only meta governance; governance wins over plan free text.
3. Idempotent create of EPIC + wave sub-issues; no GitHub mutations without explicit authorization.
4. If gh/project scope missing, print exact commands and stop — do not claim seeded.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
