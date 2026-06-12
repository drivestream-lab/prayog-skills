# Feasibility checks (F1–F12)

Run every check. PASS = zero findings. SKIPPED = missing input (state reason).

| ID | Check | Evidence required |
|----|-------|-------------------|
| F1 | **Baseline snapshot** | Current tests layout, pytest config, verify inventory, as-built state |
| F2 | **Spec → service map** | Each spec capability/wave maps to `src/` module or SKIPPED if N/A |
| F3 | **Spec → verify map** | Named verify scripts exist; aggregator list matches if spec claims it |
| F4 | **Spec → unit map** | Planned unit areas vs existing `tests/unit/` |
| F5 | **As-built drift** | Spec claims vs `implementation-status.md` rows |
| F6 | **Docs drift** | `tests/README.md`, `AGENTS.md`, rules vs spec (e.g. anti-unit README) |
| F7 | **Overlap risk** | Same HTTP journey in unit and verify for same capability |
| F8 | **CI vs live boundary** | What runs in CI vs closure/live verify per spec and README |
| F9 | **Cross-service touch** | Integration specs / contracts referenced and files exist |
| F10 | **Assumptions** | Spec asserts facts not evidenced in repo |
| F11 | **Effort drivers** | Per wave: complexity drivers (not hour estimates) |
| F12 | **PM questions** | All blocking gaps have a numbered question |

Severity: **Critical** (blocks merge), **Should fix**, **Verify**, **Gap** (informational).
