# engg-reviews (experimental)

Gate-independent **PE** advisory skills: map an open **meta PRD PR** onto a
**fleet of app repos** using **as-built + in-depth code graphs**, optionally
refine PE stance interactively, then **post product questions on the Meta PR**
so PM can strengthen the PRD.

| | |
|--|--|
| **Contract** | `engg-reviews/v1` (adjunct — **not** `sdd-delivery/v2`) |
| **Phase** | 1 — local Graphify MVP |
| **Branch / tag** | `features/rc-2` · distribute as **`pe-rc-2`** · version `0.5.0-rc.2` |
| **Lane** | **PE only** — does not replace PM requirements skills |
| **Profiles** | **Not** registered in `profiles/*.yaml` |

Plan: [docs/engg-reviews-implementation-plan.md](../../docs/engg-reviews-implementation-plan.md)

## Install (PE distribution — tag `pe-rc-2`)

```bash
curl -fsSL https://raw.githubusercontent.com/drivestream-lab/prayog-skills/pe-rc-2/scripts/install_engg_reviews.py \
  -o /tmp/install_engg_reviews.py

python3 /tmp/install_engg_reviews.py --target /path/to/pe-workspace --ref pe-rc-2
```

Or from a checkout:

```bash
python3 scripts/install_engg_reviews.py --target /path/to/pe-workspace --local-source .
# or: ./scripts/install-engg-reviews.sh --target /path/to/pe-workspace --ref pe-rc-2
```

Links **all** `skills/engg-reviews/*/SKILL.md` packages into
`{target}/.agents/skills/` and copies helpers from `templates/`.

## Non-negotiables

1. Does **not** unlock Gate 1 or `/spec-draft`.
2. Never mutates `impact-map-*` or `spec-*` labels.
3. Handoff `gate_coupled: false`; `next_candidates` only engg-reviews stages.
4. Phase 1 evidence engine: local Graphify (`uv tool install graphifyy`).
5. Prefer `EXTRACTED` graph edges; do not treat `INFERRED` alone as `exists`.
6. **PE proposes; PM decides** — interactive review refines **PE stance** only;
   it is not PM approval and does not edit the PRD.

## Skills (PE)

| Skill | Purpose | Required? |
|-------|---------|-------------|
| [`ensure-repo-graph`](ensure-repo-graph/SKILL.md) | Sync fleet `@ develop`, build/refresh graphs | Usual |
| [`prd-codebase-map`](prd-codebase-map/SKILL.md) | PRD × as-built × graph → map + product questions | Yes |
| [`review-product-questions`](review-product-questions/SKILL.md) | Interactive PE stance refine → `PE-Product-Stance-*.md` | **Optional** |
| [`post-product-questions`](post-product-questions/SKILL.md) | Post Qs + PE recommendations on Meta PR; ask PM feedback | Yes (to publish) |

## PE runbook (Phase 1)

```text
1. Open Cursor on {fleet}/pe-workspace/
2. ./bin/refresh-graph.sh <repo> [--with-docs]
3. /ensure-repo-graph
4. /prd-codebase-map
5. /review-product-questions   # optional — product-minded PE
6. /post-product-questions     # Meta PR comment (authorized)
7. Stop (PE). Wait for PM.
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
