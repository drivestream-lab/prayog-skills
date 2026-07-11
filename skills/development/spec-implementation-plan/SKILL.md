---
name: spec-implementation-plan
description: >-
  After feasibility (and technical review when applicable), produce a
  wave-level implementation plan with REQ/TASK/FILE/TEST tables and a
  WorkManifest YAML seed section (§9). Runs while the spec PR is open,
  before spec merge. Board seeding (gh issue create) happens after spec
  PR merge — not before.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
metadata:
  background_eligible: true
  background_trigger: "spec PR branch: initiative-feasibility clean + PE Approve on TDD (when required)"
---

# Spec implementation plan

Turn an accepted initiative spec (+ feasibility report + technical review when
present) into an **executable plan with a board-seed artifact (§9)**. **Do not
implement** — plan only.

Commit the plan to the **spec PR branch** alongside spec, feasibility, and TDD.
Table shape borrowed from awesome-copilot `create-implementation-plan`
(REQ/TASK/FILE/TEST/RISK). §9 WorkManifest YAML is generated here; **dev seeds
the board after spec PR merge**.

## NON-NEGOTIABLE

1. Never skip a check in [references/checks.md](references/checks.md). Mark SKIPPED with reason.
2. Every TASK has **done when** criteria and test/verify command from profile toolchain where applicable.
3. Plan scope must not exceed the initiative spec.
4. Dual output: chat summary + saved plan file on spec branch.
5. Run T0–T5 control loop.
6. Wave IDs must use `W0`, `W1`, … (one GitHub Issue per wave; launchpad WorkManifest `id:` convention).
7. Every TASK row must include `codebase`, `spec_path`, and `verify_command` — required for WorkManifest generation.
8. Spec, feasibility, TDD (when present), PRD digest, impact-map revision,
   scope digest, and approvals must agree. Stop on stale sources.
9. Resolve canonical `check_command`, `test_command`, `verify_command`, and
   `ground_command` before planning. Required commands may come from the
   consumer profile, `AGENTS.md`, or `tests_readme`; missing required commands
   block the plan. Use N/A with reason only when a layer is not applicable.

## Inputs

Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **Initiative spec** — on spec branch (REQUIRED)
2. **Feasibility report** — if exists (RECOMMENDED)
3. **Technical review** — `Technical-Review-{initiative}.md` if produced (RECOMMENDED; required when feasibility had NEW-ADR findings)
4. **As-built**, **tests_readme**, **live_verify_dir** layout (REQUIRED for test tasks)
5. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)
6. **`rules_glob`** — workspace MDC rules (REQUIRED). Read before T2 Analyze.
7. **`adr_dir`** — architecture decision records (REQUIRED). Run relevant-ADR pass per [references/governance.md](references/governance.md) before T2 Analyze.
8. **Canonical handoff references** — PRD digest, impact-map revision/scope
   digest, approved meta PR head/review (REQUIRED)
9. **Command contract** — canonical check, test, live-verify, and ground
   commands or explicit N/A rationale (REQUIRED)

## Prerequisite

Run **while spec PR is open**, **before spec merge**, after:
- Feasibility accepted (no blocking PM questions on meta PRD PR)
- PE Approve on spec PR when TDD was required (NEW-ADR findings)
- All upstream source digests and approval references are CURRENT

> **How to confirm PE Approve reached the skill chain:**
> There is no automatic signal from GitHub. After PE clicks Approve on the spec PR,
> the dev must commit a TDD status update to the spec branch:
>   `| Status | Accepted — @{pe-name}  {YYYY-MM-DD} |`  (document header)
>   `**Status:** Accepted — @{pe-name}  {YYYY-MM-DD}`   (each §4.N draft ADR)
> This committed file state is what `/spec-implementation-plan` reads to verify
> sign-off. P13 will FAIL if the TDD Status field still reads `Draft`.

## Process

1. **T0 Gather and freshness gate** — spec waves, feasibility findings,
   technical review, canonical handoff references, command contract, repo
   layout; stop if a digest/approval is stale or a required command is unresolved
2. **T1 Understand** — initiative id, wave boundaries, PR granularity from spec
3. **T2 Analyze** — map each wave to concrete files and tests; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs as **MDC notes** / **ADR notes** in the TASK table
4. **T3 Plan** — build REQ/TASK/FILE tables per wave; when TDD contains §4 draft ADRs or feasibility flagged `NEW-ADR`, add a mandatory pre-W0 `TASK-SPEC-ADR-NN` for each draft: promote TDD §4 section → `{adr_dir}/adr-NNN-{slug}.md` with status Accepted, PE name, and date; collect `codebase`/`spec_path`/`verify_command` per TASK
5. **T4 Execute** — write plan; build WorkManifest seed section; run P1–P14 checks; commit to spec branch
6. **T5 Verify** — self-contained plan readable by a fresh session; WorkManifest YAML is valid

## Output

Save to `{reports_dir}/{plan_prefix}-{initiative}.md`.

Use [references/output-template.md](references/output-template.md).

## WorkManifest integration

The plan's final section (§9) emits a ready-to-use WorkManifest YAML stub.

**After spec PR merge** — not before — the dev team seeds the board from §9:

```bash
# One GitHub Issue per wave (W0, W1, …) — primary path
gh issue create --repo {org}/{repo} \
  --title "[{INITIATIVE} W0] {wave goal}" \
  --body-file /tmp/w0-body.md \
  --label "{initiative-label}"
```

One TASK row in the plan maps to work described in the wave issue body.
Wave hierarchy is expressed via `depends_on` in §9 YAML (and GitHub issue links
in issue bodies when seeding manually).

### Engineering board-seed action

This is an external workflow action, not a skill and not part of plan creation.
After spec merge, the engineering agent:

1. confirms the merged plan and P14-valid §9 are current,
2. searches existing issues by initiative + wave id to avoid duplicates,
3. runs `gh auth status`,
4. presents the create/existing issue plan,
5. after explicit developer authorization, creates only missing issues,
6. applies initiative labels and writes dependency links,
7. reports every created/existing issue URL.

Outcomes:

- `seeded` / `already-seeded` → workflow `pass`
- `auth-unavailable` / `partial` → workflow `blocked`
- command/API failure → workflow `failed`

When `gh` is unavailable, print exact commands and do not claim seeding
completed. `/pre-implement` must not start until every expected wave has an
issue.

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md` to the plan.
Use stage `spec-implementation-plan`.

- `pass` → human Gate 2, then authorized spec merge
- `needs-input` / `blocked` → human decision
- `stale` → `initiative-feasibility`
- `failed` → stop

After the spec PR is merged, the workflow selects the engineering-owned
`board-seed` external action. Planning does not seed the board itself.
