# Changelog

All notable changes to prayog-skills are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Added — `resolve-pr-review` (meta PM)

- New manual requirements skill closes Gate 1 PE/tech-lead comment loops in one
  pass: parse every finding, fix PRD (SSOT), sync satellite docs, re-validate,
  regenerate impact map from scratch (never patch inline), run digest/consistency
  gates, and prepare a reply comment (post only with user approval).
- Registered in `profiles/meta-pm.yaml`, prompt inventory, and skill catalog.

## [0.5.3] — 2026-08-22

### Added — Harness profiles for new lab stacks

- `profiles/edge-inference-engine.yaml`
- `profiles/android-kotlin.yaml` (Gradle `app/src/` source roots)
- `profiles/ios-swift.yaml` (Tuist `Sources/` source roots)

Same-wave with launchpad **v0.5.36** config-scalable stacks.

## [0.5.2] — 2026-08-13

### Fixed — WorkManifest `files[].path` is an exact literal

- `scripts/workmanifest_contract.py` no longer treats `[` / `]` as glob
  characters. Bracketed path segments are ordinary filename characters
  (consumed via direct path APIs, never glob-expanded). Glob wildcards `*`
  and `?` are still rejected, as are absolute paths, `~`, and `../`.
- Plan check P16 PASS requires `scripts/workmanifest_contract.py` to exit 0
  on §9 — a checklist tick without that run is not P16.

### Fixed — Meta service catalog is org-suffixed without tenant hardcoding

- `/prd-impact-map` (and sister readers) resolve **one** catalog under
  `<client>-meta/config/`: prefer `service-catalog-<org>.yaml` when org is
  known (unique `governance-<org>.yaml` suffix); otherwise exactly one of
  `service-catalog.yaml` or `service-catalog-*.yaml`. Fail closed on zero or
  multiple matches. Never hardcode a tenant org.
- Prompt package `prd-impact-map` bumped `1.3.0` → `1.4.0`.

## [0.5.1] — 2026-08-12

### Fixed — Pin-root `references/` path contract for remounted skills

- Skill packages no longer cite pin-root contracts via `../../../references/…`
  (pin-layout-only; breaks under Launchpad `.harness/skills/<skill>/` and other
  runtimes) or bare `references/<pin-file>.md` (ambiguous with skill-local
  `references/`).
- **SSOT stays** pin-tip `references/`. From skill packages (source or hub),
  cite `prayog-skills/references/<file>.md` (Launchpad mounts the pin at
  `prayog-skills/`). Skill-local helpers remain `references/<local-file>`.
- Documented in `docs/overview.md`, `docs/for-launchpad.md`,
  `docs/for-gateflow.md`. `scripts/check_consistency.py` fails closed on the
  old relative/bare forms and resolves remount-path markdown links to pin
  `references/` when checking inside this repo.
- Do **not** copy pin `references/` to consumer-repo root.
- Prompt package revisions bumped for packages whose templates/fixtures changed.

## [0.5.0] — 2026-08-11

Promoted to stable from the `0.5.0-rc.2` tip family (`features/rc-2`) after
dogfooding a full initiative end-to-end (feasibility → Accepted TDD/ADRs →
implementation plan → wave execution → ground reports → learning-extract) on
wave-acceptance semantics across three consuming repos. All changes below
previously shipped incrementally under `v0.5.0-rc.2` retags; this tag is the
same content, promoted rather than re-authored. Programmes pinned at
`v0.5.0-rc.2` should retarget `agent_skills.ref: v0.5.0`.

### Added — Live-verify coverage marker, as-built split, optional codegraph tool contract

- **Live-verify coverage lives at the source, not in a growing `tests/README.md`.**
  New `references/live-verify-coverage-contract.md`: a stack-agnostic, literal
  text marker (`prayog:covers: REQ-*`) self-declared inside any
  `live_verify_dir` artifact — code comment or markdown runbook alike —
  resolved via the plan's own `files[]` paths, never by parsing `command`.
  `spec-implementation-plan` P15 now requires an explicit overlap check
  (`scripts/verify_coverage_query.py`) before declaring a new FILE, with a
  third worked example showing the extend-not-duplicate path; P9 no longer
  accepts a `tests/README.md` edit as satisfying live-verify coverage.
  `scripts/workmanifest_contract.py` optionally cross-checks the manifest's
  `verification.live.covers` against the artifact's self-declared marker
  when a workspace root is supplied (`--base-path` / `base_path=`) — omitted
  by default, so every existing invocation is unaffected.
- **`implementation-status.md` splits by initiative — nothing deleted, growth
  bounded.** New per-initiative `KEEP` file
  `Implementation-Status-{INIT}.md` (written once, stops growing once that
  initiative's waves close); the shared `implementation-status.md` shrinks to
  one row per capability, overwritten in place, never appended — same
  "supersede, never rewrite" discipline this repo already uses for
  `Ground-Report-*-W{N}.md`, applied to a `KEEP` artifact. Both new file
  kinds get explicit `KEEP` classification in `artifact-write-contract.md`
  and an explicit refuse-list entry in `purge-initiative-artifacts-app` —
  closing a pre-existing gap where neither `implementation-status.md` nor
  `tests/README.md` was formally classified at all.
- **Optional codegraph tool contract**, promoted out of the `engg-reviews`
  adjunct pack to a shared `references/codegraph-tool-contract.md`: interface
  (`ensure_graph`/`query`/`path`/`explain`/`freshness`), freshness/edge-confidence
  discipline, and degraded-mode fallback — a `Tool`, never `Forge`, never a
  dependency for any packaged skill to function. Five mainline skills
  (`initiative-feasibility`, `spec-draft`, `spec-implementation-plan`,
  `ground-spec`, `pre-implement`) gain one optional NON-NEGOTIABLE bullet +
  Inputs row each: prefer the provider when available, always fall back,
  never block or change outcome selection on its absence.
  `references/forge-side-effects.md` formalizes the shared
  `signals.codegraph_provider` / `signals.grounding_depth` shape.
  `docs/for-gateflow.md` adds a partner-only note describing Gateflow's own
  `AdapterSlotKindType`/`SlotValidator` (ADR-003/006) as the natural
  integration point if Gateflow's team chooses to build this — explicitly
  not a prayog-skills deliverable, and explicitly warns against ever marking
  the adapter required in `SlotValidator`, which would turn an intentionally
  optional Tool into an accidental hard gate.
- New scripts: `scripts/verify_coverage_query.py` (read-only, stdout-only
  query over self-declared coverage — no "current listing" file to keep in
  sync, ever). New tests: `tests/test_verify_coverage_query.py`, coverage
  cases in `tests/test_workmanifest_contract.py`.
- Prompt packages: `spec-implementation-plan@1.7.0`, `initiative-feasibility@1.4.0`,
  `spec-draft@1.4.0`, `ground-spec@1.4.0`, `pre-implement@1.8.0` (MINOR —
  additive optional guidance); `purge-initiative-artifacts-app@1.1.1` (PATCH).

### Added — Required codebase grounding for ADR drafting (product-feature-leakage fix)

- **`spec-technical-review` must ground every `NEW-ADR` finding in the actual
  codebase before classifying or drafting it — not just trust feasibility's
  `ALTERNATIVE:` text.** New NON-NEGOTIABLE 11/12: verify and extend the
  finding's Code evidence via a codegraph query (when available, per
  `references/codegraph-tool-contract.md`) or a direct `source_roots` read
  otherwise — the tool is optional, the grounding activity is not. T2
  Analyze and T3 Design (`SKILL.md`) and checks T1/T3 (`references/checks.md`)
  now require this evidence explicitly, and the ADR qualification rubric
  gains a concrete test: criterion (3) ("a real trade-off exists") requires
  naming the actual system-behavior difference between options, grounded in
  code — a choice where every option produces identical runtime behavior is
  not `ADR_REQUIRED`. `references/adr-template.md`'s "Options considered"
  section now instructs dropping/annotating any option the grounding or the
  spec's own exclusions already foreclose, so a technically-dead option never
  reads as a live peer choice.
- **`initiative-feasibility`'s ADR traceability row (F13) gains a required
  Code evidence column** — the specific module/file path this stage's own
  F1/F2 baseline found relevant to the alternative, not blank when something
  was found. `spec-technical-review` re-verifies and extends this column
  rather than trusting it as-is, closing the gap where an `ALTERNATIVE:`
  finding could be drafted from prose alone with no code ever inspected a
  second time.
- **T12's independent re-read is now a genuinely separate pass, not a
  same-session self-grade.** `SKILL.md` T4 Execute and `references/checks.md`
  both now call for a fresh sub-task/subagent with no visibility into the
  drafting turns where the runtime supports spawning one, falling back to a
  deliberate context-reset (read the file cold, as someone else's
  submission) otherwise. The T12 check row's FAIL condition explicitly
  includes "the independent re-read flags product leakage the mechanical
  lint did not catch."
- Prompt packages: `spec-technical-review@1.4.0` (MINOR — new mandatory
  grounding step, no input/output schema change), `initiative-feasibility@1.4.1`
  (PATCH — template column addition).

### Changed — Digest simplification (walk-time ceremony removed, forge null-artifact fix)

- **`artifact.digest` is now optional except on identity-minting stages.**
  Required only on `prd-impact-map` (H1/H2), `spec-implementation-plan` §10
  (`plan_digest`), and `spec-technical-review` ADR Lint evidence. All other
  stages (feasibility, TDD, plan, pre-implement, wave-execution, ground-spec,
  learning-extract) may omit it — `artifact.path` existing at the canonical
  path is sufficient walk-time proof-of-write. Nothing in this repo's
  validators (`scripts/handoff_contract.py`) ever read the generic per-hop
  digest; only H1/H2/`map_revision` were ever compared. See
  `references/handoff-envelope.md` (Required fields, Durable identity vs
  mid-lane digests) and `references/artifact-write-contract.md` (Durable
  identity).
- **Removed self-referential "freshness table" digests** that were never
  attested by any human reviewer and were already disclaimed as non-SSOT in
  each skill's own `SKILL.md`: `initiative-feasibility` "Spec digest",
  `spec-technical-review` "Feasibility digest", and `spec-implementation-plan`
  `source_spec_digest` / `feasibility_digest` / `technical_review_digest`.
  `prd_digest`, `repo_scope_digest`, and Gate 2's `plan_digest` (§10 Approve
  attestation) are unchanged.
- **Fixed forge-skill contract gap:** `open-draft-pr` and `commit-workspace`
  had no `references/output-template.md` and no documented null-artifact
  case, unlike `create-board-tickets`. Vague "persist a durable note" prompt
  wording invited an orphan workspace file with a fabricated digest on every
  run. Both now ship an explicit template (`artifact.path: null`) matching
  `create-board-tickets`'s already-correct pattern; `check_consistency.py`
  enforces it.
- No change to `H1`–`H4`, `G1`–`G3`, `plan_digest`, ADR Lint evidence, the
  `outcome`/`next_candidates`/`human_checkpoint`/`external_action`/`forge`
  navigation fields, or any workflow transition. No canonical report file is
  removed or renamed; every stage still writes its full content — only the
  self-reported/never-verified digest line is gone.
- Prompt packages: `initiative-feasibility@1.3.1`,
  `spec-technical-review@1.3.1`, `spec-implementation-plan@1.6.1`,
  `ground-spec@1.3.1` (PATCH — wording only); `open-draft-pr@1.2.0`,
  `commit-workspace@1.2.0` (MINOR — new output-template reference).
- **Partner note (Gateflow):** if any consumer hard-validates a non-null
  `artifact.digest` on every envelope, it must be relaxed to match this
  contract before remounting this tip — see `docs/for-gateflow.md`.

### Breaking — Wave-acceptance replaces live-verify; remove `/verify`

- Checkpoint `live-verify` → **`wave-acceptance`**. `pass` = **human approved**
  for the wave tip (only approval signal). Phase-1 accept ingress: GitHub label
  `wave-accepted` (docs/contract; content skills never apply labels).
- Skill **`/verify` removed** — no content skill for live smoke; policy folded
  into `skills/development/pre-implement/references/live-smoke-policy.md`.
- Pass-2 closeout (`learning-extract` → `ground-spec`) **closes the wave**.
  `wave-signoff` = **merge/publish only** — not a second human approve.
  `human_approved` comes from `wave-acceptance`, not signoff.
- WorkManifest / plan `evidence_expected` for live intent prefers
  `wave-accepted on tip` / human wave-acceptance; optional/legacy
  `Live-Verify-*` reports are PURGE-only and not gate SSOT.
- Keep `live_verify_dir` / `tests/verify` script paths and WorkManifest
  `verify_command` field names.

### Added — ADR product-boundary lint (spec lane)

- `scripts/adr_boundary_lint.py` (+ byte-identical copies under
  `spec-technical-review` / `spec-implementation-plan` scripts) rejects REQ /
  feature prose in ADR Context/Decision/Consequences and TDD engineering
  sections; supports `--strict`, evidence digest print/verify, and `--tdd`.
- Spec lane: feasibility `ALTERNATIVE:` / F13, TDD T12 independent re-read +
  required lint evidence, plan P13 re-check, `TF-*` finding ids, tighter ADR
  template scope, and clearer `needs-input` vs `findings` outcome split.
- Consistency sync for lint copies; unit + development-stage contract coverage.

### Breaking — Stack identity equality (retagged tip)

- Rename `profiles/frontend.yaml` → `profiles/nextjs-frontend.yaml`
  (`profile: nextjs-frontend`). No `prayog_profile` aliases.
- Add `profiles/flink.yaml` and `profiles/edge-agent.yaml`.
- Remount: keep pin tag **`v0.5.0-rc.2`**, fetch retagged tip, then
  `launchpad reset-harness` → `apply-harness`. Drop harness `prayog_profile:`
  keys and any `data-platform` **stack** keys (team `data-platform-devs` is
  domain ownership, not a stack).

### Added — Durable roots, light freshness, initiative-closure purge lane

- Contract: KEEP/PURGE tables, H1–H4 / G1–G3 identities, digest recipes in
  `references/artifact-write-contract.md`; WorkManifest board longevity;
  handoff mid-lane digests are walk-time only.
- Skills: mint/cite on `prd-impact-map` / `spec-draft`; light T0 on feas / TDD /
  plan; board spend wording on `create-board-tickets` / `pre-implement`.
- New skills: `purge-initiative-artifacts-app` (eng), 
  `purge-initiative-artifacts-meta` (PM) — independent packages; **handoff-only**
  success (no `Purge-*.md` reports). Profiles list both.
- Workflow: eng then PM self-contained loops —
  `initiative-closure` → app purge → `initiative-closure-pr-action-app`
  (automated) → `initiative-closure-signoff-app` → meta purge →
  `initiative-closure-pr-action-meta` (automated) →
  `initiative-closure-signoff-meta` → `workflow-complete`. Purge once after
  all waves; no Gateflow authorize-before-delete; no per-wave purge.
- Docs: overview / for-gateflow / for-launchpad declare consumer remount duties
  (Launchpad materialize + Gateflow Enter-at are out of this repo).

### Added — Pin-declared board status hops (orch-only Forge)

- Workflow: `board-tickets-action` → `wave-in-progress-action` (`update_board_status`
  / `in_progress`, automated) → `pre-implement`; `ground-spec` →
  `wave-done-action` (`done`, automated) → `wave-signoff` (human merge).
- Contract: `update_board_status` promoted from reserved to forge `actions.enum`;
  **no** human `skills/forge/update-board-status` (AGENTS stays on forge trio).
- Orch process is pin-only (`workflow.yaml`); no off-graph status side effects.

### Changed — Spec Pass-1 always enters technical review

- Pin: `initiative-feasibility` `pass` and `findings` both route to
  `spec-technical-review` (was: `pass` → `spec-implementation-plan`).
- First human stop after automated Draft PR + orch hops is
  `technical-review-approval`; plan stays manual after PE approval.
- Fixtures / Spec Pass-1 docs / feasibility outcome rubric updated.

### Fixed — Spec Pass-1 tip hygiene

- CHANGELOG: Spec Pass-1 recorded under `[0.5.0-rc.2]` (not only Unreleased).
- `for-gateflow.md`: remove stale “closeout still Gateflow INIT” line; document
  intentional `meta_workspace` optional-in-schema + Gateflow fail-closed on
  spec start.
- `spec-implementation-plan` template/fixtures surface `meta_workspace` for
  human plan hops.

### Added — Spec Pass-1 (orchestrated draft → Draft PR → feasibility / TDD stop)

- Pin: `spec-draft`, `initiative-feasibility`, and `spec-technical-review` are
  `dispatch: orchestrated`. `spec-implementation-plan` stays `manual`; Gate 2 /
  merge / board stay human or `authorization: explicit`.
- Feasibility always enters TDD before plan (`pass` and `findings` →
  `spec-technical-review`).
- Prompt contract: shared optional `meta_workspace` (app `workspace` + meta
  checkout). All packages MINOR-bump schemas; Spec Pass-1 skills (and plan)
  surface dual roots in templates / fixtures / SKILL Inputs where applicable.
- **Intentional sharpness:** schemas keep `meta_workspace.required: false`
  (shared-dict SSOT). Gateflow **fail-closes** on empty meta checkout at
  `POST /waves/spec/start`; do not flip Pass-1 packages to `required: true`
  without a PE Decision for per-skill required overrides.
- Docs: Spec Pass-1 + remount checklist in `docs/for-gateflow.md` (and overview
  pointer). Breaking for Gateflow: `POST /waves/spec/start` Enter-at is legal
  when programmes remount this tip.

### Added — External-action `authorization` knob (`explicit` | `automated`)

- Every `external-action` **must** set `authorization` (`explicit` or
  `automated`); omission is invalid (no debt / no default).
- `automated`: ForgeClient runs when `handoff.forge` requires are complete —
  no interactive STOP. `explicit`: STOP for authorize, then Forge (previous
  behavior).
- Day-one: `spec-pr-action` + `wave-pr-action` = **`automated`**; all other
  external-actions = **`explicit`**. No merge Forge action.
- Contract: `delivery-contract.yaml` `forge.external_action.authorization`;
  consumer algorithm in `references/forge-side-effects.md`.
- Fixtures/tests/consistency enforce the field and day-one values.

### Changed — Wave Draft PR after loop-spec (Pass-1 uninterrupted coding)

- Workflow: `pre-implement.pass` → `loop-spec` → `wave-pr-action` → `live-verify`
  (was PR open before coding). Avoids mid-Pass-1 STOP before `loop-spec`.
- `pre-implement` `commit_workspace: required` — checklist on `head_ref` before coding.
- `loop-spec.pass` fills `open_draft_pr` readiness; first Draft PR view has
  checklist + code. Still no merge Forge action.
- Prompt packages: pre-implement `@1.6.0`, loop-spec `@1.5.0`.

### Added — Wave Draft-PR preparation (Initiative C1)

- Workflow: originally `pre-implement.pass` → `wave-pr-action` → `loop-spec`;
  **superseded** — see “Changed — Wave Draft PR after loop-spec” above.
- Reuses existing `open_draft_pr` / `/open-draft-pr`; **no** merge Forge action.
- `wave-signoff.pass` requires human-recorded reviewed head SHA and merge
  commit SHA; Gateflow and Forge cannot merge.
- Docs / forge policy fixture / workflow scenarios updated for `wave-pr-action`.

### Deferred — Initiative C2 (out of scope)

- Evidence probes, blocking security-gate / T13 infrastructure, and task-level
  `parallel_safe` / concurrency remain deferred pending separate
  cross-repository design. Not claimed as implemented in this remount.

### Added — Prayog-owned WorkManifest contract (Initiative B)

- Canonical contract `references/workmanifest-contract.md` with identity
  `apiVersion: prayog/v1` + `kind: WorkManifest` (immutable approved execution
  intent: epic/waves/tasks/deps/files/exit proof/wave verification).
- Registered in `delivery-contract.yaml` (`workmanifest_spec` + identity);
  board status and runtime evidence stay out of the approved manifest.
- Shared validator `scripts/workmanifest_contract.py` (CLI + importable
  `validate_workmanifest`) with fixtures under `tests/fixtures/workmanifest/`
  and `tests/test_workmanifest_contract.py`.
- Plan check **P16** WorkManifest contract validity; strengthened P4/P5/P7/P10/P15
  for objective exit evidence and unit/integration/smoke/sandbox layers.
- §9 seed uses `prayog/v1` (not `launchpad/v1`); TASK rows + verification
  coverage + live-verification intent in the plan output template.
- Workflow board prerequisite renamed to documented predicate
  `workmanifest-contract-pass` (Initiative B; wave-pr-action lands in C1).
- Prompt package `spec-implementation-plan` bumped `@1.3.0` → `@1.4.0`.
- Development-stage scenarios for vague exit, dependency cycle, missing
  file/proof/live, unit-as-live, and correct N/A-layer outcomes.
- **Consumer alignment:** `/pre-implement`, `/loop-spec`, and `/verify` consume
  the canonical WorkManifest (fail-closed preflight; dependency-ordered
  file-scoped execution with observed evidence in Wave-Execution; layer
  ownership + expected-versus-observed live evidence). `/create-board-tickets`
  validates via the shared contract and projects TASK metadata without making
  board text a second authority (Forge mutate behavior otherwise unchanged).
- Prompt packages bumped `@1.3.0` → `@1.4.0` for pre-implement / loop-spec /
  verify; create-board-tickets `@1.1.0` → `@1.2.0`.
- Docs: Gateflow must reject unsupported manifest versions and consume the
  exact pinned Prayog contract before remount; Launchpad materializes only.

### Added — Development skills remediation (Initiative A)

- Deterministic stage outcome rubrics for `spec-draft`, `initiative-feasibility`,
  `spec-technical-review`, `spec-implementation-plan`, `pre-implement`,
  `loop-spec`, `verify`, and `ground-spec` (existing vocabulary only).
- Product vs architecture boundary: spec owns observable `REQ-*`; ADRs bind to
  approved REQs; new check **T12** Product-boundary integrity.
- Ground findings namespace **`GF-*`** (no longer reuse feasibility `FF-*`);
  ground checks **G1–G10**; canonical implement-lane artifacts
  `Pre-Implement-*`, `Wave-Execution-*`, `Live-Verify-*`.
- Content/Forge cleanup: no per-TASK commits in `loop-spec`; `pre-implement`
  is gate-only (never opens a branch or implements product code).
- Semantic routing fixtures: `tests/fixtures/development_stage_scenarios.json`
  + `tests/test_development_stage_contract.py` (contract-policy, not LLM
  behavioral guarantee).
- Prompt revisions bumped for affected development packages.
- **Migration:** remount requires a new tag/pin. Open initiatives keep their
  pinned behavior until explicit remount; migrated initiatives rerun from the
  earliest materially affected stage. Forge authorization unchanged in A/B.

### Added — Co-ship live-verify scripts (human executes)

- Plan check **P15**: new/material product surface ⇒ same wave ships unit TEST
  **and** FILE under `live_verify_dir`; `verify_command` is live script entry
  (not unit / `make test` / bare N/A when P15 applies).
- `/loop-spec`: implement verify FILEs; run check+unit only; handoff lists human
  `{verify_command}`; never live verify as skill success.
- `/pre-implement`: gate requires co-shipped live path when P15 applies; human
  live-verify stub on checklist.
- Verify policy: unit = agent bar; live script = human at checkpoint
  `live-verify`; `/verify` stays `dispatch: manual` (optional).
- Docs: `overview`, `for-gateflow`, README ladder.
- Prompt packages bumped `@1.1.0` → `@1.2.0` for plan / pre-implement /
  loop-spec / verify.

### Changed — Pass-1 live-verify stop + learning-extract closeout

- Checkpoint ids ≡ purpose: `gate-1` → `prd-impact-acceptance`, `gate-2` →
  `coding-readiness`, `wave-human-decision` → `wave-signoff`. Labels unchanged.
- Pass-1: `loop-spec.pass` → `live-verify` → `wave-awaiting-closeout` (park).
- `verify` is `dispatch: manual`; optional path `verify` → `learning-extract`.
- New orchestrated skill `learning-extract` (MD + YAML fence, `L-*` taxonomy) →
  `ground-spec` → `wave-signoff`. HOW: H1–H6 (worker ingest; no skill HTTP).
- App profiles include `learning-extract`.
- Docs Option A: `docs/` orientation (`overview`, `for-launchpad`, `for-gateflow`,
  `id-map`); engg-reviews plan under `skills/engg-reviews/`.

### Changed — Retire `/board-seed`; single `/create-board-tickets` after merge

- Removed content skill `skills/development/board-seed/`.
- Workflow: `spec-merge` → `board-tickets-action` (`forge.action: create_board_tickets`)
  → `pre-implement`. Human runs `/create-board-tickets` (preflight + confirm + seed).
- Profiles: dropped `board-seed` from `development_skills`; `forge_skills` on all
  profiles including `meta-pm`.
- `create-board-tickets` absorbs merge-gate / board-bind / §9 preflight formerly
  in board-seed.

### Added — Forge pin + handoff readiness + human forge skills

- Merged former `forge-producer-rules.md` into `forge-side-effects.md` (**Content producers**).

- Pin `forge.commit_workspace` on every content skill; `forge` on
  `prd-pr-action` / new `spec-pr-action` (`action: open_draft_pr`, projection
  labels, `requires`). Spec `pass` → `spec-pr-action` → feasibility.
- Handoff optional `forge:` instance payload (pin wins policy; skill fills
  slots). Content skills do not treat local CLI as success; recommend
  `/open-draft-pr`, `/commit-workspace`, `/create-board-tickets`.
- Human forge skills under `skills/forge/` (parity with Gateflow ForgeClient):
  `commit-workspace`, `open-draft-pr`, `create-board-tickets` — not on graph
  `outcomes`; `disable-model-invocation: true`. Prompt packages `@1.0.0`.
- Content prompt packages bumped `@1.0.0` → `@1.1.0` (forge awareness stanza).
- SSOT: `references/forge-side-effects.md` (includes **Content producers**),
  `delivery-contract.yaml` `forge:`, `tests/fixtures/workflow_forge_policy.json`.
- Demix: content skills no longer execute forge via local CLI; they fill
  `handoff.forge` and recommend forge skills. Board seeding is forge-only
  (`/create-board-tickets`); former content `board-seed` removed.

### Changed — Derive `human_checkpoint` from pinned `workflow.yaml`

- `human_checkpoint` means the resolved next node’s `type` is `human-checkpoint`,
  not “artifact deserves review.” Producers derive `next_candidates` +
  `human_checkpoint` from pinned `workflow.yaml` for `(stage, outcome)`.
- SSOT: `references/handoff-envelope.md` (**Derive from pinned workflow**).
- All 13 packaged skills / prompt templates updated; implement-lane contrast
  examples (`pre-implement`/`pass`→`false` vs `ground-spec`/`pass`→`true`).

### Changed — Orchestrator baton dual-write (`handoff_path`)

- Prompt packages and `SKILL.md` Workflow handoff sections require writing the
  durable `handoff:` envelope to the bound `{{handoff_path}}` baton (in addition
  to the workspace skill artifact). Fixes Gateflow BOUNDINPUT empty-baton
  fail-closed when templates only “preferred” that path for read.
- SSOT: `references/handoff-envelope.md` (Orchestrator baton) +
  `references/prompt-package-contract.md`. Consistency checks forbid the old
  Prefer-only wording.

### Added — Skill prompt packages (INIT-PRAYOG-SKILLS-003-PROMPTS)

- Per-skill **prompt packages** for every skill under `skills/requirements/`
  and `skills/development/` (**13/13**): `prompts/{template.md,schema.yaml,fixtures/}`.
- Coverage is **directory inventory** — independent of workflow `dispatch`.
  `skills/engg-reviews/` remains out of scope.
- Shared v1 variables (normative `required`): `ticket`, `initiative`,
  `handoff_path`, `workspace`, `skill_id`. Simple `{{var}}` only.
- Semver `revision` in `schema.yaml`; outcome consumers return
  `prompt_id` + `prompt_revision` (runtime bind/render = BOUNDINPUT later).
- Contract surface: `references/prompt-package-contract.md`,
  `scripts/prompt_contract.py`, `tests/fixtures/prompt_inventory.json`,
  `tests/test_prompt_contract.py`, consistency check
  `check_prompt_package_surface()`.
- **Eval before promote:** golden fixtures green + CHANGELOG lists
  `prompt_id@revision` + consistency/unittest pass.
- Initial revisions: all packages `@1.0.0`
  (`validate-requirements`, `review-findings`, `update-documents`,
  `prd-impact-map`, `spec-draft`, `initiative-feasibility`,
  `spec-technical-review`, `spec-implementation-plan`, `board-seed`,
  `pre-implement`, `loop-spec`, `verify`, `ground-spec`).

### Added — ID coherence, artifact write contract, review briefs, board TASK linkage

- **`references/id-conventions.md`** — Product (`CAP`/`REQ`/`CTR`/`OQ`),
  process (`VF`/`FF`/`CHG`/`PQ`), delivery (`INIT`/`EPIC`/`W`/`TASK`);
  `REQ-*` canonical (legacy `FR-*` alias); handoff blockers use stable ids.
- **`references/artifact-write-contract.md`** — One canonical path per artifact
  kind; overwrite + in-file revision; forbid `*-revN` / `*-v2` siblings.
- **PM:** canonical `Validation-Report-{INIT}.md` /
  `Resolution-{INIT}.md`; stable `VF-*` findings; decision-brief
  `review-findings`; `CHG-*` linked to `VF-*`.
- **Dev:** spec/plan/ground cite `REQ-*`; plan TASK **implements** `REQ-*`
  (no shadow `REQ-W*`); §9 + board-seed list TASK ids on wave bodies;
  `loop-spec` binds TASK + structured failure blockers.

### Added — Workflow dispatch policy + human-checkpoint purpose (INIT-PRAYOG-SKILLS-002)

- **`dispatch`** on every `type: skill` node in `workflow.yaml`:
  `manual` | `orchestrated` (rc-2 v1). Default policy: nine upstream skills
  `manual`; wave lane (`pre-implement`, `loop-spec`, `verify`, `ground-spec`)
  `orchestrated`. Flip any skill later by editing YAML + policy fixture.
- **`purpose`** required on every `type: human-checkpoint` (intent slug).
  Mechanism remains `human-checkpoint` — **`type: gate` is forbidden**.
- `delivery-contract.yaml` documents enum, schema default (missing → `manual`),
  consumer algorithm, and principle **`invocation-mode-is-not-an-exemption`**
  (human `/skill` and AgentRunner share workflow + delivery legality).
- `references/handoff-envelope.md` — resolve/stop/dispatch rules; 
  `next_candidates` never authorize invoke.
- `tests/fixtures/workflow_dispatch_policy.json` — editable policy SSOT for CI.
- Contract tests + `scripts/check_consistency.py` assert dispatch/purpose.

### Changed

- SDD skill `## Workflow handoff` sections defer transitions to pinned
  `workflow.yaml` (no divergent hardcoded edges).
- Consumers must **not** hardcode skill-id allowlists; read pinned workflow.

### Pin guidance

- v0.4.3 pins without `dispatch` → treat as `manual` (fail closed for
  orchestration). Upgrade pin after release tag for wave auto-dispatch.
- Prompt packages ship on the **`v0.5.0` family**. Automated consumers
  resolve briefs from the pin; missing/invalid package → **fail closed**.
  Humans may freeform.
- Before pin/tag promote of prompt revisions: fixtures green, checklist, and
  CHANGELOG `prompt_id@revision` entries.
- engg-reviews PE pack remains adjunct (`engg-reviews/v1`) — not part of
  this delivery-contract change.

---

## [0.4.3] — 2026-07-14

### Added — SDD delivery contract (Gate 1 / Gate 2) and `/board-seed`

- Root `delivery-contract.yaml` and `workflow.yaml` — portable skill chaining;
  every skill emits the shared persistent handoff envelope.
- **Gate 1 (meta):** `/prd-impact-map` revisioned artifact, Draft-PR readiness
  handoff, PE-controlled pending/blocked/LGTM labels.
- **Gate 2 (app):** Draft spec PR + labels (`spec-pending`, `spec-lgtm`, …);
  full package on head before PE unlock; Approve attestation body in
  `spec-implementation-plan` §10.
- **`/board-seed`** — stack-agnostic post-merge board seeding (governance board
  binding, EPIC + wave sub-issues on org Project). On all app profiles;
  `workflow.yaml` `board-seed` is `type: skill`.
- Delivery contract `profiles: [app]` token for Gate 2 on any non-meta-pm stack.
- `pre-implement` / `loop-spec` block coding until spec merge with `spec-lgtm`
  and board-seed complete.
- Feasibility, TDD, planning, and pre-implement templates carry freshness and
  command contracts; CI validates handoff/ripple fixtures.

### Changed

- `spec-draft` mirrors the PM lane (local slice → readiness handoff → Draft PR
  after explicit authorization); fails closed on stale/unapproved handoffs (D1–D12).
- Downstream eng skills keep Draft PR + `spec-pending` through planning;
  **`spec-lgtm`** only after full package.
- `spec-implementation-plan` delegates post-merge seeding to `/board-seed`;
  §9 `target.project` must match `governance.project_board.name`.
- `update-documents` separates Resolution and Ad-hoc modes; new semantic
  choices route back to `review-findings`.

### Fixed

- **ADR lifecycle** — `/spec-technical-review` creates Draft ADR files under
  `{adr_dir}`; TDD §4 is an index. PE acceptance before planning; P12/P13
  verify Accepted ADR files (no obsolete promotion tasks).
- Technical-review T1–T11 refs; WorkManifest P14 / `spec_path`; wave ordering
  (grounding before human approval); verify-policy layout defaults.

---

## [0.4.2] — 2026-07-09

### Added — `profiles/meta-pm.yaml` for launchpad PM harness lane

- **`profiles/meta-pm.yaml`** — declares `requirements_skills` for meta workspace
  (`validate-requirements`, `review-findings`, `update-documents`, `prd-impact-map`)
  and PM layout paths (`prd/`, `prd/reports/`).
- **`scripts/check_consistency.py`** — validates `requirements_skills` entries resolve
  under `skills/requirements/`.
- **`profiles/README.md`** — documents meta-pm profile for harness consumers.

---

## [0.4.1] — 2026-07-08

### Fixed — ADR promotion gap between `/spec-technical-review` and `/spec-implementation-plan`

Draft ADRs written in TDD §4 were not being promoted to Accepted files in
`{adr_dir}` after PE sign-off. No skill enforced the promotion step, so
`docs/specification/adr/` remained empty even after PE Approve. Downstream
skills (`/pre-implement`, `/ground-spec`) read from `adr_dir` and silently
consumed nothing.

Root cause: responsibility for promotion was delegated to "PE or human" in
`spec-technical-review` with no corresponding TASK template, check, or file
format in `spec-implementation-plan`.

#### `spec-implementation-plan/references/checks.md`
- **P12** — strengthened: now requires a pre-W0 `TASK-SPEC-ADR-NN` per
  `NEW-ADR` that produces a file at `{adr_dir}/adr-NNN-{slug}.md`; §0
  "Resolved ADRs" must link to `adr_dir` file paths, not TDD section refs;
  explicit **FAIL** if `NEW-ADR` findings exist but no `adr_dir` file is
  created or planned.
- **P13** — strengthened: now requires PE sign-off to be `[x] complete —
  {date}` (not merely "stated"); explicit **FAIL** if TDD Status field still
  reads `Draft` when the plan runs.
- **Title** — corrected file heading from `P1–P12` to `P1–P14`.

#### `spec-implementation-plan/SKILL.md`
- **T3 Plan** — now specifies a mandatory pre-W0 `TASK-SPEC-ADR-NN` for each
  TDD §4 draft ADR: promote to `{adr_dir}/adr-NNN-{slug}.md` with status
  Accepted, PE name, and date.
- **Prerequisite** — added explicit prose explaining that PE GitHub Approve has
  no automatic signal to the skill chain; the dev must commit an updated TDD
  Status field (`Accepted — @{pe-name}  {date}`) to the spec branch before
  running this skill. P13 reads that field to verify sign-off.

#### `spec-implementation-plan/references/output-template.md`
- **§0 "Resolved ADRs"** — clarified to require `adr_dir` file paths; TDD
  section refs are explicitly not sufficient.
- **§6 As-built and docs tasks** — added conditional `TASK-SPEC-ADR-NN` row
  (one per `NEW-ADR`) with a full **Accepted ADR file format** callout
  (Status, Date, PE, TDD fields); states that the acceptance date comes from
  the GitHub Approve event, not the file write date.

#### `spec-technical-review/SKILL.md`
- **Draft ADR format** — removed "PE or human commits the ADR file" with no
  further guidance; replaced with explicit handoff: `/spec-implementation-plan`
  owns `TASK-SPEC-ADR-NN`; manual promotion by PE/human is a valid fallback.

#### `spec-technical-review/references/checks.md`
- **T11 ADR promotion path** (new check) — each TDD §4 draft ADR must state
  how it will reach `{adr_dir}`: via a plan `TASK-SPEC-ADR-NN` or an explicit
  human step. Absence of any promotion path is a blocking finding.
- **Blocking condition** updated to include T11.

#### `spec-technical-review/references/output-template.md`
- **§4 ADR resolutions** — added normative lifecycle callout at section top:
  Draft → PE Approve → two required record-keeping steps (TDD status update +
  `adr_dir` file). Each `§4.N` draft block now carries a `**Target file:**`
  field.
- **Check summary table** — added T11 row.
- **PE review checklist** — added T11 item.

#### `governance.md` (SYNC-COPY — three files)
- `spec-implementation-plan/references/governance.md`
- `pre-implement/references/governance.md`
- `initiative-feasibility/references/governance.md`

Added **Accepted ADR SSOT** callout under F13/P12: TDD §4 draft sections are
not substitutes for Accepted ADR files at implementation time; a `draft-ADR
TASK` must produce a file at `{adr_dir}/adr-NNN-{slug}.md`. All three copies
remain byte-identical (SYNC-COPY constraint verified).

---

## [0.4.0] — 2026-06-xx

Two-PR delivery model. See PR #17.

## [0.3.2] — prior

See git log.
