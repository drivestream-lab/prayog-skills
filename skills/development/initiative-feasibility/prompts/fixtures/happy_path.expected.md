# Invoke: initiative-feasibility

You are executing the **initiative-feasibility** skill (Initiative feasibility).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: initiative-feasibility

## Instruction
Assess whether the repo spec slice is buildable against the current codebase. Flag only — do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks in references/checks.md; evidence for every finding.
2. Verify source freshness (PRD digest, impact-map revision/scope, approval) before analysis.
3. Commit the feasibility report to the open Draft spec PR; keep Gate 2 as spec-pending.
4. 4-lane triage for open items; do not set spec-lgtm.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
