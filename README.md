# prayog-skills

Lab-owned **Cursor Agent skills** for spec-driven development workflows. Install via [skills CLI](https://skills.sh) or **launchpad harness** (`sync-harness`) in app repos.

**Version:** see [`VERSION`](VERSION) (currently **0.3.1**)

## Role → skill mapping

**PM owns (meta workspace):** writes PRD, maps to repos, opens prd-handoff PRs.  
**Dev/Engineering owns (app repo):** writes spec, reviews feasibility, plans, builds.

### Requirements (PM workspace — `<client>-meta`)

| Skill | When | Path |
|-------|------|------|
| **prd** (community) | Writing a new initiative PRD | community/awesome-copilot |
| **validate-requirements** | Auditing PRD completeness | `skills/requirements/validate-requirements/` |
| **review-findings** | PM decides on findings | `skills/requirements/review-findings/` |
| **update-documents** | PM refines PRD after findings | `skills/requirements/update-documents/` |
| **prd-impact-map** | Maps PRD to affected repos | `skills/requirements/prd-impact-map/` |

### Development (app repos — harness seeded by launchpad)

| Skill | When | Path |
|-------|------|------|
| **spec-draft** | Dev translates PRD → spec slice for this repo | `skills/development/spec-draft/` |
| **initiative-feasibility** | Dev reviews spec slice for buildability | `skills/development/initiative-feasibility/` |
| **spec-technical-review** | PE resolves engineering decisions + drafts ADRs | `skills/development/spec-technical-review/` |
| **spec-implementation-plan** | Dev produces wave plan + board-seed YAML (§9) | `skills/development/spec-implementation-plan/` |
| **pre-implement** | Pre-flight before each wave | `skills/development/pre-implement/` |
| **loop-spec** | Implementation loop (implement → verify → fix) | `skills/development/loop-spec/` |
| **ground-spec** | Validates wave FRs + produces §Contracts produced | `skills/development/ground-spec/` |
| **verify** | Live CLI/API verification | `skills/development/verify/` |

**`background_eligible` / `background_trigger`:** Development skills carry these keys as launchpad-side conventions marking which skills can be invoked unattended and on what trigger. Not a Cursor feature — launchpad reads them when wiring background automation.

## Dev workflow

```
prd-handoff PR opened
    ↓
/spec-draft          ← dev writes spec slice from PRD
    ↓
/initiative-feasibility  ← dev reviews spec for buildability; 4-lane triage
    ↓ (if PE/engineering blockers)
/spec-technical-review   ← PE resolves decisions, drafts ADRs
    ↓
/spec-implementation-plan ← wave plan + §9 board-seed YAML
gh issue create ← dev seeds board (one issue per wave W0, W1, …)
    ↓
per wave:
/pre-implement → /loop-spec → /ground-spec → human checkpoint
    ↓ (next wave reads prior /ground-spec §Contracts produced)
```

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

Manual dev bundle:

```bash
npx skills add drivestream-lab/prayog-skills \
  --skill spec-draft \
  --skill initiative-feasibility \
  --skill spec-technical-review \
  --skill spec-implementation-plan \
  --skill pre-implement \
  --skill loop-spec \
  --skill ground-spec \
  --skill verify \
  -a cursor -y
```

Commit **`skills-lock.json`** and **`.harness/profile.yaml`** after sync. Keep **`.agents/`** gitignored.

## Provenance

- **validate-requirements**, **review-findings**, **update-documents** — vendored from rushikeshpol02/ai-skills
- **pre-implement**, **verify** — adapted from prayog-meta; formerly python-services-skills
- **initiative-feasibility**, **spec-implementation-plan** — patterns from awesome-copilot (unmet-spec loop, implementation-plan tables)
- **spec-technical-review**, **loop-spec**, **ground-spec** — v0.3.0; benchmarked against Stripe/Cloudflare/Oxide RFC process, Sentry design-first gate, `agentic_development_workflow` multi-role review, GitHub Spec Kit `/speckit.plan`
- **spec-draft** — v0.3.0; dev-side PRD → spec translation (PM writes PRD, engineering owns spec)

## Adding skills

`skills/<category>/<skill-name>/SKILL.md` per [Agent Skills](https://cursor.com/docs/skills). Tag releases and bump harness `agent_skills.ref` in launchpad / drivestream-meta. **When adding or removing a development skill, also update `development_skills:` in every `profiles/*.yaml`** — `launchpad sync-harness` seeds consumer repos from that list.
