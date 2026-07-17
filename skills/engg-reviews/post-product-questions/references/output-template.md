---
schema_version: 1
initiative: {INIT-id}
source_map: {path to PRD-Codebase-Map}
source_map_revision: {N}
source_map_digest: sha256:{hex}
meta_pr: {org}/{meta}#{N}
meta_pr_url: {url}
generated_at: {YYYY-MM-DDTHH:MM:SSZ}
gate_coupled: false
role: pe-advisory
---

# PE product questions for PM — {INIT-id}

> Posted by **engineering (PE)** from engg-reviews `/post-product-questions`.
> These are **proposals**, not decisions. Please reply on this PR (or update the
> PRD/outline) with accept / adjust / reject per question, then re-run PM
> requirements skills as needed.
>
> This comment does **not** change Gate 1 labels (`impact-map-*`).

## Ask for PM

Please:
1. Read each question (scenario + PE recommendation).
2. Reply with your product stance (or edit the PRD directly).
3. Update `prd/{INIT}.md` and outline as needed.
4. Re-run `/validate-requirements` (and `/update-documents` if using a resolution file).

## Summary

| Delta | Count | IDs |
|-------|-------|-----|
| conflict | | |
| partial | | |
| unknown | | |

## Questions

### Q-01 — {short title}

- **PRD ref:** …
- **Repos(s):** …
- **Delta:** conflict | partial | unknown
- **Scenario:** When …
- **Example:** …
- **PE recommendation:** …
- **Why (PE):** …
- **Alternatives:**
  - A: …
  - B: …
- **Evidence:** {repo} · {graph/as-built} · EXTRACTED|INFERRED
- **PM response needed:** accept-recommendation / choose-alternative / custom / defer-as-open-question

### Q-02 — …

## Map artifact

- Local/meta path: `{PRD-Codebase-Map path}`
- Revision: `{N}`

```yaml
handoff:
  contract: engg-reviews/v1
  stage: post-product-questions
  outcome: pass
  artifact:
    path: out/reports/Meta-PR-Product-Questions-{INIT-id}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    gate_coupled: false
    meta_pr: "{org}/{meta}#{N}"
    posted: true
    role: pe
  next_candidates: []
  human_checkpoint: true
  external_action: false
```
