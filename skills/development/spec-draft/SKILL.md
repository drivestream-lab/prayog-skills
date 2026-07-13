---
name: spec-draft
description: >-
  Translate the PRD into a spec slice for this repo. Reads the PRD from the
  meta PRD PR branch or merged develop, extracts capabilities relevant to this
  repo, drafts docs/specification/product/INIT-*.md locally, and produces a
  Draft-PR readiness handoff. After explicit user authorization, the agent may
  use gh to create/update the Draft spec PR and initialize Gate 2 labels. Run
  after Gate 1 approval and before /initiative-feasibility.
disable-model-invocation: true
paths: AGENTS.md, docs/specification/**, .cursor/rules/**
background_eligible: true
background_trigger: "Gate 1 approved for this repo scope; spec slice not yet on a Draft spec PR"
---

# Spec draft

Translate the **PRD** into a **spec slice** for this repo. The spec slice is
the engineering team's interpretation of what the PRD means for their codebase.

**Do not implement.** Produce `docs/specification/product/INIT-{id}.md` only.

## Why this skill exists

PM writes PRD in feature language. Engineers own the spec.
This skill bridges the gap — it reads the PRD and drafts structured spec FRs
that the dev team can review, edit, and then run `/initiative-feasibility` on.

## NON-NEGOTIABLE

1. The spec draft is a **starting point** — dev must review and edit before
   committing. Do not present it as authoritative without dev review.
2. Language in the spec must be **engineering terms** — FRs, acceptance criteria,
   module scope — not copied PRD user-story language.
3. Scope must be **bounded to this repo** only. Do not write FRs for other repos.
4. Every FR must trace to a named section or bullet in the PRD.
5. Flag anything in the PRD that is **ambiguous for this repo** — do not guess.
   Put ambiguities in a "Spec questions" section at the bottom.
6. **Handoff gate first.** The canonical impact-map artifact, source PRD
   digest, current meta PR head SHA, and tech-lead APPROVED review must match.
   A label or old LGTM alone is not approval.
7. This repo must be `affected` in the latest map and not deferred or blocked.
   Record the repo's `scope_digest` in the spec. If any gate fails: stop.
8. **No GitHub side effects during generation.** Do not create a branch,
   commit, push, PR, comment, review request, or label until the completed
   PR-readiness handoff is shown and the user explicitly authorizes PR action.
9. Treat `spec-*` labels as projections. If artifact, review, and label
   disagree, the gate is closed. Exactly one PE gate label may be active:
   `spec-pending`, `spec-lgtm`, or `spec-blocked`. `spec-revised` and
   `spec-stale` are additional invalidation labels and always close the gate.

## Prerequisites

- Meta PRD PR exists (merged or open) with a committed
  `prd/reports/Impact-Map-{INIT}.md`
- Latest tech-lead APPROVED review is bound to the current meta PR head SHA
  carrying that map revision and PRD digest
- This repo is affected in that revision and has a `scope_digest`
- An existing Draft spec PR is optional when revising; it is not required to
  start `/spec-draft`

## Inputs

Resolve paths from `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md).

1. **PRD** — (REQUIRED) from `<client>-meta/prd/INIT-*.md`. Read from the meta
   PRD PR branch or merged `develop`. Do not assume PRD is on develop if PR is
   still open — use PR branch when iterating in parallel.
2. **Impact map** — (REQUIRED) canonical
   `<client>-meta/prd/reports/Impact-Map-{INIT}.md` from the exact approved meta
   PR head; PR comments are summaries only.
3. **Approval evidence** — (REQUIRED) meta PR number/URL, current head SHA, and
   latest tech-lead APPROVED review `commit_id`; all must match.
4. **As-built** — `implementation-status.md` (REQUIRED) — understand what
   already exists before writing FRs.
5. **Source** — `source_roots` from profile — understand current module structure.
6. **Service profile** — `docs/specification/product/00-service-profile.md` if
   it exists — understand the repo's existing domain.
7. **`adr_dir`** — existing ADRs constrain what this spec can propose.
8. **Layout** — `.harness/profile.yaml` or [references/layout-defaults.md](references/layout-defaults.md)

## Process

1. **T0 Gather and gate** — PRD, canonical impact map, approval review, as-built,
   source, service profile. Verify:
   - current meta PR head SHA = approved review `commit_id`
   - impact-map `source_prd_digest` = digest of the PRD read
   - impact-map revision/path = approval attestation
   - this repo is affected, not deferred/blocked, with a `scope_digest`
   Stop on any mismatch.
2. **T1 Understand** — initiative id; approved map revision and scope digest;
   what capabilities land in this repo; what already exists (as-built + source scan)
3. **T2 Scope** — list ONLY what this repo owns. Explicitly exclude what belongs
   to other repos. Cross-service contracts are noted but not spec'd here.
4. **T3 Draft** — write INIT-*.md using [references/output-template.md](references/output-template.md)
5. **T4 Flag** — list ambiguities, open questions, and anything that needs PM
   confirmation (route to meta PRD PR — see feasibility skill)
6. **T5 Verify and hand off** — run D1–D12 from
   [references/checks.md](references/checks.md); present in chat:
   - generated/changed files,
   - gate verification summary,
   - spec summary and open questions,
   - proposed branch, base, Draft PR title/body, reviewers, and initial labels,
   - `PR READY` or `PR BLOCKED` verdict.
   Stop without GitHub side effects.

## PR creation handoff

After T5, **always** present the PR readiness section from
[references/output-template.md](references/output-template.md) and ask the user
whether to create or update the Draft spec PR.

If the user explicitly authorizes it and `gh` is configured, the agent may:

1. create/switch to the proposed branch when needed,
2. commit the approved spec file(s),
3. push the branch,
4. create or update the **Draft** spec PR,
5. verify Gate 2 labels provisioned by Launchpad are present; if missing, stop
   and instruct the user to run
   `launchpad apply-gates --repo <name> --apply`,
6. apply `spec-pending` and remove obsolete Gate 2 labels through GitHub REST
   issue-label endpoints (do not use `gh pr edit`),
7. verify the PE team exists and has repository access,
8. request PE review through GitHub REST
   `POST repos/{owner}/{repo}/pulls/{number}/requested_reviewers` with the team
   slug, then verify the request is present.

This is a separate, user-authorized agent action—not an automatic side effect
of `/spec-draft`.

If `gh` is not configured, provide exact manual commands and do not report that
the PR exists.

## Output

Draft saved to `{product_spec_dir}/INIT-{id}.md` (from profile).

Use [references/output-template.md](references/output-template.md).

Before PR creation, `spec_pr` and Gate 2 fields are `pending`. After the
user-authorized PR action, the PR body contains the spec summary, artifact path,
meta handoff digests, Gate 2 checklist, and PE review request.

## Revision handling

When a newer approved impact-map revision appears:

- Same repo `scope_digest`: record the new revision check; existing spec may
  continue if its PRD digest is unchanged.
- Changed `scope_digest`: mark this spec stale, revise affected sections, and
  re-run `/initiative-feasibility`.
- Repo removed/deferred/blocked: stop and mark the spec PR held or out of scope.
- Dependency/order-only change: update cross-service dependencies and invalidate
  the implementation plan when ordering changes.

## Next step

After dev reviews the local draft:

1. authorize Draft spec PR creation when the PR-readiness verdict is `PR READY`
2. commit the spec slice to the Draft spec PR branch (during authorized PR action
   or immediately after)
3. run `/initiative-feasibility` on the committed spec on that branch

Do not skip the PR-readiness handoff or jump straight to feasibility on a local
file only — the Draft spec PR is the engineering review surface for the whole
lane.

## Workflow handoff

Append the envelope from `../../../references/handoff-envelope.md` to the saved
spec. Use stage `spec-draft`.

- `pass` → `initiative-feasibility`
- `needs-input` / `blocked` → human decision
- `stale` → `prd-impact-map`
- `failed` → stop

Record D-check findings and source freshness under blockers/signals.
