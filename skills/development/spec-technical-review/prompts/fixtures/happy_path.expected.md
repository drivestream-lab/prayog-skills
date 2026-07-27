# Invoke: spec-technical-review

You are executing the **spec-technical-review** skill (Spec technical review (TDD / ADRs)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: spec-technical-review

## Instruction
Resolve engineering decisions that block planning. Produce TDD and draft ADRs. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks in references/checks.md.
2. Every engineering decision resolved or explicitly deferred with risk + default.
3. Route only product-scope questions to the meta PRD PR — do not ask PM for architecture choices.
4. Commit TDD/ADRs to the Draft spec PR; Gate 2 stays spec-pending until plan exists.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
