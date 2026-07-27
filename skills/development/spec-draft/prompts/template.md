# Invoke: spec-draft

You are executing the **spec-draft** skill (Spec draft (repo slice from PRD)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Translate the PRD into a repo-bounded product spec slice. Do not implement.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Write docs/specification/product/INIT-*.md in engineering terms (REQ-*), not PRD user-story prose.
2. Scope this repo only; every REQ-* must trace to a named PRD CAP-*/REQ-* or section.
3. Flag ambiguity — do not guess. Spec is a starting point pending dev review.
4. No GitHub Draft spec PR until explicit user authorization.

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
