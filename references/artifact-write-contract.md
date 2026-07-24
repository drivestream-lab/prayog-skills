# Artifact write contract (SSOT)

Rules for files skills create or update in consumer repos. Git history is the
archive — `reports/` is **not** a version-control tree of sibling revisions.

See also: [id-conventions.md](id-conventions.md).

## Canonical paths (one path per concern)

| Artifact | Canonical path | In-file revision field |
|----------|----------------|------------------------|
| Validation report | `{reports_dir}/Validation-Report-{INIT}.md` | `report_revision` |
| Resolution summary | `{reports_dir}/Resolution-{INIT}.md` | optional `resolution_revision` |
| Impact map | `{reports_dir}/Impact-Map-{INIT}.md` | `map_revision` |
| Spec product | `{product_spec_dir}/INIT-{id}.md` | digests in front matter |
| Feasibility | `{reports_dir}/Initiative-Feasibility-Report-{INIT}.md` | digests |
| Technical review | `{reports_dir}/Technical-Review-{INIT}.md` | digests |
| Implementation plan | `{reports_dir}/Implementation-Plan-{INIT}.md` | digests |
| Ground report | `{reports_dir}/Ground-Report-{SPEC}-W{N}.md` | per wave (new wave = new file) |

`{reports_dir}` defaults: meta `prd/reports`; app `docs/specification/reports`.
Resolve from `.harness/profile.yaml` when present.

## NON-NEGOTIABLE

1. **Overwrite the canonical path.** Never create
   `*-revN`, `*-v2`, or dated sibling copies for the same
   initiative and artifact kind.
2. **Bump the in-file revision** (`report_revision`, `map_revision`, …) and
   record prior revision + change reason when the skill defines those fields.
3. **Chat must name the canonical path** (“updated
   `prd/reports/Validation-Report-INIT-….md` revision N”), never imply a new
   filename family.
4. **Ground reports are per-wave** — `…-W0.md`, `…-W1.md` are different
   concerns, not revisions of one file.
5. **ADRs** use `adr-{NNN}-{slug}.md` lifecycle (Draft → Accepted), not
   `adr-…-rev2.md`.
6. If a non-canonical sibling already exists from older runs, **migrate**:
   copy/merge into the canonical path, bump revision, and stop writing the
   sibling. Do not delete without user authorization.

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

Skills may still produce a **chat summary** plus a **durable file**. The
durable file path is always the canonical path above. Chat is not workflow
state ([handoff-envelope.md](handoff-envelope.md)).
