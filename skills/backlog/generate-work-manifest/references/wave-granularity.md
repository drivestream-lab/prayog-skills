# Wave granularity — Epic + one task per wave

## When to use

Read PRD **§4.0 Delivery model** (or equivalent). Emit wave tasks when:

| Signal | Action |
|--------|--------|
| `delivery_model: waves` in PRD | **Wave mode** — default for harness / tech-debt INITs |
| PRD §4.5 / Implementation waves table with W0, W1, … | **Wave mode** even if §4.0 missing (infer `waves`) |
| `delivery_model: repo-slice` | Use [v1-granularity.md](v1-granularity.md) — one task per repo |
| Multi-repo product INIT without wave table | **repo-slice** |

**autrio10x:** PRD in `drivestream-meta/prd/INIT-*.md`; policy in `playbook/delivery-model.md`.

---

## Wave manifest shape

```
EPIC (meta / drivestream-meta)
├── W0   structure
├── PRE1 optional gate (from merged repo spec — e.g. unit test matrix)
├── W1   domain
├── W2   …
└── Wn
```

**Rules:**

- Task `id` **equals** wave id from PRD/spec (`W0`, `W1`, `PRE1`, …)
- `depends_on` = sequential wave order from PRD §4.0 or spec wave table
- `repo` = `primary_repo` from PRD (e.g. `abhilekh`) for all implementation waves
- `title` = `[W<N>] <summary>` or `[PRE1] <gate name>`
- `branch_hint` from PRD/spec wave table
- `verify_command` per wave from spec (W0: `make check && make test`; W1+: typically `make test`)
- `spec_path` = `docs/specification/product/INIT-*.md` on implementation repo
- `codebase` = project config option (`abhilekh`, `parichay`, …)

---

## PRE* gates

Merged repo spec may add planning gates not in original PRD (e.g. **PRE1** unit test case matrix before W1).

- Include as manifest task if spec lists it as a board unit
- `depends_on`: prior wave (e.g. `PRE1: [W0]`, `W1: [PRE1]`)
- `verify_command`: `make check` or docs-only `N/A — doc review` when no code
- Eng merges doc PR or attaches matrix under `docs/specification/reports/`

---

## Task body (wave)

```markdown
## Objective

<One paragraph from PRD/spec wave row>

## Deliverables

- [ ] Items from spec wave scope / W0 scope table
- [ ] Wave PR gate: feature map, as-built, overlap audit

## Spec (develop)

- `docs/specification/product/INIT-....md` — wave <id>

## PR

`<branch_hint>` → `develop`

## PRD traceability

- §4.0 delivery_model; §4.5 wave <id>; R4–R8 as applicable
```

---

## Self-check (wave mode)

| Check | Pass if |
|-------|---------|
| Wave coverage | Every PRD/spec wave id has exactly one `work[]` item |
| IDs | Manifest ids match PRD/spec (`W0` not `A1`) |
| Depends | Linear order respects PRD sequencing |
| Fields | Each item has `codebase`, `spec_path`, `verify_command`, `branch_hint` |
| apiVersion | `meta.meta/v1` for autrio10x; `prayog.meta/v1` for drivestream-lab |

---

## Example: INIT-ABHILEKH-001

| id | depends_on | title prefix |
|----|------------|--------------|
| W0 | [] | `[W0]` structure |
| PRE1 | [W0] | `[PRE1]` unit test case matrix |
| W1 | [PRE1] | `[W1]` devices |
| W2 | [W1] | `[W2]` owners / releases |
| … | … | … |
