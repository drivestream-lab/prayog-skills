# prayog-skills

Lab-owned **Cursor Agent skills** for spec-driven development workflows. Install via [skills CLI](https://skills.sh) or **launchpad harness** (`sync-harness`) in app repos.

**Version:** see [`VERSION`](VERSION) (currently **0.2.1**)

## Skill bundles

### Requirements & backlog (PM workspace)

| Skill | Path |
|-------|------|
| **validate-requirements** | `skills/requirements/validate-requirements/` |
| **review-findings** | `skills/requirements/review-findings/` |
| **update-documents** | `skills/requirements/update-documents/` |
| **generate-work-manifest** | `skills/backlog/generate-work-manifest/` |

### Development (app repos — harness seed)

| Skill | Path |
|-------|------|
| **spec-feasibility-review** | `skills/development/spec-feasibility-review/` |
| **spec-implementation-plan** | `skills/development/spec-implementation-plan/` |
| **pre-implement** | `skills/development/pre-implement/` |
| **verify** | `skills/development/verify/` |

**Harness profiles:** [`profiles/`](profiles/) — `launchpad sync-harness` copies `profiles/{profile}.yaml` → `.harness/profile.yaml` in the consumer repo (`python-backend`, `frontend`, …).

## Install (PM — drivestream-meta)

```bash
npx skills add github/awesome-copilot --skill prd -a cursor -y
npx skills add drivestream-lab/prayog-skills --skill '*' -a cursor -y
```

## Install (dev — app repo)

Harness (recommended):

```bash
launchpad sync-harness --repo <service> --apply
```

Manual dev bundle only:

```bash
npx skills add drivestream-lab/prayog-skills \
  --skill spec-feasibility-review \
  --skill spec-implementation-plan \
  --skill pre-implement \
  --skill verify \
  -a cursor -y
```

Commit **`skills-lock.json`** and **`.harness/profile.yaml`** after sync. Keep **`.agents/`** gitignored.

## Dev workflow

```text
spec PR  → /spec-feasibility-review
merged   → /spec-implementation-plan
slice    → /pre-implement → implement → /verify
```

## Provenance

- **validate-requirements**, **review-findings**, **update-documents** — vendored from rushikeshpol02/ai-skills
- **pre-implement**, **verify** — adapted from prayog-meta; formerly python-services-skills
- **spec-feasibility-review**, **spec-implementation-plan** — patterns from awesome-copilot (unmet-spec loop, implementation-plan tables)

## Adding skills

`skills/<category>/<skill-name>/SKILL.md` per [Agent Skills](https://cursor.com/docs/skills). Tag releases (`v0.2.1`) and bump harness `agent_skills.ref` in launchpad / drivestream-meta.
