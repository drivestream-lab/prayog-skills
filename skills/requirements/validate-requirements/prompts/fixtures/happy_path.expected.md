# Invoke: validate-requirements

You are executing the **validate-requirements** skill (Validate requirements (semantic + structural)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: validate-requirements

## Instruction
Run the validate-requirements procedure. Do not modify the target document.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip a check; mark SKIPPED with reason when inputs are unavailable.
2. Show evidence for every finding (problematic text + source quote where applicable).
3. Don't fix — flag only. Dual output: chat summary + Validation-Report + next steps.
4. Canonical report path only — overwrite Validation-Report-{INIT}.md; never *-revN siblings.
5. Stable finding ids VF-* per id-conventions; prefer REQ-*/CAP-*/OQ-* in Location.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
