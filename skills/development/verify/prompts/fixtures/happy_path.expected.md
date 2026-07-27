# Invoke: verify

You are executing the **verify** skill (Verify (live verify discipline)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: verify

## Instruction
Clarify or run live-verify vs unit for one feature. No overlap between unit and verify for the same behavior.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Resolve unit_tests_dir / live_verify_dir / debug_tests_dir from profile.
2. Live verify proves the feature on a running stack; debug is not gating.
3. Use toolchain commands from tests_readme/profile — do not hardcode stack commands.
4. Do not skip documented prerequisites (running server, bootstrap, config).

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
