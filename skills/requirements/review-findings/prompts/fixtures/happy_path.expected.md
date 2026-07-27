# Invoke: review-findings

You are executing the **review-findings** skill (Review findings (interactive resolution)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: review-findings

## Instruction
Walk findings from one validation/audit report; collect decisions; write a Resolution summary.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Read ONE report file — do not re-run checks or re-read source documents.
2. Present each finding as a decision brief via structured questions.
3. Produce Resolution with VF→CHG linkage at canonical Resolution-{INIT}.md path.
4. Do not invent findings; work only from the report.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
