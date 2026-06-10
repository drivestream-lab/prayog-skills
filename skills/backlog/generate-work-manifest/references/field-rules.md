# WorkManifest field rules

## Project custom fields (seed-work mapping)

YAML key → GitHub Project field (from `seed_work.py` `_FIELD_MAP`):

| YAML key | Project field | Type | Required on every item |
|----------|---------------|------|------------------------|
| `initiative` | Initiative | TEXT | Yes (via defaults) |
| `cr` | CR | TEXT | Yes — use `N/A` for INIT features |
| `codebase` | Codebase | SINGLE_SELECT | Yes — must match project config option |
| `spec_path` | Spec path | TEXT | Yes |
| `verify_command` | Verify command | TEXT | Yes — use `N/A` only when PRD has no command |
| `as_built` | As-built | SINGLE_SELECT | Yes — default `N/A` until implementation PR |
| `qa_manifest` | QA manifest | TEXT | Yes — default `N/A` for lab INIT |
| `status` | Status | SINGLE_SELECT | Default `Backlog` |

**Codebase options** (`project-drivestream-lab.yaml`):  
`prayog-meta`, `prayog-compose`, `prayog-parichay`, `prayog-abhilekh`, `prayog-ops`

## defaults block (recommended)

```yaml
defaults:
  initiative: INIT-PRAYOG-001
  parent: EPIC
  cr: N/A
  as_built: N/A
  qa_manifest: N/A
  status: Backlog
  labels:
    - initiative
```

Per-item labels merge with defaults (no duplicates).

## spec_path conventions

| Repo kind | Primary spec_path |
|-----------|-------------------|
| prayog-meta (epic) | `prd/INIT-*.md` |
| Python app | `docs/specification/product/INIT-*.md` |
| prayog-ops | `docs/specification/product/INIT-*.md` |
| prayog-compose | `docs/INIT-*-seed.md` |
| Chore / rules fork | `N/A — <description>` (bootstrap pattern) |

List companion files (`02-api-contract.md`, `02-route-map.md`, `03-integrations.md`) in the task **body**, not necessarily in `spec_path`.

## verify_command conventions

Copy **exactly** from PRD §11 when present:

| Repo | INIT-PRAYOG-001 |
|------|-----------------|
| prayog-parichay | `poetry run python -m tests.verify.verify_login` |
| prayog-abhilekh | `poetry run python -m tests.verify.verify_assets` |
| prayog-ops | `npm run verify:assets` |
| prayog-compose | `N/A — manual demo + per-repo verify` |
| prayog-meta (epic) | `N/A — §11 manual demo checklist` |

## branch_hint conventions

- Implementation: `feature/INIT-<AREA>-<NNN>-<kebab-slug>` (strict prod) or `feature/INIT-<id>-<slug>` (lab standard).
- One hint per task; matches the primary implementation PR for that repo slice.

## title conventions

| Kind | Pattern | Example |
|------|---------|---------|
| Epic | `[feature] <INIT> — <initiative name>` | `[feature] INIT-PRAYOG-001 — FrostMart MVP` |
| Task | `[feature] <INIT> — <slice>` | `[feature] INIT-PRAYOG-001 — parichay login + JWT` |

Use `[chore]` only for bootstrap manifests (e.g. BOOTSTRAP-PRAYOG-000).

## depends_on rules

- Use manifest **ids** (`P1`, `A1`), not repo names.
- Encode **merge order**, not docker startup order.
- Compose seed task typically has **no** `depends_on` (parallel with parichay).
- Empty dependency: omit key or `depends_on: []`.

## Labels

| Label | When |
|-------|------|
| `initiative` | Epic + defaults |
| `spec` | Spec-driven implementation task |
| `verify` | Optional — heavy verify slice |

Do not use `pilot` for INIT product work (bootstrap only).
