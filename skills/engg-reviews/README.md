# engg-reviews (experimental)

Gate-independent **PE** advisory skills: map an open **meta PRD PR** onto a
**fleet of app repos** using **as-built + in-depth code graphs**, then **post
product questions on the Meta PR** so PM can strengthen the PRD.

| | |
|--|--|
| **Contract** | `engg-reviews/v1` (adjunct — **not** `sdd-delivery/v2`) |
| **Phase** | 1 — local Graphify MVP |
| **Branch** | `features/rc-2` / version `0.5.0-rc.2` |
| **Lane** | **PE only** — does not replace PM requirements skills |
| **Profiles** | **Not** registered in `profiles/*.yaml` |

Plan: [docs/engg-reviews-implementation-plan.md](../../docs/engg-reviews-implementation-plan.md)

## Non-negotiables

1. Does **not** unlock Gate 1 or `/spec-draft`.
2. Never mutates `impact-map-*` or `spec-*` labels.
3. Handoff `gate_coupled: false`; `next_candidates` only engg-reviews stages.
4. Phase 1 evidence engine: local Graphify (`uv tool install graphifyy`).
5. Prefer `EXTRACTED` graph edges; do not treat `INFERRED` alone as `exists`.
6. **PE posts questions; PM decides** — engg-reviews never runs interactive PM
   accept/reject loops or edits the PRD.

## Skills (PE)

| Skill | Purpose |
|-------|---------|
| [`ensure-repo-graph`](ensure-repo-graph/SKILL.md) | Sync fleet `@ develop`, build/refresh graphs |
| [`prd-codebase-map`](prd-codebase-map/SKILL.md) | PRD × as-built × graph → map + product questions |
| [`post-product-questions`](post-product-questions/SKILL.md) | Post Qs + PE recommendations on Meta PR; ask PM feedback |

## PE runbook (Phase 1)

```text
1. Open Cursor on {fleet}/pe-workspace/
2. ./bin/refresh-graph.sh <repo> [--with-docs]
3. /ensure-repo-graph
4. /prd-codebase-map       → out/reports/PRD-Codebase-Map-{INIT}.md
5. /post-product-questions → gh pr comment on Meta PR (authorized)
6. Stop (PE). Wait for PM.
```

## PM follow-up (requirements lane — not this pack)

```text
1. Read Meta PR comment thread
2. Update PRD + outline
3. /validate-requirements  (and /update-documents / /review-findings as needed)
4. Gate 1 still: impact-map-lgtm + Approve when ready
```

Preferred layout: [prd-codebase-map/references/layout-defaults.md](prd-codebase-map/references/layout-defaults.md).

## Shared references

- [codegraph-provider.md](references/codegraph-provider.md)
- [handoff-adjunct.md](references/handoff-adjunct.md)
- [product-question-template.md](references/product-question-template.md)
