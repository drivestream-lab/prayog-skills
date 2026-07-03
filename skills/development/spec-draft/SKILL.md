---
name: spec-draft
description: >-
  Translate the PRD handoff into a spec slice for this repo. Reads the PRD
  from the prd-handoff PR branch, extracts the capabilities relevant to this
  repo, and drafts docs/specification/product/INIT-*.md. Use immediately after
  the prd-handoff PR is opened and before /initiative-feasibility.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
background_eligible: true
background_trigger: "prd-handoff PR opened in this repo"
---

# Spec draft

Translate the **PRD** into a **spec slice** for this repo. The spec slice is
the engineering team's interpretation of what the PRD means for their codebase.

**Do not implement.** Produce `docs/specification/product/INIT-{id}.md` only.

## Why this skill exists

PM writes PRD in feature language. Engineers own the spec.
This skill bridges the gap — it reads the PRD and drafts structured spec FRs
that the dev team can review, edit, and then run `/initiative-feasibility` on.

## NON-NEGOTIABLE

1. The spec draft is a **starting point** — dev must review and edit before
   committing. Do not present it as authoritative without dev review.
2. Language in the spec must be **engineering terms** — FRs, acceptance criteria,
   module scope — not copied PRD user-story language.
3. Scope must be **bounded to this repo** only. Do not write FRs for other repos.
4. Every FR must trace to a named section or bullet in the PRD.
5. Flag anything in the PRD that is **ambiguous for this repo** — do not guess.
   Put ambiguities in a "Spec questions" section at the bottom.

## Inputs

Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **PRD** — (REQUIRED) from `<client>-meta/prd/INIT-*.md`. Developer provides
   the path or pastes the URL of the prd-handoff PR. Read from the PR branch,
   not `<client>-meta/develop` (PRD may not be merged yet).
2. **prd-handoff PR body** — (REQUIRED) PM's plain-English description of what
   this repo needs to deliver. This is the scope boundary.
3. **As-built** — `implementation-status.md` (REQUIRED) — understand what
   already exists before writing FRs.
4. **Source** — `source_roots` from profile — understand current module structure.
5. **Service profile** — `docs/specification/product/00-service-profile.md` if
   it exists — understand the repo's existing domain.
6. **`adr_dir`** — existing ADRs constrain what this spec can propose.
7. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)

## Process

1. **T0 Gather** — PRD path, prd-handoff PR body, as-built, source, service profile
2. **T1 Understand** — initiative id; what capabilities land in this repo per PRD
   and prd-handoff PR body; what already exists (as-built + source scan)
3. **T2 Scope** — list ONLY what this repo owns. Explicitly exclude what belongs
   to other repos. Cross-service contracts are noted but not spec'd here.
4. **T3 Draft** — write INIT-*.md using [references/output-template.md](references/output-template.md)
5. **T4 Flag** — list ambiguities, open questions, and anything that needs PM
   confirmation before this spec is used for feasibility
6. **T5 Present** — show draft to dev for review; do NOT commit until dev confirms

## Output

Draft saved to `{product_spec_dir}/INIT-{id}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

## Next step

After dev reviews and edits the spec draft:

```
git add docs/specification/product/INIT-{id}.md
git commit -m "feat: spec slice for INIT-{id}"
/initiative-feasibility   ← run this on the committed spec
```
