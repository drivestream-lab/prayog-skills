# ID map (orientation)

Procedure and field SSOTs:

| Doc | Role |
|-----|------|
| [`../references/id-conventions.md`](../references/id-conventions.md) | Product / process / delivery ids (**mint-only-if-consumed**) |
| [`../references/quality-confidence-ladder.md`](../references/quality-confidence-ladder.md) | Unit / capability / journey prove |
| [`../references/artifact-write-contract.md`](../references/artifact-write-contract.md) | Canonical paths; H1–H4; no `*-revN` siblings |
| [`../references/handoff-envelope.md`](../references/handoff-envelope.md) | Persistent handoff; blockers use stable ids |

## Quick map (current pin)

```text
PRD CAP-* / J-* / REQ-* / OQ-* / CTR-*
  → validate VF-*
  → review CHG-* (linked to VF-*)
  → update PRD
  → impact map (Impact-Map-{INIT}.md) + IM-* (Blocking:yes → Gate 1 closed)
  → engg-reviews PQ-* (PE→PM on Meta PR) when code map needs product clarify
  → prd-impact-acceptance → merge
  → spec carries CAP-* / J-* / REQ-* ; spec Q-* (engineering only)
  → plan TASK-* implements REQ-* ; live covers CAP-* and/or J-* + fixtures
  → coding-readiness → spec merge
  → board EPIC → W* (TASK table in wave body)
  → Pass-1: pre-implement → loop-spec (TASK-*) → wave-acceptance
       (scripted prove and/or human_observations; ack = wave-accepted)
  → Pass-2: learning-extract (L-*) → ground-spec (REQ + CAP/J evidence)
  → wave-signoff (merge only)
```

## Question namespaces (do not mix)

| Id | Meaning |
|----|---------|
| `OQ-*` | Open **product** question in the PRD |
| `IM-*` | **Impact** / programme / Gate-1 question |
| `PQ-*` | **Product** question PE→PM after code evidence |
| `Q-*` | **Spec** engineering question |

## Defaults

- Prove keys: **`CAP-*`** (capability rung) and **`J-{nn}`** (journey rung); `REQ-*` on TASK/unit  
- Board: TASK ids in **wave issue body**  
- Learning: **`L-*`** in Learning-Extract artifact  
- PM/dev reports: **overwrite** canonical paths only  
