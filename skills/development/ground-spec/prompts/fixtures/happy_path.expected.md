# Invoke: ground-spec

You are executing the **ground-spec** skill (Ground spec (wave grounding)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: ground-spec

## Instruction
Validate the completed wave against product spec REQ rows and repo artifacts; produce a Ground Report.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Run ground_command when defined; otherwise manually map each REQ-* to verifiable artifacts.
2. Check cross-spec contracts against prior waves' Ground Reports.
3. Populate Contracts Produced — required input for next wave pre-implement.
4. Do not mark human_approved — that is a human gate only.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
