# Invoke: update-documents

You are executing the **update-documents** skill (Update documents (propagate approved changes)).

## Bound context
- ticket: {{ticket}}
- initiative: {{initiative}}
- handoff_path: {{handoff_path}}
- workspace: {{workspace}}
- skill_id: {{skill_id}}

## Instruction
Propagate verified decisions across related documents. Decide where, not what.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Resolution mode: consume approved Resolution without re-deciding semantics.
2. Present an exact change manifest; apply only approved edits.
3. Run inline consistency verification after edits.
4. Preserve product ids (CAP-*/REQ-*/OQ-*) when the resolution requires it.

## Workspace
Root: `{{workspace}}`. Prefer the latest handoff artifact at `{{handoff_path}}` when relevant to this skill.
