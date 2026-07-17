---
schema_version: 1
initiative: {INIT-id}
map_revision: {N}
source_prd: prd/{INIT-id}.md
source_prd_digest: sha256:{hex}
meta_pr_head_sha: {sha or null}
previous_revision: {N-1 or null}
change_reason: {initial map or concise revision reason}
codegraph_provider: local-graphify
grounding_depth: deep | none
generated_at: {YYYY-MM-DDTHH:MM:SSZ}
gate_coupled: false
---

# PRD codebase map — {INIT-id} — revision {N}

> engg-reviews experimental artifact. **Does not** approve Gate 1 or authorize
> `/spec-draft`. Product questions help PM strengthen the PRD.

## 1. Fleet graph status

| Repo | develop_sha | graph_digest | Freshness | As-built path |
|------|-------------|--------------|-----------|---------------|
| {org/repo} | {sha} | sha256:{hex} | CURRENT / STALE / MISSING | {path or none} |

## 2. Capability matrix

| ID | PRD ref | Primary repo | As-built today | Graph evidence (node/path) | Confidence | Delta |
|----|---------|--------------|----------------|----------------------------|------------|-------|
| M-01 | {§ / capability} | {repo} | {summary or none} | {query/path summary} | EXTRACTED / INFERRED / MIXED / NONE | exists / partial / absent / conflict / unknown |

## 3. Product questions

> Cap {N}. Priority: conflict → partial → unknown. Template:
> [product-question-template.md](../../references/product-question-template.md)

### Q-01 — {short title}

- **PRD ref:** …
- **Repos(s):** …
- **Delta:** conflict | partial | unknown
- **Scenario:** When …
- **Example:** …
- **Recommendation:** …
- **Why:** …
- **Alternatives:**
  - A: …
  - B: …
- **Evidence:** …

### Q-02 — …

## 4. Matrix summary (no question)

| Delta | Count | IDs |
|-------|-------|-----|
| exists | | |
| partial | | |
| absent | | |
| conflict | | |
| unknown | | |

## 5. Engineering appendix (not for PM)

| Topic | Repo | Detail |
|-------|------|--------|
| Communities / god nodes | | |
| Notable paths | | |
| ADR touches (behaviour only) | | |

## 6. Checks

| ID | Result | Notes |
|----|--------|-------|
| C0–C12 | PASS / FAIL / SKIPPED | |

## 7. Chat summary (also print in session)

```text
PRD codebase map {INIT} rev {N}
- Repos mapped: {list}
- Grounding: deep | none
- Questions open: {count} (conflict={n}, partial={n}, unknown={n})
- Artifact: prd/reports/PRD-Codebase-Map-{INIT}.md
- Gates: unchanged (gate_coupled=false)
Next: optional /review-product-questions (PE stance), then /post-product-questions (Meta PR)
```

## 8. Handoff

```yaml
handoff:
  contract: engg-reviews/v1
  stage: prd-codebase-map
  outcome: findings
  artifact:
    path: prd/reports/PRD-Codebase-Map-{INIT-id}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    gate_coupled: false
    codegraph_provider: local-graphify
    grounding_depth: deep
    open_question_count: {N}
  next_candidates:
    - review-product-questions
    - post-product-questions
  human_checkpoint: true
  external_action: false
```
