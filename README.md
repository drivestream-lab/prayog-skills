# prayog-skills

Lab-owned **Cursor Agent skills** for [drivestream-lab](https://github.com/drivestream-lab). Skills are installable via the [skills CLI](https://skills.sh) or committed under `.cursor/skills/` in consumer repos.

## Skills

| Skill | Path | Purpose |
|-------|------|---------|
| **validate-requirements** | `skills/requirements/validate-requirements/` | PRD / requirements validation (15 checks, incremental reports) |
| **review-findings** | `skills/requirements/review-findings/` | Interactive walkthrough of validation report findings → resolution summary |
| **update-documents** | `skills/requirements/update-documents/` | Apply resolution summary across PRD + integration stubs |
| **generate-work-manifest** | `skills/backlog/generate-work-manifest/` | PRD → `work/INIT-*.yaml` for `seed-work` (draft only) |

Backlog creation uses **generate-work-manifest** + **seed-work** — not issue classification of existing dumps.

## Install (project)

From a consumer repo (e.g. `prayog-meta`, `drivestream-meta`):

```bash
npx skills add drivestream-lab/prayog-skills --skill '*' -a cursor -y
npx skills add github/awesome-copilot --skill prd -a cursor -y
```

Verify:

```bash
npx skills list
```

Invoke in Cursor Agent: `/validate-requirements`, `/review-findings`, `/update-documents`, `/generate-work-manifest`

## Lab workflow

Documented in [prayog-meta/playbook/skills-matrix.md](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/skills-matrix.md) and [skills-audition.md](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/skills-audition.md).

## Provenance

**validate-requirements**, **review-findings**, and **update-documents** were vendored from `rushikeshpol02/ai-skills` (upstream unavailable). Maintained by drivestream-lab.

## Adding skills

Place new skills under `skills/<category>/<skill-name>/SKILL.md` matching [Agent Skills](https://cursor.com/docs/skills) layout. Open a PR in this repo; bump consumer install or submodule reference in `prayog-meta`.
