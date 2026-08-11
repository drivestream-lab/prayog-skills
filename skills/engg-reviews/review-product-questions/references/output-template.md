---
schema_version: 1
initiative: {INIT-id}
source_map: {path to PRD-Codebase-Map}
source_map_revision: {N}
source_map_digest: sha256:{hex}
generated_at: {YYYY-MM-DDTHH:MM:SZ}
gate_coupled: false
role: pe
authority: pe_proposal
---

# PE product stance — {INIT-id}

> Optional engg-reviews `/review-product-questions` output.
> These are **PE proposals** grounded in codebase evidence — **not** PM
> approval. Feed into `/post-product-questions` for the Meta PR thread.

## Summary

| Metric | Count |
|--------|-------|
| Questions reviewed | |
| Kept map recommendation | |
| Chose alternative | |
| Custom PE stance | |
| Dropped (do not post) | |
| Needs PM only (no PE rec) | |

## Stances

| ID | Title | pe_action | Refined PE recommendation |
|----|-------|-----------|---------------------------|
| Q-01 | | keep-recommendation / choose-alternative / custom-stance / drop-question / needs-pm-only | |

### Q-01 — detail

- **PRD ref:** …
- **Delta:** …
- **Scenario:** …
- **Example:** …
- **PE recommendation (final for post):** …
- **Why:** …
- **Alternatives (remaining):** …
- **Evidence:** …
- **pe_action:** …
- **Notes:** …

## Next

Run `/post-product-questions` with this file as preferred stance input (else raw map).

```yaml
handoff:
  contract: engg-reviews/v1
  stage: review-product-questions
  outcome: pass
  artifact:
    path: out/reports/PE-Product-Stance-{INIT-id}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    gate_coupled: false
    role: pe
    authority: pe_proposal
  next_candidates:
    - post-product-questions
  human_checkpoint: true
  external_action: false
```
