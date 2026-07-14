# Technical review checks (T1–T11)

Run every check. PASS = zero findings. SKIPPED = missing input (state reason).

Governance and routing detail: [governance.md](governance.md).

| ID | Check | Evidence required |
|----|-------|-------------------|
| T1 | **Module / package boundaries** | Each affected module named; inputs and outputs of each boundary stated; no ambiguity about which layer owns what |
| T2 | **Public interface contracts** | For each module boundary, the method names, argument shapes (types described in engineering terms, not language syntax), return shapes, and invariants are specified |
| T3 | **NEW-ADR dispositions** | Every `NEW-ADR` maps to exactly one `ADR_REQUIRED` Draft file, `TDD_ONLY` rationale, or `DEFERRED_WITH_DEFAULT` risk/default/revisit trigger |
| T4 | **Test policy** | Unit / integration / live-verify boundary documented per module; golden test strategy named (exact match vs fuzzy vs snapshot); AI-output determinism policy stated where applicable |
| T5 | **Error handling strategy** | Failure modes named for each module; propagation path to caller stated; which failures are recoverable vs terminal; how errors surface at the CLI/API boundary |
| T6 | **Observability contract** | What is logged at which level for each module; which fields appear in structured output (correlation IDs, domain IDs); no silent swallowing of errors |
| T7 | **Data contract ownership** | Schema ownership named (who defines, who validates, which layer); validation points stated (edge vs internal); versioning policy if schema evolves |
| T8 | **Dependency graph integrity** | No circular dependencies introduced; no ADR violations; import layer order consistent with `rules_glob` layering constraints |
| T9 | **Engineering questions — zero PE-lane items unresolved** | All items routed to PE lane are resolved or deferred with defaults; PM/domain items explicitly listed as out-of-scope for this review |
| T10 | **PE review readiness** | Package explicitly requires PE review, lists the exact TDD + ADR files to review, reports `ready_for_pe_review`, and does not claim approval or planning readiness |
| T11 | **ADR artifact integrity** | Every `ADR_REQUIRED` file exists under `{adr_dir}`, is Draft, links the feasibility finding/TDD, contains context/options/recommendation/consequences/revisit triggers, and is linked with digest from TDD/handoff |

Severity: **Blocking** (PE cannot sign off until resolved), **Should fix**, **Verify**.

**Blocking** when: T3 has an unresolved NEW-ADR with no disposition/default; T9
has PE-lane items pending; T2 is missing for a crossed boundary; or T11 finds a
missing/broken/duplicate ADR file or embedded ADR content without its required
canonical file.
