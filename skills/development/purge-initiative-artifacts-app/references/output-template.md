# Output template — purge initiative artifacts (app)

Save to `{reports_dir}/Purge-App-{INIT}.md`.

```markdown
# Purge app artifacts — {INIT}

| Field | Value |
|-------|-------|
| Initiative | {INIT} |
| Repo | app |
| Base | develop (closure head) |
| Date | {YYYY-MM-DD} |

## Deleted
- {path}

## Missing (ok)
- {path}

## Refused (KEEP)
- {path} — reason

## Signals
- board_workmanifest: intact (outside tree)
- product_spec_keep: {product_spec_dir}/INIT-*.md
```

Append handoff:

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: purge-initiative-artifacts-app
  outcome: pass
  artifact:
    path: docs/specification/reports/Purge-App-{INIT}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    deleted_count: {n}
    missing_ok_count: {n}
    refused_count: {n}
  next_candidates:
    - purge-initiative-artifacts-meta
  human_checkpoint: false
  external_action: false
```
