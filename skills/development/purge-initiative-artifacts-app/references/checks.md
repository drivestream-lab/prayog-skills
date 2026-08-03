# Purge app checks (A1–A6)

| ID | Check | Evidence |
|----|-------|----------|
| A1 | Initiative id resolved | `INIT-*` present |
| A2 | Allowlist only | Every deleted path ∈ app PURGE set for this INIT |
| A3 | KEEP refused | No product INIT, Accepted ADR, or source/test/verify script deleted |
| A4 | Idempotent | Missing allowlisted files recorded as `missing_ok` |
| A5 | Purge note | `Purge-App-{INIT}.md` lists deleted / missing_ok / refused |
| A6 | Handoff | Envelope stage `purge-initiative-artifacts-app` with outcome |

Blocking: A2, A3. A1 missing → `needs-input`.
