# Checks — prd-codebase-map

Never skip a check. Mark SKIPPED with reason.

| ID | Check | Pass criteria |
|----|-------|---------------|
| C0 | **Provider ready** | Fleet graphs for required repos are CURRENT (or explicit degraded mode authorized) |
| C1 | **PRD identity** | Initiative id, PRD path, `source_prd_digest`, meta PR head SHA (if PR open) recorded |
| C2 | **Candidate set** | Every mapped repo listed with path, `develop_sha`, `graph_digest` |
| C3 | **Capability coverage** | Every in-scope PRD capability/feature has a matrix row |
| C4 | **Evidence honesty** | Rows claiming `exists`/`partial`/`conflict` cite EXTRACTED evidence or as-built; INFERRED-only cannot alone justify `exists` |
| C5 | **As-built read** | As-built opened per repo when file exists; missing as-built noted |
| C6 | **Delta taxonomy** | Every row uses exactly one of: exists / partial / absent / conflict / unknown |
| C7 | **Question quality** | Each product question has scenario, example, recommendation, why, alternatives, evidence |
| C8 | **Question cap** | Open questions ≤ cap (default 10) unless PE documented raise |
| C9 | **Product language** | Questions avoid module/ADR/implement jargon; eng detail only in appendix |
| C10 | **Gate isolation** | No gate label mutations; handoff `gate_coupled: false`; no sdd-delivery next_candidates |
| C11 | **Revision discipline** | `map_revision` incremented when prior map exists; change_reason set |
| C12 | **Artifact dual output** | Chat summary + saved `PRD-Codebase-Map-{INIT}.md` + digest |

## Severity guidance for questions

| Delta | Default |
|-------|---------|
| `conflict` | Must ask (blocking product clarity) |
| `partial` | Should ask if acceptance criteria ambiguous |
| `unknown` | Ask only if high user impact |
| `exists` | Optional confirm if PRD still lists as new work |
| `absent` | Matrix only unless scope split unclear |
