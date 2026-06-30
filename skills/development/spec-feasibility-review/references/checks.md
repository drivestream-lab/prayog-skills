# Feasibility checks (F1–F14)

Run every check. PASS = zero findings. SKIPPED = missing input (state reason).

Governance detail: [../references/governance.md](../references/governance.md).

| ID | Check | Evidence required |
|----|-------|-------------------|
| F1 | **Baseline snapshot** | Current test layout, toolchain config, live-verify inventory, as-built state |
| F2 | **Spec → code map** | Each spec capability/wave maps to a module under `source_roots` or SKIPPED if N/A |
| F3 | **Spec → verify map** | Named live-verify artifacts exist; aggregator list matches if spec claims it |
| F4 | **Spec → unit map** | Planned unit areas vs existing `unit_tests_dir` |
| F5 | **As-built drift** | Spec claims vs `implementation-status.md` rows |
| F6 | **Docs drift** | `tests_readme`, `AGENTS.md`, `rules_glob`, `adr_dir` index vs spec |
| F7 | **Overlap risk** | Same user journey in unit and live-verify for same capability |
| F8 | **CI vs live boundary** | What runs in CI vs closure/live verify per spec and tests_readme |
| F9 | **Cross-service touch** | Integration specs / contracts referenced and files exist |
| F10 | **Assumptions** | Spec asserts facts not evidenced in repo |
| F11 | **Effort drivers** | Per wave: complexity drivers (not hour estimates) |
| F12 | **PM questions** | All blocking gaps have a numbered question |
| F13 | **ADR conformance** | Relevant Accepted ADRs cited; spec does not contradict ADR; `NEW-ADR` flagged when initiative needs an undocumented decision |
| F14 | **MDC conformance** | Spec wording does not conflict with `rules_glob` patterns; discrepancies listed in findings |

Severity: **Critical** (blocks merge), **Should fix**, **Verify**, **Gap** (informational).

**Critical** for F13 when spec contradicts an Accepted ADR.
