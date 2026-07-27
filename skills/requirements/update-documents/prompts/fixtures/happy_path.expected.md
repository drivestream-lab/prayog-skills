# Invoke: update-documents

You are executing the **update-documents** skill (Update documents (propagate approved changes)).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: update-documents

## Instruction
Propagate verified decisions across related documents. Decide where, not what.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Resolution mode: consume approved Resolution without re-deciding semantics.
2. Present an exact change manifest; apply only approved edits.
3. Run inline consistency verification after edits.
4. Preserve product ids (CAP-*/REQ-*/OQ-*) when the resolution requires it.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
