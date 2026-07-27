# Invoke: verify

You are executing the **verify** skill (Verify (live verify discipline)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Clarify or run live-verify vs unit for one feature. No overlap between unit and verify for the same behavior.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Resolve unit_tests_dir / live_verify_dir / debug_tests_dir from profile.
2. Live verify proves the feature on a running stack; debug is not gating.
3. Use toolchain commands from tests_readme/profile — do not hardcode stack commands.
4. Do not skip documented prerequisites (running server, bootstrap, config).

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
