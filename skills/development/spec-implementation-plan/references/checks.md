# Plan checks (P1–P14)

Governance detail: [governance.md](governance.md).

Before P1, verify the template's **Source freshness and command contract**
table. Any STALE source or MISSING required command fails the plan; do not run
P1–P14 against obsolete inputs.

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
| P10 | Plan is self-contained (fresh agent can execute one wave); source digests/revisions and canonical check/test/verify/ground commands are populated |
| P11 | **MDC conformance** — per `rules_glob`; discrepancies in TASK **MDC notes** and RISK table |
| P12 | **ADR conformance** — architectural TASKs cite ADR id or `NEW-ADR`; when NEW-ADR findings exist, a pre-W0 `TASK-SPEC-ADR-NN` must promote each TDD §4 draft to a file at `{adr_dir}/adr-NNN-{slug}.md` with status Accepted; §0 "Resolved ADRs" must link to `adr_dir` file paths, not TDD section refs; discrepancies in TASK **ADR notes** and RISK table. **FAIL** if NEW-ADR findings exist but no `adr_dir` file is created or planned. |
| P13 | **Technical design reference** — §0 present; technical review path populated or explicitly N/A with reason; PE sign-off status stated as `[x] complete — {date}` (not `[ ] required`) when TDD was produced; **FAIL** if TDD Status field in `Technical-Review-{initiative}.md` still reads `Draft` — this means the dev has not committed the post-Approve TDD status update and the plan must not proceed |
| P14 | **WorkManifest seed** — §9 present; wave IDs (`W0`, `W1`, …) match plan waves exactly; every TASK row has `codebase`, `spec_path`, and `verify_command`; YAML is syntactically valid |
