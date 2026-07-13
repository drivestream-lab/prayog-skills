# Board seed report — {INITIATIVE}

## Board binding (governance SSOT)

| Field | Value |
|-------|-------|
| Org | {org} |
| Board name | {governance.project_board.name} |
| Board number | {number or N/A} |
| Board URL | {url} |
| Governance path | {meta_repo}/config/governance-{org}.yaml |
| Plan §9 target.project | {manifest.target.project} |
| Binding match | MATCH / MISMATCH (governance wins) |

## Spec merge evidence

| Field | Value |
|-------|-------|
| Integration branch | {branch} @ {sha} |
| Plan path | {reports_dir}/Implementation-Plan-{initiative}.md |
| Spec PR | {url or N/A} |
| spec-lgtm on merge head | verified / not verified / N/A |

## Seed plan

| Item | Action | Repo | Title |
|------|--------|------|-------|
| EPIC | create / exists / link | {repo} | {epic.title} |
| W0 | create / exists / link-parent | {repo} | {work[0].title} |
| W1 | … | | |

## Executed commands (authorized apply only)

```bash
# EPIC
gh issue create --repo {org}/{repo} \
  --title "{epic.title}" \
  --label "{initiative}" \
  --project "{board_name}" \
  --body-file /tmp/epic-body.md

# Wave (repeat per Wn)
gh issue create --repo {org}/{repo} \
  --title "{wave.title}" \
  --label "{initiative}" \
  --parent {EPIC#} \
  --project "{board_name}" \
  --body-file /tmp/w{n}-body.md
```

## Result tree

| Role | Issue | URL | On board | Sub-issue of EPIC |
|------|-------|-----|----------|-------------------|
| EPIC | #{n} | {url} | yes/no | — |
| W0 | #{n} | {url} | yes/no | yes/no |

## Project fields (manual if API cannot set)

Set on programme Project for each item:

- **Initiative:** `{initiative}`
- **Codebase:** `{repo slug}`
- **Spec path:** from §9 `spec_path`
- **Status:** Backlog

---

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: board-seed
  outcome: pass | blocked | failed
  artifact:
    path: null
    digest: null
  blockers: []
  signals:
    initiative: {INITIATIVE}
    board_name: {board_name}
    board_url: {url}
    epic_issue: {url}
    waves_seeded: [W0, W1, ...]
    repo: {codebase repo}
    stack_profile: {from .harness/profile.yaml — informational only}
  next_candidates:
    - pre-implement
  human_checkpoint: true
  external_action: true
```
