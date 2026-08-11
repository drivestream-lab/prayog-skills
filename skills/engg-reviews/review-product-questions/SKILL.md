---
name: review-product-questions
description: >-
  Phase 1 engg-reviews (PE, optional): interactively walk product questions from
  a PRD-Codebase-Map. Lets a product-minded PE refine recommendations (scenario,
  stance, alternatives) before posting to the Meta PR. Writes PE-Product-Stance
  artifact — proposals only, not PM authority. Does not edit the PRD, does not
  set gate labels. Skip and go straight to /post-product-questions if PE does
  not want this pass.
disable-model-invocation: true
paths: prd/reports/**
metadata:
  background_eligible: false
  experimental: true
  pack: engg-reviews
  lane: pe
  optional: true
---

# Review product questions (PE stance — optional)

Interactive pass for a **PE with product perspective**: refine codebase-grounded
questions and **PE recommendations** before `/post-product-questions`.

**Optional.** Some PEs skip this and post the map as-is.  
**Not PM authority.** Refined stances are still proposals for PM on the Meta PR.  
**Not** `/validate-requirements` / `/update-documents` / PRD edits.

Question shape: [../references/product-question-template.md](../references/product-question-template.md).  
Handoff: [../references/handoff-adjunct.md](../references/handoff-adjunct.md).

## When to use

| Use | Skip |
|-----|------|
| PE wants to sharpen scenarios / pick a recommended stance | PE only wants to publish map questions |
| Senior PE owning product tradeoffs with eng evidence | Hand all product calls to PM untouched |

## NON-NEGOTIABLE

1. Read **one** map (or prior stance file) — do not re-run graphs.
2. Present each question with scenario, example, recommendation, why,
   alternatives, evidence before asking how to refine.
3. Prefer AskQuestion when available; otherwise chat options and wait.
4. Record refined **PE stance** into
   `out/reports/PE-Product-Stance-{INIT}.md` (or pe-workspace equivalent).
5. Label every decision as `pe_proposal` — never `pm_approved`.
6. Do **not** edit the PRD or outline.
7. `gate_coupled: false`. No `impact-map-*` / `spec-*` mutations.
8. After this skill, typical next step is `/post-product-questions` (uses stance
   file when present).

## Inputs

1. **Map path** — (REQUIRED) `PRD-Codebase-Map-{INIT}.md`
2. **Mode** — all / conflicts-only / PE-selected IDs

## Process

### Phase 1 — Setup

- Parse § Product questions (`Q-NN`).
- Summarize counts by delta.
- Entry gate AskQuestion:

```text
- refine-all — Walk all questions interactively
- conflicts-only — Walk conflict/partial only
- skip — Skip; go to /post-product-questions with raw map
```

### Phase 2 — Per question (PE refine)

For each selected question, show full template fields, then:

**Map recommendation:** …  
**Why:** …

AskQuestion:

```text
- keep-recommendation — Keep map recommendation as PE stance
- choose-alternative — Prefer alternative A/B (ask which; capture wording)
- custom-stance — PE provides different recommended product stance
- drop-question — Do not post this Q (record reason)
- needs-pm-only — Post Q but clear PE recommendation (PM must decide cold)
```

Record: question id, pe_action, refined_recommendation, notes.

### Phase 3 — Stance artifact

Write [references/output-template.md](references/output-template.md).  
Chat summary: kept / changed / dropped counts.

### Phase 4 — Handoff

| Outcome | When | next_candidates |
|---------|------|-----------------|
| `pass` | Stance file written | `post-product-questions` |
| `skipped` | PE skipped entry gate | `post-product-questions` |
| `needs-input` | Stopped mid-walk | `review-product-questions` |

## Workflow handoff

Append the envelope from
[../references/handoff-adjunct.md](../references/handoff-adjunct.md).
Use `contract: engg-reviews/v1` and stage `review-product-questions`.

Always `gate_coupled: false`. Does not navigate `sdd-delivery/v2`.
