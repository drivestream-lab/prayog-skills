# prayog-skills

**Cursor Agent skills for specification-driven development** — procedural workflows for PM and engineering lanes in a [Launchpad](https://github.com/drivestream-lab/launchpad) harness.

Skills answer **what steps an agent runs** (validate PRD, draft spec, pre-implement gate, live verify). They complement **rules** repos (`.mdc` coding constitution at `.cursor/rules/`) and **launchpad** (factory CLI + playbook).

Portable delivery semantics live in [`workflow.yaml`](workflow.yaml) under the
contract in [`delivery-contract.yaml`](delivery-contract.yaml). Every skill
persists a standard handoff so Cursor, Claude Code, Codex, or a Launchpad-seeded
agent can resolve the next stage without platform-specific skill calls.

| | |
|---|---|
| **License** | [MIT](LICENSE) |
| **Version** | see [`VERSION`](VERSION) (currently **0.4.3-rc.2**) |
| **Install** | [skills CLI](https://skills.sh) or `launchpad sync-harness-*` |
| **Pairs with** | [launchpad](https://github.com/drivestream-lab/launchpad) · `*-rules` repos |

---

## Two lanes — do not mix

| Lane | Workspace | Skills | Rules submodule |
|------|-----------|--------|-----------------|
| **PM** | `<client>-meta` | Requirements pipeline below | None |
| **Dev** | App repos | Development pipeline below | `python-services-rules`, `nextjs-bff-rules`, or `data-platform-rules` |

PM skills validate and refine PRDs. Dev skills implement spec slices in service repos. Collapsing lanes causes agents to run against the wrong tree.

---

## Skill catalog

### Requirements (PM — `<client>-meta`)

| Skill | When |
|-------|------|
| **prd** (community) | Writing a new initiative PRD |
| **validate-requirements** | Auditing PRD completeness |
| **review-findings** | PM decides on findings |
| **update-documents** | PM refines PRD after findings |
| **prd-impact-map** | Generates a versioned PRD → repo map and Draft-PR readiness handoff |

### Development (app repos — harness seeded)

| Skill | When |
|-------|------|
| **spec-draft** | Dev translates PRD → spec slice for this repo |
| **initiative-feasibility** | Dev reviews spec for buildability |
| **spec-technical-review** | PE resolves engineering decisions + drafts ADRs |
| **spec-implementation-plan** | Wave plan + §9 WorkManifest YAML on spec branch |
| **board-seed** | EPIC + wave tree on programme board after spec merge (all app stacks) |
| **pre-implement** | Pre-flight before each implementation wave |
| **loop-spec** | Implement → verify → fix per task |
| **ground-spec** | Wave complete — FR validation + contracts for next wave |
| **verify** | Live CLI/API verification |

Profile manifests (`profiles/*.yaml`) list which dev skills apply per harness profile (`python-backend`, `frontend`, `data-platform`, `meta-pm`). **Launchpad** reads these at sync time — when adding or removing a dev skill, update every relevant `profiles/*.yaml` and bump the harness `agent_skills.ref`.

---

## Dev workflow (high level)

```text
PM: validated PRD → generate Impact-Map-{INIT}.md locally
    → review PR-readiness handoff → user authorizes Draft PR creation
    → agent uses gh when configured; initializes impact-map-pending
    → product clarification on PR; PE sets impact-map-lgtm
    → tech-lead Approve on exact meta PR head SHA
    → merge PRD PR to develop
    ↓
Eng: Draft spec PR (entire spec lifecycle) for approved repo scope
    → spec-pending; Q&A on Draft PR
    ↓
/spec-draft  →  /initiative-feasibility  →  [/spec-technical-review]
    ↓
/spec-implementation-plan  (§9 WorkManifest YAML on spec branch)
    ↓
PE sets spec-lgtm on exact head → Ready for review → Approve → merge
    ↓
Merge spec PR → develop → **`/board-seed`** (governance board + EPIC/wave tree)
    ↓
Per wave:  /pre-implement  →  /loop-spec  →  /ground-spec  →  human checkpoint
```

Full process: [launchpad delivery workflow](https://github.com/drivestream-lab/launchpad/blob/main/playbook/delivery-workflow.md).

Artifacts are the source of truth. GitHub labels are status projections only.
PE moves Gate 1 through `impact-map-pending`, `impact-map-blocked`, and
`impact-map-lgtm`; Gate 2 through `spec-pending`, `spec-blocked`, and
`spec-lgtm`. Revised or stale labels close the gate. Never infer approval from
labels alone — require matching GitHub Approve and artifact digests on the exact
PR head.

---

## Installation

### With Launchpad (recommended)

**PM meta workspace:**

```bash
launchpad sync-harness-meta --apply
launchpad verify-harness-meta
```

**App repo:**

```bash
launchpad sync-harness-app --repo <service> --apply
launchpad verify-harness-app --repo <service>
```

Harness writes `.harness-pin.yaml`, seeds `.agents/skills/`, and optionally commits `skills-lock.json`. Keep **`.agents/`** gitignored in consumers.

### Manual — PM workspace

```bash
npx skills add github/awesome-copilot --skill prd -a cursor -y
npx skills add drivestream-lab/prayog-skills --skill '*' -a cursor -y
```

### Manual — dev bundle (python-backend example)

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

---

## Layout

```text
prayog-skills/
  VERSION
  profiles/           # SSOT skill lists per harness profile
    python-backend.yaml
    frontend.yaml
    meta-pm.yaml
  skills/
    requirements/     # PM lane
    development/      # Dev lane
  scripts/            # Consistency checks (CI)
```

Each skill: `skills/<category>/<name>/SKILL.md` per [Agent Skills](https://cursor.com/docs/skills).

---

## Release process (maintainers)

1. Change skills on a branch; run `scripts/check_consistency.py`
2. Bump `VERSION` and tag (`v0.4.0`)
3. PR → `develop` → `main`
4. Update tenant `config/harness-<org>.yaml` approved pairs (`agent_skills.ref`)
5. Consumers run `sync-harness-meta` / `sync-harness-app` or bump pin manually

---

## Provenance

| Skill area | Origin |
|------------|--------|
| validate-requirements, review-findings, update-documents | Vendored from rushikeshpol02/ai-skills |
| pre-implement, verify | Adapted from early platform skills work |
| initiative-feasibility, spec-implementation-plan | Patterns from awesome-copilot |
| spec-technical-review, loop-spec, ground-spec, spec-draft | Platform SDD design (RFC-style review, spec kit patterns) |

---

## Related repositories

| Repo | Role |
|------|------|
| [launchpad](https://github.com/drivestream-lab/launchpad) | Sync/verify harness; playbook SSOT |
| [python-services-rules](https://github.com/drivestream-lab/python-services-rules) | Python coding constitution |
| [nextjs-bff-rules](https://github.com/drivestream-lab/nextjs-bff-rules) | Frontend BFF constitution |
| [data-platform-rules](https://github.com/drivestream-lab/data-platform-rules) | Flink/Java constitution |

---

## License

MIT — see [LICENSE](LICENSE).
