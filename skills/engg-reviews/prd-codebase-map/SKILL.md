---
name: prd-codebase-map
description: >-
  Phase 1 engg-reviews: map an open meta PRD onto a fleet of app repos using
  as-built status plus in-depth codegraph evidence (Graphify query/path/explain).
  Produces PRD-Codebase-Map artifact and PM-facing product questions (scenario,
  example, recommendation, why). Gate-independent — does not require
  impact-map-lgtm and never unlocks Gate 1 or /spec-draft. Run after
  /ensure-repo-graph.
disable-model-invocation: true
paths: prd/**, config/service-catalog.yaml
metadata:
  background_eligible: false
  experimental: true
  pack: engg-reviews
---

# PRD codebase map

Ground the **incoming PRD** on **current product reality** (as-built) and
**in-depth codebase structure** (codegraph provider) across candidate repos.
Emit **product questions** so PM can strengthen the PRD on the meta PR.

**Does not implement.** **Does not draft app specs.** **Does not open Gate 1.**

## NON-NEGOTIABLE

1. **Gate-independent.** May run while meta PR is Draft and without
   `impact-map-lgtm`. Never set/clear gate labels. Never unlock `/spec-draft`.
2. Run checks in [references/checks.md](references/checks.md). Mark SKIPPED
   with reason — never silently omit.
3. In-depth evidence only via [codegraph provider](../references/codegraph-provider.md).
   Prefer `EXTRACTED` edges. `INFERRED`/`AMBIGUOUS` alone must not justify
   `exists`.
4. Product questions use [product-question-template.md](../references/product-question-template.md)
   — feature language only. Engineering detail → appendix.
5. As-built vs graph conflicts → product question (`conflict`), not silent pick.
6. Cap open product questions (default **10**); prioritize conflict → partial →
   unknown.
7. Dual output: chat summary + `prd/reports/PRD-Codebase-Map-{INIT}.md`.
8. Handoff contract **`engg-reviews/v1`** only — see
   [handoff-adjunct.md](../references/handoff-adjunct.md).
9. Greenfield / missing as-built + empty graph → short-circuit: PRD-ambiguity
   questions only; set `grounding_depth: none`; do not claim deep grounding.
10. Don't fix the PRD in this skill — flag and question. PE posts via
    `/post-product-questions`; PM updates PRD with requirements skills.

## Inputs

Resolve paths from [references/layout-defaults.md](references/layout-defaults.md).

1. **PRD** — (REQUIRED) `prd/INIT-*.md` + digest + meta PR head SHA if open
2. **Fleet graphs** — (REQUIRED for deep PASS) output of `/ensure-repo-graph`
3. **As-built** — per repo `docs/specification/as-built/implementation-status.md`
   (or profile equivalent)
4. **Impact map** — (OPTIONAL) candidate repos + scope hints
5. **Accepted ADRs** — (OPTIONAL) product-behaviour constraints only
6. **Prior map** — (OPTIONAL) for revision increment

## Process

### T0 — Gather

- Read PRD fully; list capabilities / features / waves to map.
- Load fleet status (SHAs, digests). Stop if required graphs not `CURRENT`.
- Read as-built per candidate repo.

### T1 — Understand

- Build capability inventory with PRD refs.
- Assign primary repo per capability (impact-map / catalog / evidence).

### T2 — Analyze (per capability)

1. Provider `query` with product-language terms.
2. `path` / `explain` for critical nodes; record edge confidence.
3. Compare to as-built row(s).
4. Classify delta: `exists` | `partial` | `absent` | `conflict` | `unknown`.
5. Queue product question if delta is `partial` | `conflict` | high-impact
   `unknown` (and optionally confirm-drop for surprising `exists`).

### T3 — Plan questions

- Apply cap + priority.
- Fill scenario / example / recommendation / why / alternatives.
- Move eng paths/communities to appendix.

### T4 — Execute (write artifact)

- Increment `map_revision` if prior exists.
- Write [references/output-template.md](references/output-template.md).
- Compute artifact digest after save.

### T5 — Verify

- Re-read checks.md; every capability row has evidence or explicit unknown.
- Handoff `gate_coupled: false`; `next_candidates` ⊆ engg-reviews only.

## Outcomes

| Outcome | When | next_candidates |
|---------|------|-----------------|
| `pass` | Matrix complete; no blocking open questions required | `review-product-questions` and/or `post-product-questions` |
| `findings` | Product questions open for PE refine / PM | `review-product-questions` and/or `post-product-questions` |
| `needs-input` | PRD/repos/graphs incomplete | `ensure-repo-graph` or `[]` |
| `blocked` | Provider missing and PE refused degraded mode | `ensure-repo-graph` |
| `stale` | PRD digest or graph SHA mismatch mid-run | `ensure-repo-graph` |
| `failed` | Write/tool failure | `[]` |

## Meta PR comments

Only after explicit authorization: post numbered questions linking to the map
artifact. Still **no** gate label changes.

## Workflow handoff

Append the envelope from
[../references/handoff-adjunct.md](../references/handoff-adjunct.md).
Use `contract: engg-reviews/v1` and stage `prd-codebase-map`.

| Outcome | Next |
|---------|------|
| `pass` / `findings` | Optional `/review-product-questions`, then `/post-product-questions` |
| `needs-input` / `blocked` / `stale` | `/ensure-repo-graph` then retry |
| `failed` | Human fixes tool/write issues; retry |

Always `gate_coupled: false`. **Never** list `gate-1`, `prd-merge`, or
`spec-draft` in `next_candidates`. SDD Gate navigators must ignore this
contract.
