# Plan checks (P1–P15)

Governance detail: [governance.md](governance.md).

Before P1, verify the template's **Source freshness and command contract**
table. Any STALE source or MISSING required command fails the plan; do not run
P1–P15 against obsolete inputs.

| ID | Check |
|----|-------|
| P1 | Every product `REQ-*` in scope for this plan appears in §1; every wave that implements work cites those REQs via TASK **Implements** |
| P2 | Every in-scope `REQ-*` has ≥1 TASK; every TASK **Implements** ≥1 `REQ-*` (no shadow `REQ-W*`) |
| P3 | Every TASK has FILE paths or explicit "docs only" |
| P4 | Every TASK has **done when** (observable) |
| P5 | Test TASKs name unit target and/or live-verify artifact + command from profile toolchain |
| P6 | No product scope beyond initiative spec |
| P7 | Feasibility blockers addressed or explicitly deferred |
| P8 | Wave order and dependencies documented |
| P9 | As-built / README updates listed in same PR as code tasks |
| P10 | Plan is self-contained (fresh agent can execute one wave); source digests/revisions and canonical check/test/verify/ground commands are populated |
| P11 | **MDC conformance** — per `rules_glob`; discrepancies in TASK **MDC notes** and RISK table |
| P12 | **ADR conformance** — architectural TASKs cite Accepted ADR id from `{adr_dir}`; §0 "Resolved ADRs" links every TDD §4 `ADR_REQUIRED` file path with `Status: Accepted`; discrepancies in TASK **ADR notes** and RISK table. **FAIL** if any required ADR file is missing, still `Draft`, or only referenced from TDD §4 without a canonical `{adr_dir}` file. Do not add ADR promotion tasks — `/spec-technical-review` creates Draft files; PE acceptance happens before planning. |
| P13 | **Technical design reference** — §0 present; technical review path populated or explicitly N/A with reason; PE sign-off status stated as `[x] complete — {date}` (not `[ ] required`) when TDD was produced; **FAIL** if TDD Status field in `Technical-Review-{initiative}.md` still reads `Draft`, or any required ADR file is not `Accepted` — the dev has not committed the pre-approval acceptance package and the plan must not proceed |
| P14 | **WorkManifest seed** — §9 present; wave IDs (`W0`, `W1`, …) match plan waves exactly; every TASK row has `codebase`, `spec_path`, `verify_command`, and **Implements `REQ-*`**; each wave has `tasks[]` + body task table with stable `TASK-*` ids; YAML is syntactically valid |
| P15 | **Co-ship live verify** — if this wave's FILE list adds or materially changes a **product surface** (HTTP route, worker ingress, lane start, public contract, or equivalent callable entry), the same wave MUST include (a) ≥1 unit TEST/TASK covering the change and (b) ≥1 FILE under profile `live_verify_dir` that exercises the new/changed surface (plus `tests_readme` / feature-map rows as needed). Wave `verify_command` MUST be the **live** script entry (path/command under `live_verify_dir`), not `{test_command}` / `make test` / an unrelated existing smoke. **FAIL** if only unit coverage ships, if live verify is bare `N/A` when this check applies, or if `verify_command` is unit-only. Unrelated smoke does not satisfy unless the plan proves it asserts the new surface. Agent runs check+unit only; the human runs the co-shipped script at checkpoint `live-verify`. |

## P15 examples (narrative)

| Scenario | Verdict |
|----------|---------|
| Wave adds an HTTP route; FILE list has unit tests only; `verify_command: make test` | **FAIL** — no `live_verify_dir` artifact; unit is not live |
| Wave adds a worker ingress; FILE list includes `tests/verify/verify_foo.py` (or profile `live_verify_dir` equivalent) + unit TEST; `verify_command` points at that script | **PASS** |
| Wave is docs-only / no new product surface; live `verify_command` N/A with reason | **PASS** (P15 does not apply) |
