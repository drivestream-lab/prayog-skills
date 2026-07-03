---
name: generate-work-manifest
description: "Drafts a WorkManifest YAML from a signed-off PRD and per-repo spec slices. Reads PRD delivery_model: waves → one Epic + one task per wave (W0…Wn, PRE*); repo-slice → one task per repo. Produces work/INIT-<id>.yaml — compatible with seed-work --dry-run|--apply. Does not create GitHub issues. Use after Phase 2 merges, before seed-work."
---

# Generate Work Manifest — PRD → seed-work YAML

## NON-NEGOTIABLE (read first)

1. **Draft only — never run `seed-work --apply`.** This skill writes YAML; the PM runs `seed-work` after PR review.
2. **Schema lock:** Output must be `apiVersion: prayog.meta/v1`, `kind: WorkManifest`, matching [references/work-manifest-schema.md](references/work-manifest-schema.md).
3. **Merged truth only:** Cite paths on **`develop`** (post handoff Phase 2). Do not reference draft PR branches.
4. **Granularity from PRD:** Read §4.0 `delivery_model`. **`waves`** → one task per wave ([references/wave-granularity.md](references/wave-granularity.md)). **`repo-slice`** → one task per repo ([references/v1-granularity.md](references/v1-granularity.md)). If §4.5 wave table exists without §4.0, infer `waves`.
5. **Dual output:** Chat summary (epic + task table) **and** saved manifest file under `prayog-meta/work/`.
6. **Depends_on = merge order:** Task dependencies must reflect PRD Appendix A / handoff merge order — not runtime verify order.
7. **Field completeness:** Every work item needs `repo`, `title`, `codebase`, `spec_path`, `verify_command`, `branch_hint`, and `body` (see [references/field-rules.md](references/field-rules.md)).

## Purpose

Turns signed-off initiative intent into a **WorkManifest** that `seed_work.py` consumes: epic on the Project, child tasks per repo, project custom fields (Initiative, Codebase, Spec path, Verify command, …), and `depends_on` links for implementation merge order.

Replaces ad-hoc issue drafting and OSS classifiers for **new** backlog creation. Use **`seed-work`** to apply the manifest to GitHub.

## Critical Rules

1. **Read before write.** Phase 1 must read the full PRD, `docs/cross-service-lab.md`, and each repo's handoff bundle before drafting items.
2. **PRD §10 is the repo map.** §11 supplies verify commands; Appendix A supplies `depends_on`. §2 FRs inform task bodies — do not duplicate the PRD in YAML bodies; summarize deliverables + acceptance pointers.
3. **Epic lives in prayog-meta.** Child tasks live in their **implementation repos** (same pattern as `BOOTSTRAP-PRAYOG-000.yaml`).
4. **Title convention:** `[feature] INIT-<id> — <repo-slice summary>` for tasks; `[feature] INIT-<id> — <initiative title>` for epic.
5. **Branch hints:** `feature/INIT-<id>-<kebab-slug>` per [branching-policy](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/branching-policy.md).
6. **Labels:** Default `initiative` on epic; per-item labels may add `spec`, `verify` — merge with manifest `defaults.labels`.
7. **Compose task:** `verify_command` is `N/A — manual demo + per-repo verify` when PRD §11 has no automated command for compose.
8. **Meta task (optional):** v1 does **not** add a prayog-meta implementation task unless the user asks; epic body covers §11 manual demo checklist.
9. **Do not invent scope.** If the PRD omits a repo or verify command, flag a gap in the chat summary — do not guess.
10. **Self-check before save.** Run the Phase 4 checklist; if any item fails, fix the YAML before publishing.

## When to Use

- After [pm-dev-handoff](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/pm-dev-handoff.md) **Phase 2** — meta PRD + all spec handoff PRs merged to `develop`
- After spec conformance gate is clean ([skills-matrix § Spec conformance](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/skills-matrix.md#spec-conformance-gate-per-repo--after-prd-sign-off))
- Before `./scripts/prayog seed-work --config work/INIT-*.yaml --dry-run`

**Do not use** during Phase 1 (open handoff PRs) — paths and verify commands may still change.

## Inputs

Gather before starting (all on **`develop`** unless noted):

| Input | Required | Used for |
|-------|----------|----------|
| **Initiative id** | Yes | `INIT-PRAYOG-001` → filename + fields |
| **PRD** | Yes | `prayog-meta/prd/INIT-*.md` — §10, §11, Appendix A, scope |
| **Cross-service lab map** | Yes | `prayog-meta/docs/cross-service-lab.md` |
| **Per-repo spec bundles** | Yes | Each app repo: `INIT-*.md` + `02-*` + `03-integrations` |
| **Compose seed doc** | If in §10 | `prayog-compose/docs/INIT-*-seed.md` |
| **Schema template** | Yes | `prayog-meta/bootstrap/BOOTSTRAP-PRAYOG-000.yaml` (structure only) |
| **Project config** | Reference | `prayog-meta/scripts/config/project-drivestream-lab.yaml` — Codebase options |
| **delivery_model** | From PRD §4.0 | `waves` \| `repo-slice`; see [wave-granularity.md](references/wave-granularity.md) |
| **delivery-model playbook** | autrio10x | `drivestream-meta/playbook/delivery-model.md` when present |

**Workspace:** `prayog-meta` (read sibling repos via multi-root workspace or absolute paths).

---

## Mandatory Todo / Checklist Control Loop

Create and maintain this checklist. Exactly one item `in_progress` at a time.

1. **T0 Gather** — Inventory inputs; note missing files
2. **T1 Understand** — Confirm initiative id, `delivery_model` (waves vs repo-slice), output path
3. **T2 Analyze** — Extract §4.0 delivery model + §4.5 wave table (waves) OR §10 repo map (repo-slice)
4. **T3 Plan** — Draft epic + task ids, `depends_on` graph, branch hints
5. **T4 Execute** — Write YAML; populate bodies with deliverables + PRD pointers
6. **T5 Verify** — Schema/field checklist; save file; publish chat summary

Never publish until **T5 Verify** is `completed`.

---

## Execution Workflow

### Phase 1: Read sources

1. Read the PRD end-to-end (minimum: §1 summary, §2 scope, §10, §11, Appendix A).
2. Read `docs/cross-service-lab.md`.
3. For each repo in §10 Technical Delivery Map, read the companion spec files listed in the PRD companion table.
4. Read `bootstrap/BOOTSTRAP-PRAYOG-000.yaml` for structural patterns (not content).
5. Read [references/work-manifest-schema.md](references/work-manifest-schema.md) and [references/field-rules.md](references/field-rules.md).

**Mark gaps:** missing spec file on `develop`, absent verify command, or unclear merge dependency → list in chat before drafting.

### Phase 2: Plan work breakdown

**If `delivery_model: waves`** — read [references/wave-granularity.md](references/wave-granularity.md):

1. Parse PRD §4.0 `board_units` and §4.5 wave table.
2. Read merged repo spec wave table — add **PRE*** gates if spec defines them.
3. Build linear `depends_on`: W0 → PRE* → W1 → … → Wn.
4. One `work[]` item per wave id; `id` field = wave id (`W0`, not `A1`).

**If `delivery_model: repo-slice`** — read [references/v1-granularity.md](references/v1-granularity.md):

**Repo-slice default (multi-repo product INIT):**

| id | repo | depends_on | Notes |
|----|------|------------|-------|
| `EPIC` | prayog-meta | — | Parent; initiative container |
| `C1` | prayog-compose | — | Parallel with parichay (no hard merge dep) |
| `P1` | prayog-parichay | — | First app merge |
| `A1` | prayog-abhilekh | `[P1]` | JWT contract from parichay |
| `O1` | prayog-ops | `[A1]` | BFF depends on abhilekh API |

Adjust ids/titles for the initiative; keep **one task per repo** in repo-slice mode only.

### Phase 3: Draft YAML

Output path: `prayog-meta/work/<INITIATIVE>.yaml` (e.g. `work/INIT-PRAYOG-001.yaml`).

**Top-level blocks (all required):**

```yaml
apiVersion: prayog.meta/v1
kind: WorkManifest
initiative: INIT-...
metadata:
  title: ...
  summary: |
    ...
  playbook:
    - playbook/chapters/chapter-08-sprint-001.md
    - playbook/pm-dev-handoff.md
target:
  org: drivestream-lab
  project: Prayog Pilot
defaults:
  initiative: INIT-...
  parent: EPIC
  cr: N/A
  as_built: N/A
  qa_manifest: N/A
  status: Backlog
  labels:
    - initiative
epic:
  id: EPIC
  ...
work:
  - id: C1
    ...
```

**Task body template** (each `work:` item):

```markdown
## Objective

<One paragraph — repo slice from §10>

## Deliverables

- [ ] <Concrete outcomes from repo INIT-*.md + 02-*>
- [ ] Verify: `<command from §11>`
- [ ] Update `as-built/implementation-status.md` in implementation PR

## Spec (develop)

- `docs/specification/product/INIT-....md`
- `<02-api-contract.md | 02-route-map.md>`
- `03-integrations.md`

## PR

`<branch_hint>` → `develop`

## PRD traceability

- FR-… / AC-… (list relevant ids)
```

Epic body: initiative objective, repo table from §10, §11 demo checklist reference, merge order, exit criteria checkboxes.

### Phase 4: Self-check (before save)

| Check | Pass if |
|-------|---------|
| Schema | `apiVersion`, `kind`, `initiative`, `target.org`, `target.project` present |
| Epic | `epic.id` = `EPIC`; `defaults.parent` = `EPIC` |
| Tasks | **waves:** every PRD/spec wave id has exactly one task; **repo-slice:** every §10 repo has one task |
| Fields | Each item has `codebase`, `spec_path`, `verify_command`, `branch_hint` |
| Codebase | Values ∈ project config Codebase options |
| Depends | `A1` → `P1`, `O1` → `A1`; compose independent |
| Paths | All `spec_path` values exist on `develop` |
| Labels | Epic includes `initiative` |
| Footer | Do not duplicate `seed_work.py` initiative footer — script adds it |

Fix failures before saving.

### Phase 5: Output

1. **Save** `prayog-meta/work/<INITIATIVE>.yaml`.
2. **Chat summary** (required sections):

**Manifest summary**

| id | repo | title | depends_on | verify_command |
|----|------|-------|------------|----------------|
| … | … | … | … | … |

**Gaps / assumptions** (if any)

**Next steps (PM)**

```bash
cd prayog-meta
./scripts/prayog seed-work --config work/<INITIATIVE>.yaml --dry-run
# After PR merge:
./scripts/prayog seed-work --config work/<INITIATIVE>.yaml --apply
```

Project → Table → **Show hierarchy** after apply.

---

## Worked examples (illustrative — not conventions to copy commands from)

`verify_command` and `spec_path` always come from that repo's own PRD/spec/harness profile on `develop` (Phase 1) — never invent or reuse a command from another initiative. The two examples below exist only to show what populated fields look like under the two `delivery_model` modes and on two different stacks; the manifest schema, field rules, and `depends_on` rules are identical regardless of stack.

### Example 1 — INIT-PRAYOG-001 (repo-slice mode, Python + Node stack)

When initiative is `INIT-PRAYOG-001`, use these merged paths and verify commands unless `develop` differs:

| Repo | spec_path (primary) | verify_command |
|------|---------------------|----------------|
| prayog-compose | `docs/INIT-PRAYOG-001-seed.md` | `N/A — manual demo + per-repo verify` |
| prayog-parichay | `docs/specification/product/INIT-PRAYOG-001.md` | `poetry run python -m tests.verify.verify_login` |
| prayog-abhilekh | `docs/specification/product/INIT-PRAYOG-001.md` | `poetry run python -m tests.verify.verify_assets` |
| prayog-ops | `docs/specification/product/INIT-PRAYOG-001.md` | `npm run verify:assets` |

Merge order: `parichay → abhilekh → ops`; compose parallel with parichay.

### Example 2 — illustrative wave-mode initiative on a non-Python/Node stack

**Fictional example** — `prayog-ledger` does not exist; this only demonstrates that wave mode and the manifest schema are stack-agnostic. When `delivery_model: waves` and the primary repo is a Go or JVM service, only `verify_command` and `spec_path` change — everything else (id = wave id, `depends_on` chain, field rules) is identical to a Python/Node repo:

| id | repo | title prefix | verify_command | depends_on |
|----|------|--------------|-----------------|------------|
| W0 | prayog-ledger (Go) | `[W0]` structure | `make check` | [] |
| PRE1 | prayog-ledger (Go) | `[PRE1]` unit test matrix | `go test ./... -run TestMatrix` | [W0] |
| W1 | prayog-ledger (Go) | `[W1]` ledger domain | `go test ./...` | [PRE1] |
| W2 | prayog-ledger (Go) | `[W2]` reconciliation API | `go test ./... && golangci-lint run` | [W1] |

For a JVM stack, the same rows would use `verify_command: ./gradlew check` (Gradle) or `mvn -q verify` (Maven) instead. `spec_path` still follows the standard convention (`docs/specification/product/INIT-*.md`) — only the verify tooling differs.

---

## Integration

| Step | Skill / tool | Notes |
|------|--------------|-------|
| PRD sign-off | `validate-requirements`, `review-findings`, `update-documents` | Before handoff |
| Spec conformance | `validate-requirements` per repo | Before this skill |
| **This skill** | `generate-work-manifest` | Writes `work/*.yaml` |
| Apply backlog | `./scripts/prayog seed-work` | PM only; `--dry-run` first |
| Implement | `pre-implement`, `verify`, SDD kit | Per task / repo |

See [skills-matrix.md](https://github.com/drivestream-lab/prayog-meta/blob/develop/playbook/skills-matrix.md).

---

## Related references (read in skill folder)

- [references/work-manifest-schema.md](references/work-manifest-schema.md) — YAML shape + example excerpts
- [references/field-rules.md](references/field-rules.md) — Project field mapping + defaults
- [references/wave-granularity.md](references/wave-granularity.md) — Epic + per-wave task rules
- [references/v1-granularity.md](references/v1-granularity.md) — Epic + per-repo task rules
