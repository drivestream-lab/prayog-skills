# Invoke: spec-technical-review

You are executing the **spec-technical-review** skill (Spec technical review (TDD / ADRs)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Resolve engineering decisions that block planning. Produce TDD and draft ADRs. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Never skip checks in references/checks.md.
2. Every engineering decision resolved or explicitly deferred with risk + default.
3. Route only product-scope questions to the meta PRD PR — do not ask PM for architecture choices.
4. Commit TDD/ADRs to the Draft spec PR; Gate 2 stays spec-pending until plan exists.

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
