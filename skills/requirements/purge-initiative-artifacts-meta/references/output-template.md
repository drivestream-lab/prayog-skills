# Output template — purge initiative artifacts (meta)

Save to `{reports_dir}/Purge-Meta-{INIT}.md`.

```markdown
# Purge meta artifacts — {INIT}

| Field | Value |
|-------|-------|
| Initiative | {INIT} |
| Repo | meta |
| Base | develop (closure head) |
| Date | {YYYY-MM-DD} |

## Deleted
- {path}

## Missing (ok)
- {path}

## Refused (KEEP)
- {path} — reason

## Signals
- prd_keep: prd/{INIT}.md
- impact_map_keep: Impact-Map-{INIT}.md
```

Append handoff:

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: purge-initiative-artifacts-meta
  outcome: pass
  artifact:
    path: prd/reports/Purge-Meta-{INIT}.md
    digest: sha256:{hex}
  blockers: []
  signals:
    deleted_count: {n}
    missing_ok_count: {n}
    refused_count: {n}
    pr_ready: true
  next_candidates:
    - initiative-closure-pr-action
  human_checkpoint: false
  external_action: true
  forge:
    action: open_draft_pr
    draft: true
    apply_labels: []
    title: "Initiative closure purge: {INIT}"
    body_path: prd/reports/Purge-Meta-{INIT}.md
```
