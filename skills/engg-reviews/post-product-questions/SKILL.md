---
name: post-product-questions
description: >-
  Phase 1 engg-reviews (PE): after /prd-codebase-map, format product questions
  (scenario, example, recommendation, why, alternatives) and post them on the
  open Meta PRD PR with an explicit request for PM feedback. Does not decide
  product answers, does not edit the PRD, does not run PM skills. Gate-
  independent — never sets impact-map-* labels. PM later pulls the thread,
  updates PRD/outline, and re-runs validate-requirements / update-documents.
disable-model-invocation: true
paths: prd/reports/**
metadata:
  background_eligible: false
  experimental: true
  pack: engg-reviews
  lane: pe
---

# Post product questions (PE → Meta PR)

PE closes the engg-reviews loop by **publishing** codebase-grounded product
questions on the **Meta PRD PR** and asking PM for feedback.

**This is not a PM decision skill.** Do not walk AskQuestion accept/reject
loops. Do not edit `prd/INIT-*.md` or outlines. Do not run
`/validate-requirements`, `/review-findings`, or `/update-documents`.

Question shape: [../references/product-question-template.md](../references/product-question-template.md).  
Handoff: [../references/handoff-adjunct.md](../references/handoff-adjunct.md).

## Lane split

| Role | Action |
|------|--------|
| **PE** | Map → optional `/review-product-questions` → this skill posts on Meta PR |
| **PM (later, meta)** | Read PR comments → update PRD + outline → requirements skills |
| **Gate 1** | Unchanged — still impact-map-lgtm + Approve; this post does not unlock it |

## NON-NEGOTIABLE

1. Input is one `/prd-codebase-map` artifact — do not re-run graphs.
2. Include for each Q: scenario, example, **recommendation**, why, alternatives,
   evidence (so PM can decide without reading code).
3. **No product decisions** in this skill — recommendations are PE proposals only.
4. **No PRD / outline edits.**
5. GitHub comment (or draft body file) only after **explicit PE authorization**.
6. Never set/clear `impact-map-*` or `spec-*` labels.
7. `gate_coupled: false` always.
8. Dual output: local body file under pe-workspace `out/reports/` + Meta PR
   comment when authorized.

## Inputs

1. **Map path** — (REQUIRED) `PRD-Codebase-Map-{INIT}.md`
2. **PE stance** — (OPTIONAL) `PE-Product-Stance-{INIT}.md` from
   `/review-product-questions`. When present, prefer refined recommendations
   and omit dropped questions.
3. **Meta PR** — (REQUIRED) number/URL + repo (e.g. `autrio10x/drivestream-meta` #104)
4. **Mode** — all questions / conflicts-only / PE-selected IDs

## Process

### T0 — Gather

- Parse § Product questions from the map.
- If stance file exists, overlay pe_action / refined recommendations; skip
  `drop-question` rows.
- Resolve Meta PR via `gh pr view` when available.
- Cap: post the same capped set as the map (default ≤10).

### T1 — Format PE feedback request

Write `out/reports/Meta-PR-Product-Questions-{INIT}.md` using
[references/output-template.md](references/output-template.md).

Tone: PE proposing grounded questions + recommended stance; **asking PM to
confirm, adjust, or reject** and then update PRD/outline.

### T2 — Authorize + post

Show the body. Ask PE to authorize Meta PR comment.

```bash
gh pr comment {N} --repo {org}/{meta} --body-file out/reports/Meta-PR-Product-Questions-{INIT}.md
```

If `gh` unavailable: print the file path and exact command; outcome `blocked`
until posted or PE marks `posted-manually`.

### T3 — Handoff

| Outcome | When | next_candidates |
|---------|------|-----------------|
| `pass` | Comment posted (or PE confirms manual post) | `[]` — wait for PM |
| `needs-input` | Meta PR / map missing | `[]` |
| `blocked` | No auth / gh failure | `post-product-questions` |
| `skipped` | PE declines to post | `[]` |

## After this skill (PM lane — not engg-reviews)

1. PM reads Meta PR thread.
2. PM updates PRD + outline.
3. PM re-runs requirements skills (`validate-requirements`, etc.).
4. PE may later re-run `/prd-codebase-map` on a revised PRD (new map revision).
5. Gate 1 remains independent.

## Workflow handoff

Append the envelope from
[../references/handoff-adjunct.md](../references/handoff-adjunct.md).
Use `contract: engg-reviews/v1` and stage `post-product-questions`.

Always `gate_coupled: false`. `external_action: true` only when a Meta PR
comment is the authorized next step (comment ≠ gate labels).
