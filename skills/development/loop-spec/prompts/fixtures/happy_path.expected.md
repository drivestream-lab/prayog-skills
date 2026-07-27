# Invoke: loop-spec

You are executing the **loop-spec** skill (Loop spec (per-wave implement loop)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: loop-spec

## Instruction
Implement one TASK at a time against the product spec; verify; fix; stop at ground handoff. Do not self-approve.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Prerequisites: pre-implement checklist PASS; plan on develop (spec package merged).
2. After each TASK run check_command and test_command; fix before advancing.
3. Bind each iteration to TASK-* + wave issue + implements REQ-*.
4. When green, hand off to ground-spec before any human checkpoint.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
