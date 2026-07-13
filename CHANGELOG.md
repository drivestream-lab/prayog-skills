# Changelog

All notable changes to prayog-skills are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.4.3-rc.1] — local RC

### Added — versioned SDD handoff and freshness contracts

- Root `delivery-contract.yaml` and `workflow.yaml` define portable existing-skill
  chaining; every skill now emits the shared persistent handoff envelope.
- `/prd-impact-map` now produces a canonical, revisioned impact-map artifact
  with PRD and per-repo scope digests, SHA-bound tech-lead approval, explicit
  effective states, and downstream ripple actions.
- `/prd-impact-map` now generates its artifact before a PR exists, emits a
  complete Draft-PR readiness handoff, and forbids GitHub side effects until
  explicit user authorization. Gate 1 uses PE-controlled pending/blocked/LGTM
  labels with revised/stale invalidation labels.
- `/spec-draft` now fails closed on stale/unapproved handoffs and runs D1–D12
  completeness checks covering traceability, acceptance, negative paths,
  contracts, NFR applicability, assumptions, and blocking questions.
- `/spec-draft` now mirrors the PM lane: generate the spec slice locally, emit a
  Draft-PR readiness handoff in chat, and open the Draft spec PR with
  `spec-pending` only after explicit user authorization.
- Feasibility, technical review, planning, and pre-implement templates now
  carry source freshness and command contracts.
- CI now validates check ranges, template contracts, links, profile keys, and
  deterministic handoff/ripple scenarios.
- Added a team-first pilot playbook with scenario coverage, scorecard metrics,
  and review-graduation criteria.
- `update-documents` now separates Resolution and Ad-hoc modes, requires every
  propagated edit to cite an approved decision source, and routes new semantic
  choices back to `review-findings` instead of requesting retrospective sign-off.

### Fixed

- Aligned technical-review references on T1–T11.
- Corrected WorkManifest P14 from §8 to §9 and added `spec_path` to TASK rows.
- Corrected wave ordering so grounding precedes human approval.
- Fixed the verify-policy link to shared layout defaults.
- **ADR lifecycle** — `/spec-technical-review` now creates Draft ADR files under
  `{adr_dir}` and TDD §4 is an index only. PE acceptance (`Draft` → `Accepted`)
  happens on the spec PR before `/spec-implementation-plan`. Removed obsolete
  `TASK-SPEC-ADR-NN` promotion tasks from planning; P12/P13 verify Accepted ADR
  files exist instead.

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
