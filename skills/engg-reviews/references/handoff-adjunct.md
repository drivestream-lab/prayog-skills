# engg-reviews adjunct handoff

engg-reviews uses contract **`engg-reviews/v1`**. This is **not**
`sdd-delivery/v2`. Navigators of the SDD delivery workflow must **ignore**
these handoffs for Gate 1 / Gate 2 / `spec-draft` transitions.

## Envelope

```yaml
handoff:
  contract: engg-reviews/v1
  stage: ensure-repo-graph | prd-codebase-map | post-product-questions
  outcome: pass | findings | needs-input | blocked | stale | failed | skipped
  artifact:
    path: {durable path or null}
    digest: sha256:{hex} | null
  blockers: []
  signals:
    gate_coupled: false
    codegraph_provider: local-graphify | mcp-falkordb | degraded-none
    grounding_depth: deep | none
  next_candidates: []
  human_checkpoint: true
  external_action: false
```

## Hard rules

1. Always set `gate_coupled: false`.
2. `next_candidates` may only list engg-reviews stages:
   - `ensure-repo-graph`
   - `prd-codebase-map`
   - `post-product-questions`
   - empty list
3. **Never** put `gate-1`, `prd-merge`, `spec-draft`, `impact-map-pending`,
   or any `sdd-delivery/v2` node in `next_candidates`.
4. `external_action: false` by default. Posting meta PR comments requires
   explicit user authorization and still does **not** set gate labels.
5. Mutating `impact-map-*` or `spec-*` labels from engg-reviews is forbidden.
6. Chat summaries may repeat the handoff; the durable artifact is source of
   truth.

## Outcome vocabulary

Same words as delivery contract for familiarity — different authority:

| Outcome | Meaning in engg-reviews |
|---------|-------------------------|
| `pass` | Stage work complete (graphs fresh / map written / questions reviewed) |
| `findings` | Durable product questions or gaps need human resolution |
| `needs-input` | Missing PRD, repos, or authorization |
| `blocked` | Provider missing, clone failed, or policy stop |
| `stale` | PRD digest or graph SHA no longer matches |
| `failed` | Tool/execution failure |
| `skipped` | Legitimately N/A (e.g. greenfield short-circuit noted) |

`pass` here never means “approved for Gate 1” or “ready for `/spec-draft`”.
