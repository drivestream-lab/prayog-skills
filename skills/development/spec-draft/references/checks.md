# Spec draft checks (D1–D12)

Run every check. PASS means zero findings. SKIPPED requires a missing input and
an explicit reason; a check that is not applicable should PASS with the
applicability rationale. D1, D2, D3, D4, D7, and D11 are blocking.

| ID | Check | Evidence required |
|----|-------|-------------------|
| D1 | **Approved handoff is current** | Canonical impact-map path/revision, PRD digest, current meta PR head SHA, and matching tech-lead APPROVED review; repo is affected and not deferred/blocked |
| D2 | **Complete PRD traceability** | Every in-scope PRD capability maps to at least one FR; every FR cites a named PRD section/bullet |
| D3 | **Repo-bounded scope** | In-scope, out-of-scope, deferred, and other-repo responsibilities agree with the approved repo scope digest |
| D4 | **Observable acceptance** | Every FR has externally observable done criteria and names the evidence type that can prove it |
| D5 | **Negative and failure paths** | Error, empty, unavailable, timeout, authorization, retry/idempotency, and partial-success behavior are specified or N/A with reason |
| D6 | **Assumptions and questions** | Every assumption has evidence/status; every question has lane, owner, blocking, required-by stage, default-if-deferred, and resolution link/status |
| D7 | **Cross-repository contracts** | Every boundary has contract ID, provider/consumer owner, entry point, input/output shape, invariants, errors, compatibility/versioning, and contract-test location; PASS with “no cross-repo boundary” when none |
| D8 | **NFR applicability** | Security, reliability, performance, observability, privacy, migration, rollback, and operations are specified or N/A with reason |
| D9 | **As-built alignment** | Proposed changes distinguish existing, changed, and new behavior using as-built/source evidence |
| D10 | **Dependency order** | Consumed contracts and dependency/build order agree with the approved impact map; discrepancies are blocking questions |
| D11 | **Zero unresolved blockers** | No open blocking PM, PE, or domain question remains; safe defaults are explicit only for non-blocking deferrals |
| D12 | **Output completeness** | Required header references, tables, check summary, PR readiness handoff, and explicit dev-review status are present with no placeholders presented as facts |

## Verdict

- **PASS:** D1–D12 pass and no blocking question remains.
- **FAIL:** any blocking check fails or any blocking question remains.
- **NEEDS INPUT:** a required handoff/source input is missing; do not draft or
  advance to feasibility.
