# generate-work-manifest

Drafts `prayog-meta/work/INIT-*.yaml` (WorkManifest) from a signed-off PRD and per-repo spec slices. Output is consumed by `./scripts/prayog seed-work` — this skill does **not** create GitHub issues.

**Maintainer:** drivestream-lab.

**When:** After PM↔dev handoff Phase 2 merges and spec conformance is clean.

**v1 granularity:** 1 Epic + 1 task per app repo (compose, parichay, abhilekh, ops).

See repo root README for install command.
