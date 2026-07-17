# Fleet graph status — {INIT-id}

> engg-reviews Phase 1. Gate-independent. Not an SDD delivery artifact.

```yaml
initiative: {INIT-id}
generated_at: {YYYY-MM-DDTHH:MM:SSZ}
codegraph_provider: local-graphify
integration_branch: develop
candidate_source: impact-map rev {N} | pe-list | catalog-hint
```

## Fleet table

| Repo | Local path | develop_sha | graph_digest | Status | Notes |
|------|------------|-------------|--------------|--------|-------|
| {org/repo} | ../{repo} | {sha} | sha256:{hex} | CURRENT/BUILT/UPDATED/FAILED/BLOCKED | |

## Provider

| Check | Result |
|-------|--------|
| `graphify` on PATH / uv tool | pass / fail |
| Mode | deep / update |
| Failures | none / {list} |

## Next

- If all required rows CURRENT/BUILT/UPDATED → run `/prd-codebase-map`
- If any FAILED/BLOCKED → fix clones/provider and re-run `/ensure-repo-graph`

```yaml
handoff:
  contract: engg-reviews/v1
  stage: ensure-repo-graph
  outcome: pass
  artifact:
    path: prd/reports/Graph-Fleet-Status-{INIT-id}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    gate_coupled: false
    codegraph_provider: local-graphify
    grounding_depth: deep
  next_candidates:
    - prd-codebase-map
  human_checkpoint: true
  external_action: false
```
