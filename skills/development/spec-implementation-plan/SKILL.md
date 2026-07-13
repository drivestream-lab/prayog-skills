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
  background_trigger: "spec PR branch: Accepted TDD/ADRs on head when required; spec-pending"
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
10. Commit the plan to the **same Draft spec PR**. Gate 2 label stays
    **`spec-pending`**. After T5, present the **Gate 2 unlock checklist** from
    the output template so PE knows when to set `spec-lgtm`.

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

Run **while the Draft spec PR is open**, **before spec merge**, after:
- Feasibility accepted (no blocking PM questions on meta PRD PR)
- `/spec-technical-review` completed when feasibility had NEW-ADR or PE-lane items
- **`technical-review-approval` satisfied in files** — TDD `Status: Accepted`
  and every required ADR file in `{adr_dir}` is `Accepted` on the current head
- All upstream source digests and approval references are CURRENT

> **Artifact gate vs GitHub gate**
> Planning requires **Accepted TDD/ADR files** (P12/P13). It does **not**
> require `spec-lgtm`. PE sets **`spec-lgtm` + GitHub Approve + attestation**
> only after this plan is committed — that unlocks merge and board-seed.

## Process

1. **T0 Gather and freshness gate** — spec waves, feasibility findings,
   technical review, canonical handoff references, command contract, repo
   layout; stop if a digest/approval is stale or a required command is unresolved
2. **T1 Understand** — initiative id, wave boundaries, PR granularity from spec
3. **T2 Analyze** — map each wave to concrete files and tests; cross-reference `rules_glob` and relevant ADRs; flag spec wording that conflicts with MDC patterns or Accepted ADRs as **MDC notes** / **ADR notes** in the TASK table
4. **T3 Plan** — build REQ/TASK/FILE tables per wave; verify every TDD §4
   `ADR_REQUIRED` row links an **Accepted** file in `{adr_dir}` (created by
   `/spec-technical-review`, accepted during PE review — do not add promotion
   tasks); cite those ADR ids in TASK **ADR notes**; collect
   `codebase`/`spec_path`/`verify_command` per TASK
5. **T4 Execute** — write plan; build WorkManifest seed section; run P1–P14 checks; commit to spec branch
6. **T5 Verify** — self-contained plan readable by a fresh session; WorkManifest YAML is valid; present Gate 2 unlock checklist (§10) in chat for PE

## Output

Save to `{reports_dir}/{plan_prefix}-{initiative}.md`.

Use [references/output-template.md](references/output-template.md).

## WorkManifest integration

The plan's final section (§9) emits a ready-to-use WorkManifest YAML stub.

**After spec PR merge** — not before — run **`/board-seed`** (development lane,
stack-agnostic). That skill reads §9, governance board binding from read-only
meta, creates EPIC + wave sub-issues on the programme Project, and hands off to
`/pre-implement`.

When authoring §9, set `target.org` and `target.project` from governance
(`project_board.name` in `{meta_repo}/config/governance-*.yaml`). Do not invent
board names.

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md` to the plan.
Use stage `spec-implementation-plan`.

- `pass` → human Gate 2, then authorized spec merge
- `needs-input` / `blocked` → human decision
- `stale` → `initiative-feasibility`
- `failed` → stop

After the spec PR is merged, the workflow selects the engineering-owned
`board-seed` external action. Planning does not seed the board itself.
