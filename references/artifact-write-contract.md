# Artifact write contract (SSOT)

Rules for files skills create or update in consumer repos. Git history is the
archive — `reports/` is **not** a version-control tree of sibling revisions.

See also: [id-conventions.md](id-conventions.md),
[workmanifest-contract.md](workmanifest-contract.md),
[handoff-envelope.md](handoff-envelope.md).

## Canonical paths (one path per concern)

| Artifact | Canonical path | In-file revision field | Longevity |
|----------|----------------|------------------------|-----------|
| Validation report | `{reports_dir}/Validation-Report-{INIT}.md` | `report_revision` | PURGE (meta) |
| Resolution summary | `{reports_dir}/Resolution-{INIT}.md` | optional `resolution_revision` | PURGE (meta) |
| Impact map | `{reports_dir}/Impact-Map-{INIT}.md` | `map_revision` | **KEEP** (meta) |
| Spec product | `{product_spec_dir}/INIT-{id}.md` | digests in front matter | **KEEP** (app) |
| Feasibility | `{reports_dir}/Initiative-Feasibility-Report-{INIT}.md` | digests | PURGE (app) |
| Technical review | `{reports_dir}/Technical-Review-{INIT}.md` | digests | PURGE (app) |
| Implementation plan | `{reports_dir}/Implementation-Plan-{INIT}.md` | digests | PURGE (app) — walk-time |
| Pre-implement checklist | `{reports_dir}/Pre-Implement-{INIT}-W{N}.md` | per wave | PURGE (app) |
| Wave execution | `{reports_dir}/Wave-Execution-{INIT}-W{N}.md` | per wave | PURGE (app) |
| Live verify report | `{reports_dir}/Live-Verify-{INIT}-W{N}.md` | per wave | PURGE (app) |
| Ground report | `{reports_dir}/Ground-Report-{SPEC}-W{N}.md` | per wave | PURGE (app) |
| Learning extract | `{reports_dir}/Learning-Extract-{INIT}-W{N}.md` | per wave | PURGE (app) |

`{reports_dir}` defaults: meta `prd/reports`; app `docs/specification/reports`.
Resolve from `.harness/profile.yaml` when present.

**Also KEEP (not in the reports table):** meta `prd/INIT-*.md`; app Accepted ADRs;
product source / unit tests / live-verify **scripts** (not Live-Verify report
prose). **Outside the tree:** programme board WorkManifest projection; Gate 1 /
spec / wave / initiative-closure merge SHAs on PRs.

Draft ADRs under `{adr_dir}` are **PURGE (app)** until Accepted — then KEEP.

## Durable roots and purge (initiative closure)

Working papers accumulate through all waves. **One mental model:** purge
**once** after `initiative-closure` (all waves done), not per wave-signoff.

| Repo | KEEP (refuse delete) | PURGE allowlist |
|------|----------------------|-----------------|
| **meta** | `prd/INIT-*.md`, `Impact-Map-{INIT}.md` | `Validation-Report-{INIT}.md`, `Resolution-{INIT}.md` |
| **app** | `product/INIT-*.md`, Accepted ADRs, source / unit / live-verify **scripts** | Feas, TDD, Implementation-Plan, Pre-Implement-W*, Wave-Execution-W*, Live-Verify-W*, Ground-Report-W*, Learning-Extract-W*, Draft ADRs |

**Lane (pin):** `initiative-closure` → `purge-initiative-artifacts-app` →
`purge-initiative-artifacts-meta` → `initiative-closure-pr-action` →
`initiative-closure-signoff` → `workflow-complete`. Closure work branches from
`develop`; Forge opens closure Draft PR(s); human merges (Gateflow does not
merge). No Gateflow authorize-before-delete — safety is allowlist + refuse KEEP
+ idempotent delete. Dual-walker: same skill packages for human `/skill` and
Gateflow orch.

Purge skills may delete **only** allowlisted paths for `{INIT}`. They **must
refuse** any KEEP path. Missing allowlisted files → ok (idempotent `pass`).

## Durable identity (H1–H4, G1–G3)

Hash / cite roots of meaning that survive purge. Do **not** use mid-lane
`artifact.digest` (feas / TDD / plan / wave reports) as long-term staleness SSOT.

| Id | Meaning | Mint / cite |
|----|---------|-------------|
| **H1** | `prd_digest` / `source_prd_digest` | `prd-impact-map`; cited in product spec |
| **H2** | `scope_digest` (per affected repo) | `prd-impact-map` (recipe below); cited in product spec |
| **H3** | `map_revision` | `prd-impact-map`; cited in product spec |
| **H4** | Product-spec header citations of H1–H3 (+ G1 while open) | `spec-draft` |
| **G1** | Gate 1 meta PR head + tech-lead APPROVED | acceptance / `spec-draft` Gate 1 |
| **G2** | Spec merge commit SHA(s) | after spec merge |
| **G3** | Wave merge commit SHA(s) | after `wave-signoff` |

### Digest recipes

**H1 — PRD digest.** SHA-256 of the canonical PRD file bytes as read for the
map (`prd/INIT-*.md`), hex prefixed `sha256:`. Record as `source_prd_digest`.

**H2 — scope digest.** For every affected repository, SHA-256 of this canonical
UTF-8/LF payload, sorted list values, exactly one final newline:

```text
repo={org}/{repo}
status=affected
capabilities={sorted CAP-* and/or REQ-* identifiers (legacy FR-* ≡ REQ-*), comma-separated}
contracts={sorted provider->consumer contract identifiers, comma-separated}
depends_on={sorted repository names, comma-separated}
scope={single-line normalized scope summary}
```

**H3 — map revision.** Integer `map_revision` on the Impact-Map canonical path
(overwrite + bump; never `*-revN` siblings).

**Light freshness (mid-lane):** `initiative-feasibility`, `spec-technical-review`,
and `spec-implementation-plan` compare product-spec citations (H1–H3) and tip
continuity (and G1 while the meta gate still applies). `stale` means **authority
drift**, not “missing feas/TDD/plan digest.”

## NON-NEGOTIABLE

1. **Overwrite the canonical path.** Never create
   `*-revN`, `*-v2`, or dated sibling copies for the same
   initiative and artifact kind.
2. **Bump the in-file revision** (`report_revision`, `map_revision`, …) and
   record prior revision + change reason when the skill defines those fields.
3. **Chat must name the canonical path** (“updated
   `prd/reports/Validation-Report-INIT-….md` revision N”), never imply a new
   filename family.
4. **Per-wave implement-lane artifacts** — `Pre-Implement-…-W{N}`,
   `Wave-Execution-…-W{N}`, `Live-Verify-…-W{N}`,
   `Ground-Report-…-W{N}`, and `Learning-Extract-…-W{N}` are different concerns
   per wave, not revisions of one file.
5. **ADRs** use `adr-{NNN}-{slug}.md` lifecycle (Draft → Accepted), not
   `adr-…-rev2.md`. Accepted ADRs are KEEP; Draft ADRs are PURGE.
6. If a non-canonical sibling already exists from older runs, **migrate**:
   copy/merge into the canonical path, bump revision, and stop writing the
   sibling. Do not delete siblings ad hoc — use
   `/purge-initiative-artifacts-app` or `/purge-initiative-artifacts-meta` (or
   the initiative-closure lane) for allowlisted PURGE paths only.
7. **Purge once** at initiative closure for both app and meta; never invent a
   per-wave purge hop in this pin.

## PM revision loop (expected)

```text
edit PRD
  → validate → overwrite Validation-Report-{INIT}.md (report_revision++)
  → review   → overwrite Resolution-{INIT}.md
  → update   → edit PRD (+ stubs)
  → validate incremental against same Validation-Report-{INIT}.md
  → impact map → overwrite Impact-Map-{INIT}.md (map_revision++)
```

Git commits on the meta PR carry history. Do not accumulate report families
in `prd/reports/`.

## Dual output

Skills may still produce a **chat summary** plus a **file on the canonical
path**. Chat is not workflow state ([handoff-envelope.md](handoff-envelope.md)).
After initiative-closure purge, only KEEP paths remain live; Git retains purged
blobs.
