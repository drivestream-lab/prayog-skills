# Persistent handoff envelope

Every Prayog stage ends with a handoff block in its durable output artifact.
Chat summaries may repeat it, but chat is not workflow state.

```yaml
handoff:
  contract: sdd-delivery/v2
  stage: initiative-feasibility
  outcome: findings
  artifact:
    path: docs/specification/reports/Initiative-Feasibility-Report-INIT-001.md
    digest: sha256:{hex}
  blockers:
    - F-12
  signals:
    new_adr: true
  next_candidates:
    - spec-technical-review
  human_checkpoint: false
  external_action: false
```

## Required fields

| Field | Meaning |
|-------|---------|
| `contract` | Delivery contract implemented by the producer |
| `stage` | Node id from `workflow.yaml` |
| `outcome` | One of the contract outcomes |
| `artifact.path` | Durable stage output |
| `artifact.digest` | Digest of the output after it is saved |
| `blockers` | Stable finding/question ids that prevent progress |
| `signals` | Stage-specific routing facts; never implicit prose |
| `next_candidates` | Workflow-valid next nodes, not an authorization to execute |
| `human_checkpoint` | Whether a human decision is required next |
| `external_action` | Whether the next transition can mutate GitHub or another system |

Optional future field (not required in v1): `executed_by: manual | orchestrated`
records who ran a skill; it does not change navigation or eligibility.

## Navigation rules

1. Read the latest handoff and the pinned `workflow.yaml`.
2. Verify the handoff contract matches the installed contract.
3. Resolve the transition for the recorded outcome from `workflow.yaml` (SSOT).
4. Explain the next action before executing it.
5. Never auto-transition a `type: human-checkpoint` node. Mechanism is human
   review; `purpose` on the node is intent for display/ops only — not a
   separate node kind (`type: gate` is forbidden).
6. Never perform an external action without explicit authorization.
7. A stale artifact routes to the workflow's stale transition, not the nominal
   next skill.
8. `next_candidates` never authorize invoke and never bypass
   `human_checkpoint: true` or a resolved `type: human-checkpoint` node.
9. **Invocation mode is not an exemption.** Human `/skill` and AgentRunner
   both obey the same pinned workflow + delivery contract + latest handoff.
10. For a resolved `type: skill` node: a human or ad-hoc agent may run the
    skill when preconditions allow. An orchestrator may **auto-dispatch** only
    when `dispatch: orchestrated` (missing `dispatch` → schema default
    `manual`). Read `dispatch` from the pin — do not hardcode skill-id lists.
11. Technical review reports `ready_for_pe_review: true` and
    `ready_for_plan: false` until Accepted TDD/ADR files exist on the spec
    branch. Mid-lane PE acceptance updates files only — not `spec-lgtm`.
12. `/spec-implementation-plan` may run when TDD/ADR files are **Accepted**;
    **`spec-lgtm`** is set only after the plan is on head (Gate 2 unlock).
13. `/pre-implement` and `/loop-spec` require spec PR **merged** with
    `spec-lgtm` on merge head and board-seed complete — not an open Draft spec
    PR branch.
14. ADR signals contain actual file paths/digests; target paths or future
    promotion tasks are not artifacts.

## Outcome vocabulary

- `pass` — stage criteria are satisfied.
- `findings` — durable findings require a workflow-defined resolution path.
- `needs-input` — required information is unavailable.
- `blocked` — an explicit gate prevents progress.
- `stale` — an upstream artifact or approval no longer matches.
- `failed` — execution or verification failed.
- `skipped` — stage is legitimately inapplicable with a recorded reason.

Stage-specific statuses such as `PR READY`, `approved`, or `partial` belong
under `signals`; they map to one of the standard outcomes.
