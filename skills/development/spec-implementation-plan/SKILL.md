---
name: spec-implementation-plan
description: >-
  After feasibility (and technical review when applicable), produce a
  wave-level implementation plan with REQ/TASK/FILE/TEST tables and a
  WorkManifest YAML seed section (§9) for board seeding via gh issue create.
  Use when the dev needs an execution plan before feature branches, or after
  spec merge.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "prd-handoff branch: initiative-feasibility + PE sign-off on spec-technical-review complete"
---

# Spec implementation plan

Turn an accepted initiative spec (+ feasibility report + technical review when
present) into an **executable plan with a board-seed artifact**. **Do not
implement** — plan only.

Table shape borrowed from awesome-copilot `create-implementation-plan`
(REQ/TASK/FILE/TEST/RISK). §9 WorkManifest YAML is the **board-seed artifact**
— dev creates GitHub Issues from it (one issue per wave: `W0`, `W1`, …).

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Every TASK has **done when** criteria and test/verify command from profile toolchain where applicable.
3. Plan scope must not exceed the initiative spec.
4. Dual output: chat summary + saved plan file.
5. Run T0–T5 control loop.
6. Wave IDs must use `W0`, `W1`, … (one GitHub Issue per wave; launchpad WorkManifest `id:` convention).
7. Every TASK row must include `codebase`, `spec_path`, and `verify_command` — required for WorkManifest generation.

## Inputs

Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **Initiative spec** — merged or final (REQUIRED)
2. **Feasibility report** — if exists (RECOMMENDED)
3. **Technical review** — `Technical-Review-{initiative}.md` if produced (RECOMMENDED; required when feasibility had NEW-ADR findings)
4. **As-built**, **tests_readme**, **live_verify_dir** layout (REQUIRED for test tasks)
5. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)
6. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
7. **`adr_dir`** — architecture decision records (REQUIRED). Run relevant-ADR pass per [references/governance.md](references/governance.md) before T2 Analyze.

## Prerequisite

Run **after**:
- Feasibility accepted (no blocking PM questions)
- Technical review PE sign-off complete (when feasibility had NEW-ADR findings)

Ideally after spec is on `develop`.

## Process

1. **T0 Gather** — spec waves, feasibility findings, technical review (if exists), repo layout
2. **T1 Understand** — initiative id, wave boundaries, PR granularity from spec
3. **T2 Analyze** — map each wave to concrete files and tests; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs as **MDC notes** / **ADR notes** in the TASK table
4. **T3 Plan** — build REQ/TASK/FILE tables per wave; add draft-ADR TASK when plan flags `NEW-ADR`; collect `codebase`/`spec_path`/`verify_command` per TASK
5. **T4 Execute** — write plan; build WorkManifest seed section; run P1–P14 checks
6. **T5 Verify** — self-contained plan readable by a fresh session; WorkManifest YAML is valid

## Output

Save to `{reports_dir}/{plan_prefix}-{initiative}.md`.

Use [references/output-template.md](references/output-template.md).

## WorkManifest integration

The plan's final section (§9) emits a ready-to-use WorkManifest YAML stub.

After PE review and spec merge, the **dev team seeds the board** from §9:

```bash
# One GitHub Issue per wave (W0, W1, …) — primary path
gh issue create --repo {org}/{repo} \
  --title "[{INITIATIVE} W0] {wave goal}" \
  --body-file /tmp/w0-body.md \
  --label "{initiative-label}"

# Optional multi-repo / bulk: copy §9 to work/{initiative}.yaml, then:
# launchpad seed-work --config work/{initiative}.yaml --dry-run
# launchpad seed-work --config work/{initiative}.yaml --apply
```

One TASK row in the plan maps to work described in the wave issue body.
Wave hierarchy is expressed via `depends_on` in §9 YAML (and GitHub issue links
in issue bodies when seeding manually).
