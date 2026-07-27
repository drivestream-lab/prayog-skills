# Invoke: review-findings

You are executing the **review-findings** skill (Review findings (interactive resolution)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Walk findings from one validation/audit report; collect decisions; write a Resolution summary.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Read ONE report file — do not re-run checks or re-read source documents.
2. Present each finding as a decision brief via structured questions.
3. Produce Resolution with VF→CHG linkage at canonical Resolution-{INIT}.md path.
4. Do not invent findings; work only from the report.

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
