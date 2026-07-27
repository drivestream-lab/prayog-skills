# Invoke: pre-implement

You are executing the **pre-implement** skill (Pre-implement (wave pre-flight)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: pre-implement

## Instruction
Produce the pre-flight checklist for one wave slice. Do not write product code unless explicitly asked after the checklist.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Gate check first — prior wave Ground Report exists and as-built row is human_approved.
2. Read domain-filtered rules and relevant ADRs; cite concrete paths for this slice.
3. Resolve check/test/verify/ground commands; stop on MISSING command.
4. Stop if plan source-freshness or impact-map revision/scope digest is stale.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
