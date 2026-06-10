# WorkManifest schema (prayog.meta/v1)

**SSOT loader:** `prayog-meta/scripts/py/prayog_scripts/seed_work.py`  
**Reference manifest:** `prayog-meta/bootstrap/BOOTSTRAP-PRAYOG-000.yaml`

## Required top-level keys

| Key | Type | Notes |
|-----|------|-------|
| `apiVersion` | string | Must be `prayog.meta/v1` |
| `kind` | string | Must be `WorkManifest` |
| `initiative` | string | e.g. `INIT-PRAYOG-001` |
| `metadata` | object | `title`, `summary`, optional `playbook` paths |
| `target` | object | `org`, `project` (required); optional `project_config` |
| `defaults` | object | Merged into every epic + work item |
| `epic` | object | Parent issue; `id` usually `EPIC` |
| `work` | array | Child tasks (issues) |

## Epic block

```yaml
epic:
  id: EPIC
  repo: prayog-meta
  title: "[feature] INIT-PRAYOG-001 — FrostMart MVP"
  codebase: prayog-meta
  spec_path: prd/INIT-PRAYOG-001.md
  verify_command: N/A — §11 manual demo checklist
  labels:
    - initiative
  body: |
    ## Objective
    ...
```

- `kind` is set to `epic` by `seed_work.py` (do not rely on YAML `kind` for epic).
- `parent` is stripped for epic; children use `defaults.parent: EPIC`.

## Work item block

```yaml
work:
  - id: P1
    kind: issue
    repo: prayog-parichay
    title: "[feature] INIT-PRAYOG-001 — auth login + JWT session"
    depends_on: []
    codebase: prayog-parichay
    spec_path: docs/specification/product/INIT-PRAYOG-001.md
    verify_command: poetry run python -m tests.verify.verify_login
    branch_hint: feature/INIT-PRAYOG-001-parichay-login
    labels:
      - spec
    body: |
      ## Objective
      ...
```

### Optional keys

| Key | Purpose |
|-----|---------|
| `depends_on` | List of manifest ids (`P1`, `A1`, …) — linked in issue body by seed-work |
| `issue_type` | Override GitHub type (default: Task; epic → Epic) |
| `status` | Project Status single-select (must match board columns) |
| `cr`, `as_built`, `qa_manifest` | Project custom fields |

## What seed-work does

1. Merges `defaults` into epic + each work item (labels union).
2. Creates epic issue in `epic.repo`, then each work item in `item.repo`.
3. Sets GitHub issue type from project config roles (`epic` → Epic, else Task).
4. Adds issues to Project; sets custom fields from `_FIELD_MAP`.
5. Links children as sub-issues of epic via GitHub sub-issues API.
6. Appends `## Linked dependencies` to body when `depends_on` is set.
7. Appends `_Initiative: <id>_` footer if not already in body.

## Apply command

```bash
./scripts/prayog seed-work --config work/INIT-PRAYOG-001.yaml --dry-run
./scripts/prayog seed-work --config work/INIT-PRAYOG-001.yaml --apply
```
