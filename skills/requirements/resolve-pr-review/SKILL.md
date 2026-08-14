---
name: resolve-pr-review
description: >-
  Resolves PE/tech-lead review comments on Gate 1 meta PRs in one pass: parse and
  classify each finding, fix the PRD (SSOT), sync satellite docs, re-validate,
  regenerate the impact map from scratch (never patch inline), update the PR body,
  run a final consistency check, and prepare a reply comment. Never posts without
  user approval. Use when a reviewer requests changes on a meta PRD/impact-map PR.
paths: prd/**, config/service-catalog*.yaml
---

# Resolve PR review — Gate 1 comment resolution

## Purpose

Takes a reviewer's PR comment, systematically addresses **every** finding, and
produces a clean commit + draft reply — designed to close all objections in a
**single round**.

**Key principle:** The PRD is the SSOT. The impact map is a **derived artifact**
regenerated from the validated PRD — never patched inline. Every satellite file
(outline, validation report, PR body) is synced to the PRD before the map is
built.

Conventions: `prayog-skills/references/id-conventions.md`,
`prayog-skills/references/artifact-write-contract.md`,
`prayog-skills/references/handoff-envelope.md`,
`prayog-skills/references/forge-side-effects.md`.

Map template: `../prd-impact-map/references/output-template.md`.

Workflow routing: pinned root `prayog-skills/workflow.yaml`.

## When to use

- After a PE / tech lead posts `CHANGES_REQUESTED` or a numbered comment on a
  Gate 1 meta PR
- User provides PR number (or URL) and comment text (or `latest`)

**Not for:** first-time PRD authoring (`/prd`), validation-only runs
(`/validate-requirements`), or interactive resolution of validation findings
(`/review-findings`).

## Inputs

1. **PR number** — meta PR under review (REQUIRED)
2. **Comment** — reviewer comment text, or `latest` to fetch the most recent
   reviewer comment (REQUIRED)
3. **User overrides** — product decisions already made by PM (OPTIONAL)

---

## NON-NEGOTIABLE

1. **Never skip a finding.** Every numbered item in the reviewer's comment must
   map to a section in the response.
2. **Never claim "authorized" / "resolved" without linked evidence.** If
   PE/owner authorization is not recorded in-thread, write **proposed** /
   **pending** and keep the relevant `IM-*` blocking.
3. **Never patch the map inline.** Regenerate it from the validated PRD.
4. **Grep after every bulk edit.** After rename/renumber/reclassify, grep the
   full PRD for the OLD value — must return **0** hits.
5. **Never rubber-stamp validation.** Re-run validation after PRD edits;
   increment `report_revision`; reflect current PRD version.
6. **Compute digests from committed text.** Write H2 payload blocks in the map
   file first, then hash that exact text. Verify by re-extracting from the file.
7. **Derive handoff routing from `workflow.yaml`.** If verdict is **PR BLOCKED**:
   `outcome: blocked` → `requirements-human-decision`; `human_checkpoint: true`;
   `external_action: false`; **no** `handoff.forge`. If **PR READY**: `outcome:
   pass` → `prd-pr-action`; Forge payload required per pin.
8. **Expand every catalog repo in §5.** Never collapse rows (e.g.
   `abhilekh … drivestream-mobile`).
9. **Update the live PR body.** Committed `PR-Body-*.md` and GitHub PR body must
   match. Prefer REST API for body/labels (see impact-map output template).
10. **Every satellite file must match the PRD** — outline, validation report,
    resolution/update-summary naming, PR body revision/digest/blockers.

---

## Phase 1 — Parse and classify

### 1.1 Fetch the comment

If user provides `latest`:

```bash
gh api repos/{owner}/{repo}/issues/{pr}/comments \
  --jq '.[] | select(.user.login != "{bot}") | {id, user:.user.login, body}'
```

Take the most recent **reviewer** comment (not PM/bot replies).

### 1.2 Extract findings

Parse numbered items (e.g. `1. **Fix the wave mappings**`).

### 1.3 Classify each finding

| Type | Signal | Action |
|------|--------|--------|
| **mechanical** | stale refs, wrong wave id, digest mismatch, missing field | Auto-fix Phases 2–6 |
| **template/contract** | missing §10 columns, Forge label policy, handoff routing | Auto-fix from template + workflow |
| **product decision** | choose option 1 or 2 | **STOP — AskQuestion** |
| **missing evidence** | no recorded authorization | Mark `IM-*` blocking; never fabricate |

### 1.4 Gate — product decisions

If any finding is **product decision**, ask via AskQuestion before proceeding.

If **missing evidence**, inform user the map stays **PR BLOCKED** until
authorization is recorded in-thread.

---

## Phase 2 — Fix PRD (SSOT)

1. Read the **full** `prd/INIT-{id}.md`.
2. Apply mechanical fixes; grep for OLD values after each edit (0 hits).
3. Apply approved product decisions only.
4. For missing evidence: move items to Open Questions; remove from Resolved
   Decisions; use **proposed** not **authorized**.
5. Full grep audit (old versions, stale wave ids, unsourced claims).
6. Bump PRD version + document history entry.

---

## Phase 3 — Sync satellite docs

Update every file referencing the PRD:

| File | Sync |
|------|------|
| `prd/INIT-{id}-outline.md` | version, waves, delivery language, footer |
| `prd/reports/Resolution-{INIT}.md` | canonical path only (no `*-rN` siblings) |
| `prd/reports/Update-Summary-{INIT}.md` | revision, stage |

Grep satellite files for old PRD version / map revision / stale terminology → 0 hits.

---

## Phase 4 — Validate

1. Re-run `/validate-requirements` logic (incremental against prior report).
2. Overwrite `prd/reports/Validation-Report-{INIT}.md` with incremented
   `report_revision`, current PRD version, changes detected.
3. If findings > 0, loop to Phase 2.

---

## Phase 5 — Regenerate impact map (from scratch)

**Do not patch the existing map.** Build fresh from validated PRD using
`../prd-impact-map/references/output-template.md`.

1. Frontmatter — bump `map_revision`, set `generated_at` to now,
   `previous_artifact_commit` to pre-fix HEAD, compute **H1** from PRD bytes.
2. §1–§12 — derive from PRD; full §5 catalog (read `config/service-catalog*.yaml`).
3. **H2** — write canonical payload text block in map, then SHA-256 with exactly
   one final newline per `artifact-write-contract.md`. Re-read file and verify
   hash matches recorded digest.
4. **Verdict** — any open blocking `IM-*` → **PR BLOCKED**; else **PR READY**.
5. **Handoff** — derive from `workflow.yaml` (`prd-impact-map` outcomes for
   blocked vs pass). Forge `apply_labels`: **`impact-map-pending` only**;
   `impact-map-revised` is PR projection only.
6. **Artifact digest** — blank-hash convention on handoff `artifact.digest`.

---

## Phase 6 — Update PR body

Regenerate `prd/reports/PR-Body-{INIT}.md` from map §11: revision, H1, affected
repos, blocking questions (must match §10/§11).

---

## Phase 7 — Final consistency check (commit gate)

Run before commit:

| Check | Rule |
|-------|------|
| Version consistency | PRD version identical in PRD, outline, validation header |
| Map revision | frontmatter, §1, §12, PR body |
| Digest consistency | H1/H2/artifact match across map sections + PR body |
| H2 reproducibility | extract `text` blocks from committed map → re-hash |
| Cross-file claims | PRD §4.8 DAG = map §7; Q8 = DS route table; §10 = §11 = PR body blockers |
| Handoff routing | BLOCKED vs READY matches workflow.yaml |
| Stale sweep | old version/revision/terms → 0 hits |
| Template completeness | §10/§11 columns match output template |

**Do not commit** until all checks pass.

---

## Phase 8 — Prepare response (do not post)

1. Build reply: one section per reviewer finding; attestation block (initiative,
   map_revision, head SHA, H1, artifact digest, H2 per repo).
2. Coverage check — no silent skips.
3. Honesty check — no "authorized"/"resolved" without evidence.
4. Present summary + diff + draft comment to user via AskQuestion:
   - commit + push + update PR body + post
   - commit + push only
   - show diff first
   - abort

On **commit-push-post**: use REST API for PR body and labels; post comment only
after user approval.

---

## Integration

| Skill | Relationship |
|-------|--------------|
| `validate-requirements` | Phase 4 — re-run after PRD edits |
| `prd-impact-map` | Phase 5 — full regeneration replaces map output |
| `review-findings` | Different lane — validation report workshop, not PR comments |
| `update-documents` | Phase 2–3 — targeted sync, not full Resolution propagation |

---

## Failure modes prevented

| Failure | Prevention |
|---------|------------|
| Stale refs after bulk rename | Phase 2 grep audit |
| Validation rubber-stamped | Phase 4 mandatory re-run |
| Unsourced authorization claims | Rules 2 + Phase 2.4 |
| Satellite file staleness | Phase 3 + Phase 7 |
| Collapsed §5 / missing §10–§11 columns | Phase 5 template compliance |
| H2 / artifact digest mismatch | Phase 5.3 + Phase 7 H2 verify |
| Verdict vs handoff contradiction | Phase 5.4 + Phase 7 routing check |
| Live PR body drift | Phase 6 + REST API update |
| Silent finding skip | Phase 8 coverage check |

---

## Workflow handoff

Manual skill (`dispatch: manual` in pinned `workflow.yaml`). When regenerating the
impact map (Phase 5), the map artifact handoff follows `prd-impact-map` rules
(`outcome: blocked` or `pass` per verdict). When the skill completes as a whole,
emit stage `resolve-pr-review` per pinned workflow outcomes.

When an orchestrator binds `handoff_path`:

1. Persist initiative artifacts under the meta workspace (PRD, validation report,
   impact map, PR body draft).
2. **Overwrite** `handoff_path` with a minimal `handoff:` envelope before exit.
   Leaving the baton empty is a failed stage for automated consumers.
3. Derive `next_candidates` and `human_checkpoint` from pinned root
   `workflow.yaml` for `(stage: prd-impact-map, outcome)` per
   `prayog-skills/references/handoff-envelope.md` (**Derive from pinned
   workflow**). Set `human_checkpoint: true` only when the resolved next node's
   `type` is `human-checkpoint` — never because the artifact "should be reviewed."
4. Follow `prayog-skills/references/forge-side-effects.md#content-producers` when
   map verdict is PR READY and next is `prd-pr-action` — fill `handoff.forge` per
   pin; never apply `*-lgtm` labels.

Does **not** authorize forge mutations by itself. User approves
commit/push/post separately.
