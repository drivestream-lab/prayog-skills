# Invoke: loop-spec

You are executing the **loop-spec** skill (Loop spec (per-wave implement loop)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Implement one TASK at a time against the product spec; verify; fix; stop at ground handoff. Do not self-approve.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Prerequisites: pre-implement checklist PASS; plan on develop (spec package merged).
2. After each TASK run check_command and test_command; fix before advancing.
3. Bind each iteration to TASK-* + wave issue + implements REQ-*.
4. When green, hand off to ground-spec before any human checkpoint.

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
