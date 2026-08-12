# prayog-skills

**Cursor Agent skills for specification-driven development** — procedural workflows for PM and engineering lanes in a [Launchpad](https://github.com/drivestream-lab/launchpad) harness.

Skills answer **what steps an agent runs** (validate PRD, draft spec, pre-implement gate, live verify). They complement **rules** repos (`.mdc` coding constitution at `.cursor/rules/`) and **launchpad** (factory CLI + playbook).

Portable delivery semantics live in [`workflow.yaml`](workflow.yaml) under the
contract in [`delivery-contract.yaml`](delivery-contract.yaml). Every skill
persists a standard handoff so Cursor, Claude Code, Codex, or a Launchpad-seeded
agent can resolve the next stage without platform-specific skill calls.

**SSOT:** `workflow.yaml` owns node `type`, skill `dispatch` (`manual` |
`orchestrated`), human-checkpoint `purpose`, and **`forge`** mutation policy
(`commit_workspace` on skills; `action` / labels / `requires` on
`external-action`). Skills are procedures — they do not fork navigation or
eligibility. Human `/skill` and AgentRunner share the same legality rules
(`invocation-mode-is-not-an-exemption`). Orchestrators auto-dispatch only when
`dispatch: orchestrated`; do not hardcode skill-id lists. Human stops use
`type: human-checkpoint` (not `type: gate`). Publish uses ForgeClient
(orchestrator) or `skills/forge/` (human) from pin ⋉ `handoff.forge` — see
[`references/forge-side-effects.md`](references/forge-side-effects.md).

**IDs & artifacts:** [`references/id-conventions.md`](references/id-conventions.md)
(product / process / delivery ids) ·
[`references/artifact-write-contract.md`](references/artifact-write-contract.md)
(canonical report paths — no `*-revN` siblings).

**Prompt packages:** every skill under `skills/requirements/`,
`skills/development/`, and `skills/forge/` ships `prompts/` (versioned
invocation brief). Coverage is independent of `dispatch`. See
[`references/prompt-package-contract.md`](references/prompt-package-contract.md).

**Human forge skills:** `commit-workspace`, `open-draft-pr`,
`create-board-tickets` — Gateflow ForgeClient parity for the human walker;
not workflow graph nodes.

| | |
|---|---|
| **License** | [MIT](LICENSE) |
| **Version** | see [`VERSION`](VERSION) — **0.5.1** |
| **Install** | [skills CLI](https://skills.sh) or Launchpad `apply-harness` |
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
| **purge-initiative-artifacts-meta** | After initiative-closure: delete meta PURGE allowlist (Validation/Resolution) |

### Development (app repos — harness seeded)

| Skill | When |
|-------|------|
| **spec-draft** | Dev translates PRD → spec slice (observable REQs; WHAT not HOW) |
| **initiative-feasibility** | Read-only buildability triage; lane→outcome routing |
| **spec-technical-review** | PE options + ADRs bound to approved REQs (T12) |
| **spec-implementation-plan** | Wave plan + WorkManifest seed on spec branch |
| **pre-implement** | Gate-only preflight before each wave (no branch/code) |
| **loop-spec** | Implement → check/unit → fix; Wave-Execution + stage Forge readiness |
| **ground-spec** | Wave-assigned REQ grounding (`GF-*`, G1–G10); sign-off package |
| **learning-extract** | After wave-acceptance: structured L-* learning (closeout) |
| **purge-initiative-artifacts-app** | After initiative-closure: delete app PURGE allowlist (working papers) |

### Forge (human — meta + app)

| Skill | When |
|-------|------|
| **commit-workspace** | Commit staged workspace changes (ForgeClient parity) |
| **open-draft-pr** | Open draft PR with pin labels (ForgeClient parity) |
| **create-board-tickets** | After spec merge: preflight + authorize + seed EPIC/waves from plan §9 |

Profile manifests (`profiles/*.yaml`) list which skills apply per **stack key**
(`python-backend`, `nextjs-frontend`, `terraform-iac`, `flink`, `edge-agent`,
`meta-pm`). Filename = YAML `profile:` = Launchpad harness profile (no aliases).
**Launchpad** reads these at sync time — when adding or removing a skill, update
every relevant `profiles/*.yaml` and bump the harness `skills[].ref`.

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
/spec-draft  →  /initiative-feasibility  →  /spec-technical-review
    ↓
/spec-implementation-plan  (§9 WorkManifest YAML on spec branch; after PE approval)
    ↓
PE sets spec-lgtm on exact head → Ready for review → Approve → merge
    ↓
Merge spec PR → develop → **`/create-board-tickets`** (governance board + EPIC/wave tree)
    ↓
Per wave Pass-1:  /pre-implement → /loop-spec → wave-pr-action → wave-acceptance (human runs co-shipped script; label wave-accepted)
Pass-2 closeout:  /learning-extract  →  /ground-spec  →  wave-signoff (human merge only; record merge SHA)
    ↓
All waves done (eng then PM):
  initiative-closure → /purge-initiative-artifacts-app → app Draft PR → merge
  → /purge-initiative-artifacts-meta → meta Draft PR → merge → complete
```

New/material product surfaces **co-ship** a live script under `live_verify_dir`
in the same wave (plan P15). Agent bar is check+unit; human executes the script
at `wave-acceptance` (only approval signal). There is **no** `/verify` content
skill. Content skills never apply labels / commit / merge (Forge boundary).
`wave-signoff` is merge/publish only.
Full process: [launchpad delivery workflow](https://github.com/drivestream-lab/launchpad/blob/main/playbook/delivery-workflow.md).

Artifacts are the source of truth. GitHub labels are status projections only.
PE moves prd-impact-acceptance through `impact-map-pending`, `impact-map-blocked`, and
`impact-map-lgtm`; coding-readiness through `spec-pending`, `spec-blocked`, and
`spec-lgtm`. Revised or stale labels close the gate. Never infer approval from
labels alone — require matching GitHub Approve and artifact digests on the exact
PR head.

---

## Installation

### With Launchpad (recommended)

```bash
# PM meta workspace
launchpad apply-harness --meta --apply
launchpad status --meta

# App repo
launchpad apply-harness --repo <service> --apply
launchpad status --repo <service>
```

(`--dry-run` is default; pass `--apply` to execute.)

Skill hubs under `.harness/skills/` / `.agents/skills/` are local (often gitignored); re-run `apply-harness` after clone. Pin / submodule gitlinks are committed; `status` checks readiness. See [Launchpad factory CLI](https://github.com/drivestream-lab/launchpad/blob/develop/docs/onboarding/factory-cli.md) and [`docs/for-launchpad.md`](docs/for-launchpad.md).

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
  --skill learning-extract \
  --skill ground-spec \
  -a cursor -y
```

---

## Layout

```text
prayog-skills/
  VERSION
  profiles/           # SSOT skill lists per stack_key (identity equality)
    python-backend.yaml
    nextjs-frontend.yaml
    terraform-iac.yaml
    flink.yaml
    edge-agent.yaml
    meta-pm.yaml
  references/         # normative: handoff, forge, ids, artifacts, prompts
  docs/               # human orientation (overview, for-launchpad/gateflow)
  skills/
    requirements/     # PM lane (+ prompts/ per skill)
    development/      # Dev lane (+ prompts/ per skill)
    forge/            # Human forge skills (+ prompts/)
    engg-reviews/     # Experimental PE adjunct (not in profiles; no prompts/)
  scripts/            # Consistency + prompt contract checks (CI)
  tests/fixtures/     # dispatch / forge / prompt inventory SSOTs
```

**Docs:** start at [`docs/README.md`](docs/README.md) — orientation only; contracts stay in `references/` and the pin YAMLs.

Each skill: `skills/<category>/<name>/SKILL.md` per [Agent Skills](https://cursor.com/docs/skills).

Requirements and development skills also include:

```text
skills/<area>/<skill-id>/prompts/
  template.md                 # simple {{var}} invocation brief
  schema.yaml                 # prompt_id + semver revision + variables
  fixtures/happy_path.*       # golden render inputs + expected output
```

---

## Experimental — engg-reviews (Phase 1 MVP)

Gate-independent PE advisory pack, adjunct to the mainline release.
**Not** part of `sdd-delivery/v2`. **Not** listed in `profiles/*.yaml` — does not
unlock `prd-impact-acceptance` or `/spec-draft`. PE posts product questions on the Meta PR; PM
updates the PRD via requirements skills.

| Skill | When |
|-------|------|
| **ensure-repo-graph** | Refresh local Graphify graphs for candidate app repos `@ develop` |
| **prd-codebase-map** | Map meta PRD → as-built + codegraph; emit product questions |
| **review-product-questions** | Optional interactive PE stance refine before posting |
| **post-product-questions** | PE posts questions + recommendations on Meta PR; request PM feedback |

Details: [`skills/engg-reviews/README.md`](skills/engg-reviews/README.md) ·
Plan: [`skills/engg-reviews/implementation-plan.md`](skills/engg-reviews/implementation-plan.md).
Partner orientation: [`docs/`](docs/README.md).

**PE install (tag `pe-rc-2`):**

```bash
curl -fsSL https://raw.githubusercontent.com/drivestream-lab/prayog-skills/pe-rc-2/scripts/install_engg_reviews.py \
  -o /tmp/install_engg_reviews.py
python3 /tmp/install_engg_reviews.py --target /path/to/pe-workspace --ref pe-rc-2
```

---

## Release process (maintainers)

1. Change skills on a branch; run `scripts/check_consistency.py`
2. Bump `VERSION` and tag (`v0.4.0`)
3. PR → `develop` → `main`
4. Update tenant `config/harness-<org>.yaml` approved pairs (`agent_skills.ref`)
5. Consumers run `apply-harness --meta` / `apply-harness --repo …` (then `status` as needed) or bump pin manually

---

## Provenance

| Skill area | Origin |
|------------|--------|
| validate-requirements, review-findings, update-documents | Vendored from rushikeshpol02/ai-skills |
| pre-implement | Adapted from early platform skills work |
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
