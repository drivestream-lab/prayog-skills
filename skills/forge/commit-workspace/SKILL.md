---
name: commit-workspace
description: >-
  Publish includable workspace changes to the remote head for this run (human
  walker Forge tooling). Use after a content skill when pin forge.commit_workspace
  is optional or required. Orchestrators use ForgeClient instead — do not
  auto-invoke this skill.
disable-model-invocation: true
---

# Commit workspace

Human-walker equivalent of Gateflow `ForgeClient` **commit workspace**
(`forge.action` / pin field: `commit_workspace`).

## NON-NEGOTIABLE

1. Read pinned `workflow.yaml` for the **content** stage that just completed
   (`forge.commit_workspace`). Do not invent policy.
2. Bind the remote head from run / human context (wave PR, meta PR, spec
   branch) — not from a pin `head` enum.
3. If policy is `disabled`, stop and explain; do not publish.
4. If policy is `required` and there is nothing includable to publish, fail
   closed.
5. If policy is `optional` and the tree is clean, report success with no-op.
6. Never apply approval labels (`*-lgtm`).
7. Use available Forge tooling in this environment (git remote APIs, `gh`, …)
   as examples — tool-neutral. Do not assume a specific CLI exists.

## Inputs

1. Latest content-skill `handoff:` (artifact and/or `handoff_path` baton)
2. Pinned root `workflow.yaml`
3. Workspace root with includable changes

## Process

1. Resolve prior stage + `commit_workspace` policy from the pin.
2. Determine includable paths (respect `.gitignore` / harness norms).
3. Publish to the bound head when policy allows.
4. Emit a short durable note + `handoff:` for this forge step (stage
   `commit-workspace`).

## Workflow handoff

1. Append/emit the envelope from `../../../references/handoff-envelope.md`.
   Stage id: `commit-workspace`. Prefer `outcome: pass` when publish or
   justified no-op succeeded.
2. When `handoff_path` is bound, **overwrite** that baton with the same
   envelope.
3. Forge skills are **not** workflow graph nodes — do not invent
   `next_candidates` from a missing pin node. If continuing the programme,
   re-read the **content** stage handoff and pinned transitions.
