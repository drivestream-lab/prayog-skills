# Technical review checks (T1–T10)

Run every check. PASS = zero findings. SKIPPED = missing input (state reason).

Governance and routing detail: [governance.md](governance.md).

| ID | Check | Evidence required |
|----|-------|-------------------|
| T1 | **Module / package boundaries** | Each affected module named; inputs and outputs of each boundary stated; no ambiguity about which layer owns what |
| T2 | **Public interface contracts** | For each module boundary, the method names, argument shapes (types described in engineering terms, not language syntax), return shapes, and invariants are specified |
| T3 | **NEW-ADR resolutions** | Every `NEW-ADR` item from the feasibility report has either a draft ADR with recommended option, or an explicit defer entry with a default assumption and named risk |
| T4 | **Test policy** | Unit / integration / live-verify boundary documented per module; golden test strategy named (exact match vs fuzzy vs snapshot); AI-output determinism policy stated where applicable |
| T5 | **Error handling strategy** | Failure modes named for each module; propagation path to caller stated; which failures are recoverable vs terminal; how errors surface at the CLI/API boundary |
| T6 | **Observability contract** | What is logged at which level for each module; which fields appear in structured output (correlation IDs, domain IDs); no silent swallowing of errors |
| T7 | **Data contract ownership** | Schema ownership named (who defines, who validates, which layer); validation points stated (edge vs internal); versioning policy if schema evolves |
| T8 | **Dependency graph integrity** | No circular dependencies introduced; no ADR violations; import layer order consistent with `rules_glob` layering constraints |
| T9 | **Engineering questions — zero PE-lane items unresolved** | All items routed to PE lane are resolved or deferred with defaults; PM/domain items explicitly listed as out-of-scope for this review |
| T10 | **PE sign-off gate** | Document explicitly marks human PE review as required; states what a PE approver must check; does not self-approve |
| T11 | **ADR promotion path** | Each TDD §4 draft ADR states how it will reach `{adr_dir}` — either via a `/spec-implementation-plan` `TASK-SPEC-ADR-NN` or an explicit human step; both options are valid; absence of any promotion path is a finding |

Severity: **Blocking** (PE cannot sign off until resolved), **Should fix**, **Verify**.

**Blocking** when: T3 has an unresolved NEW-ADR with no default; T9 has PE-lane
items still pending a decision; T2 is missing for a boundary that implementation
will cross; T11 has no promotion path documented for any draft ADR.
