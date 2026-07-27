# Invoke: prd-impact-map

You are executing the **prd-impact-map** skill (PRD impact map).

## Bound context
- ticket: FORGE-1001
- initiative: INIT-PRAYOG-SKILLS-003-PROMPTS
- handoff_path: prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md
- workspace: /workspace/example-repo
- skill_id: prd-impact-map

## Instruction
Map the PRD to affected repos via the service catalog; produce a versioned impact-map artifact.

Follow the full procedure in this skill's `SKILL.md` (and `references/` when present). Treat `SKILL.md` as the procedure SSOT; this brief is the invocation package only.

## Non-negotiables (summary)
1. Read config/service-catalog.yaml before the PRD; match capabilities semantically.
2. Include transitive depends_on impacts; explicitly list not-affected repos with reason.
3. Canonical Impact-Map-{INIT}.md only — bump map_revision; never *-revN siblings.
4. Record PRD digest and one scope_digest per affected repo.
5. No GitHub Draft PR / Gate 1 labels until explicit user authorization.

## Workspace
Root: `/workspace/example-repo`. Prefer the latest handoff artifact at `prd/reports/Impact-Map-INIT-PRAYOG-SKILLS-003-PROMPTS.md` when relevant to this skill.
