# ID conventions (SSOT)

Stable identifiers across PM and development skills. Every skill that assigns
or cites an id MUST follow this vocabulary. Check ids (rule numbers) are
**not** entity primary keys.

See also: [artifact-write-contract.md](artifact-write-contract.md).

## Namespaces

| Namespace | Purpose | Stable across revisions? |
|-----------|---------|--------------------------|
| **Product** | What we want (PRD / spec) | Yes — never recycle |
| **Process** | What an audit/review produced | Yes within a report revision chain |
| **Delivery** | How we execute (plan / board) | Yes for the initiative |
| **Checks** | Which rule fired | Stage-local documentation only |

---

## Product ids

| Kind | Shape | Lives in | Meaning |
|------|-------|----------|---------|
| Capability | `CAP-{nn}` | PRD | User/product capability (PM language) |
| Requirement | `REQ-{nn}` | PRD + spec | Testable requirement (**canonical**) |
| Contract | `CTR-{nn}` | Impact map / spec | Cross-repo interface |
| Open question | `OQ-{nn}` | PRD (or resolution → PRD) | Unresolved product decision |

**`REQ-*` is canonical.** Spec tables may show `FR-{nn}` only as a **display
alias** for the same number (`FR-05` ≡ `REQ-05`). New artifacts use `REQ-*`.
Legacy PRDs/specs that only have `FR-*` remain valid until next edit — do not
renumber; map `FR-n` → `REQ-n` when touching the row.

Trace rule:

```text
CAP-03 ──covers──▶ REQ-07, REQ-08
REQ-07 ──cited by──▶ impact scope, spec row, plan TASK, ground-spec row
```

---

## Process ids

| Kind | Shape | Producer | Meaning |
|------|-------|----------|---------|
| Validation finding | `VF-{nn}` | `validate-requirements` | One finding instance |
| Feasibility finding | `FF-{nn}` | `initiative-feasibility` | One feasibility finding |
| Ground finding | `GF-{nn}` | `ground-spec` | One grounding discrepancy |
| Change to apply | `CHG-{nn}` | `review-findings` / `update-documents` | Approved edit unit |
| Product question (PE) | `PQ-{nn}` | engg-reviews | PE question on Meta PR (optional pack) |

Rules:

- Validation tables use **`VF-01`**, never bare `# 1` as the primary key.
- Incremental re-validation: surviving findings **keep the same `VF-*`**;
  tag `(carried from …)`. Resolved findings stay under `## Resolved` with the
  same id.
- Resolution and `update-documents` link **`VF-*` → `CHG-*`**.
- Feasibility handoff blockers use **`FF-*`**, never bare `F-12` (conflicts
  with check id `F12` and looks like an FR).
- Grounding discrepancies use **`GF-*`**. Do **not** reuse feasibility-owned
  `FF-*` for new grounding findings.
- Spec open engineering questions stay **`Q-{n}`** in the spec file; PRD open
  questions use **`OQ-*`**. Do not mix registries.

---

## Delivery ids

| Kind | Shape | Meaning |
|------|-------|---------|
| Initiative | `INIT-…` | Programme initiative |
| Epic / parent | `EPIC` (WorkManifest) / board parent | Board root (call Epic or Feature in titles — one word per programme) |
| Wave | `W{n}` | Sign-off / merge boundary (`W0`, `W1`, …) |
| Task | `TASK-W{n}-{nn}` | Executable unit |
| File / Test | `FILE-…` / `TEST-…` | Plan-only helpers |

Plan tasks **implement** product requirements:

```text
TASK-W0-01 ──implements──▶ REQ-07, REQ-08
```

Do **not** invent shadow product ids like wave-scoped `REQ-W{n}`. Wave-scoped requirement
buckets in plans are removed; cite `REQ-*` directly.

Board linkage (minimum): EPIC → wave issues; each wave body lists `TASK-*`
with done-when. Sub-issues per TASK are optional; ids in the body are
mandatory for traceability.

---

## Check ids (not entities)

Stage-local rule numbers stay as documentation of which check fired:

| Stage | Examples |
|-------|----------|
| validate-requirements | `1`…`11`, `S1`…`S4` |
| initiative-feasibility | `F1`…`F14` |
| spec-technical-review | `T1`…`T12` |
| spec-implementation-plan | `P1`…`P16` |
| ground-spec | `G1`…`G10` |
| create-board-tickets (forge) | `B1`…`B8` |
| learning-extract | `L-01`…`L-{nn}` |
| engg-reviews | `C0`…`C12` |

Cite the check on a finding (`VF-04`, Check `7`) — never use the check number
alone as a handoff blocker.

---

## Handoff blockers

`handoff.blockers` MUST use stable process or delivery ids, for example:

- `VF-03`, `VF-11`
- `FF-02`
- `GF-01` (ground findings from `ground-spec`)
- `L-01`
- `OQ-04`
- `TASK-W0-03`

Not: `1`, `F-12`, `Critical #2`, free-text sentences.

---

## Coherence bar

1. Product ids (`CAP`, `REQ`, `CTR`, `OQ`) are assigned once and never recycled.
2. Process ids (`VF`, `FF`, `GF`, `CHG`) are stable within a canonical report
   file’s revision chain.
3. Delivery ids (`W`, `TASK`) never rename product ids.
4. Check ids document which rule fired — not primary keys.
