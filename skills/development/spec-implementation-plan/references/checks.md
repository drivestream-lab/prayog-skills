# Plan checks (P1–P12)

Governance detail: [governance.md](governance.md).

| ID | Check |
|----|-------|
| P1 | Every spec wave/section has ≥1 REQ row |
| P2 | Every REQ has ≥1 TASK |
| P3 | Every TASK has FILE paths or explicit "docs only" |
| P4 | Every TASK has **done when** (observable) |
| P5 | Test TASKs name unit target and/or live-verify artifact + command from profile toolchain |
| P6 | No product scope beyond initiative spec |
| P7 | Feasibility blockers addressed or explicitly deferred |
| P8 | Wave order and dependencies documented |
| P9 | As-built / README updates listed in same PR as code tasks |
| P10 | Plan is self-contained (fresh agent can execute one wave) |
| P11 | **MDC conformance** — per `rules_glob`; discrepancies in TASK **MDC notes** and RISK table |
| P12 | **ADR conformance** — architectural TASKs cite ADR id or `NEW-ADR`; draft-ADR TASK in same or earlier wave when required; discrepancies in TASK **ADR notes** and RISK table |
| P13 | **Technical design reference** — §0 present; technical review path populated or explicitly N/A with reason; PE sign-off status stated |
| P14 | **WorkManifest seed** — §8 present; wave IDs (`W0`, `W1`, …) match plan waves exactly; every TASK row has `codebase`, `spec_path`, and `verify_command`; YAML is syntactically valid |
