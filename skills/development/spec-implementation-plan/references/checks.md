# Plan checks (P1–P16)

Governance detail: [governance.md](governance.md).

Before P1, verify the template's **Source freshness and command contract**
table. Any STALE source or MISSING required command fails the plan; do not run
P1–P16 against obsolete inputs.

| ID | Check |
|----|-------|
| P1 | Every product `REQ-*` in scope for this plan appears in §1; every wave that implements work cites those REQs via TASK **Implements** |
| P2 | Every in-scope `REQ-*` has ≥1 TASK; every TASK **Implements** ≥1 `REQ-*` (no shadow `REQ-W*`) |
| P3 | Every TASK has FILE paths or explicit "docs only" |
| P4 | Every TASK has objective exit evidence: (a) artifact/change under scope, (b) **observable** exit criteria (not “done/works”), (c) proving `command` or `review`, (d) **expected** result, (e) **evidence location** (`evidence_expected`). Same fields appear on the TASK row and in §9 `exit` |
| P5 | Test / verification layers are explicit: **unit**, **integration/contract** (when applicable), **smoke**, and **sandbox**. Unit/integration commands come from profile toolchain; smoke/sandbox are human-run live verify under `live_verify_dir`. Each acceptance criterion maps to a layer in the wave **Verification Coverage** table |
| P6 | No product scope beyond initiative spec |
| P7 | Feasibility blockers and accepted **operational risks** are addressed or explicitly deferred with owner + default-if-deferred; residual ops risk appears in RISK |
| P8 | Wave order and dependencies documented |
| P9 | As-built / README updates listed in same PR as code tasks |
| P10 | Plan is self-contained (fresh agent can execute one wave); source digests/revisions and canonical check/test/verify/ground commands are populated; operational prerequisites for live verify (env class, safe data, cleanup/stop) are stated when live applies |
| P11 | **MDC conformance** — per `rules_glob`; discrepancies in TASK **MDC notes** and RISK table |
| P12 | **ADR conformance** — architectural TASKs cite Accepted ADR id from `{adr_dir}`; §0 "Resolved ADRs" links every TDD §4 `ADR_REQUIRED` file path with `Status: Accepted`; discrepancies in TASK **ADR notes** and RISK table. **FAIL** if any required ADR file is missing, still `Draft`, or only referenced from TDD §4 without a canonical `{adr_dir}` file. Do not add ADR promotion tasks — `/spec-technical-review` creates Draft files; PE acceptance happens before planning. |
| P13 | **Technical design reference** — §0 present; technical review path populated or explicitly N/A with reason; PE sign-off status stated as `[x] complete — {date}` (not `[ ] required`) when TDD was produced; **FAIL** if TDD Status field in `Technical-Review-{initiative}.md` still reads `Draft`, or any required ADR file is not `Accepted` — the pre-approval acceptance package is not on head and the plan must not proceed |
| P14 | **WorkManifest seed** — §9 present; wave IDs (`W0`, `W1`, …) match plan waves exactly; every TASK row has `codebase`, `spec_path`, `verify_command`, and **Implements `REQ-*`**; each wave has `tasks[]` + body task table with stable `TASK-*` ids; YAML is syntactically valid |
| P15 | **Co-ship live verify** — if this wave's FILE list adds or materially changes a **product surface** (HTTP route, worker ingress, lane start, public contract, or equivalent callable entry), the same wave MUST include (a) ≥1 unit TEST/TASK covering the change and (b) ≥1 FILE under profile `live_verify_dir` that exercises the new/changed surface (plus `tests_readme` / feature-map rows as needed). Wave `verify_command` / `verification.live` MUST be the **live** script entry (`smoke` or `sandbox`), not `{test_command}` / `make test` / an unrelated existing smoke. **FAIL** if only unit coverage ships, if live verify is bare `N/A` when this check applies, or if `verify_command` is unit-only. Unrelated smoke does not satisfy unless the plan proves it asserts the new surface. Agent runs check+unit only; the human runs the co-shipped script at checkpoint `live-verify`. Docs-only / no surface → `applicable: false` with reason (**PASS**) |
| P16 | **WorkManifest contract** — §9 validates via `scripts/workmanifest_contract.py` (`prayog/v1` + `WorkManifest`): stable IDs, same-wave dependency DAG (no missing/self/cycle), exact `files[]` path/action, exit criteria+proof, REQ mappings, wave order, and live-verification completeness (cleanup + stop when applicable). Reject `launchpad/v1` identity and mutable board/runtime fields |

## P12 / P13 failure → stage outcome

These checks FAIL when an authoritative artifact **exists** but shows an
unsatisfied gate (Draft ADR, unaccepted TDD, missing Accepted path). Map that
to workflow outcome **`blocked`** (not `failed`, not `needs-input`).

| Situation | Outcome |
|-----------|---------|
| Spec/TDD/feasibility path absent or unreadable | `needs-input` |
| TDD/ADR present but still Draft / not Accepted (P12/P13 FAIL) | `blocked` |
| Digest/head/revision mismatch | `stale` |
| Plan render / WorkManifest contract validation fails (P16) or crashes on otherwise valid inputs | `failed` |
| Vague exit / missing proof / unit-as-live / missing live when P15 applies (P4/P15/P16) | `failed` |
| All P1–P16 PASS | `pass` |

## P15 examples (narrative)

| Scenario | Verdict |
|----------|---------|
| Wave adds an HTTP route; FILE list has unit tests only; `verify_command: make test` | **FAIL** — no `live_verify_dir` artifact; unit is not live |
| Wave adds a worker ingress; FILE list includes `tests/verify/verify_foo.py` (or profile `live_verify_dir` equivalent) + unit TEST; `verify_command` points at that script | **PASS** |
| Wave is docs-only / no new product surface; live `verify_command` N/A with reason | **PASS** (P15 does not apply) |
