# Verify policy

Resolve paths from `.harness/profile.yaml` or [pre-implement layout defaults](../../pre-implement/references/layout-defaults.md).

## Layer ownership

| Layer | Who owns / runs | Location / evidence | Proves | Must not |
|-------|-----------------|---------------------|--------|----------|
| **Unit** | Agent (`/loop-spec`) | `unit_tests_dir` | Deterministic logic, branches, edge cases with mocked dependencies | Require a deployed/running stack; substitute for smoke/sandbox |
| **Integration / contract** | Agent or CI when the harness defines it | Contract/integration suite from `tests_readme` / profile | Cross-module wiring and interface shapes without full product UX | Duplicate unit-only assertions; substitute for live smoke/sandbox |
| **Smoke** | Human (checkpoint `live-verify`) or optional `/verify` | `live_verify_dir` | Critical path on a **running** stack: process starts, primary routes respond, feature is reachable | Assert deep edge cases already covered by unit; duplicate unit-only assertions |
| **Sandbox** | Human / optional `/verify` | `live_verify_dir` + documented sandbox env | Environment-dependent behavior with safe test data | Leave fixtures/processes running; skip cleanup/stop conditions; duplicate unit-only assertions |
| **Debug** | Exploratory | `debug_tests_dir` | Exploration and diagnosis | Gate Pass-1 or Pass-2 |

**Co-ship:** when a wave adds or materially changes a product surface, the same
wave ships ≥1 unit TEST **and** ≥1 FILE under `live_verify_dir` (plan check
P15). Agent implements the script; human executes it. Depth of inspection
follows env access (smoke vs fuller sandbox). WorkManifest
`verification.live` (when applicable) declares mode, command, covers,
prerequisites, expected observations, cleanup, and stop conditions — observed
results belong in `Live-Verify-*`, not in the approved manifest.

**No overlap / forbid unit-as-live:** do not assert the same behavior in unit and
live verify (smoke/sandbox) for the same feature. Smoke/sandbox scripts must
**not** duplicate unit-only assertions. Wave `verify_command` /
`verification.live.command` must not be unit-only (`make test`, bare `pytest`,
`{test_command}`).

## Expected-versus-observed human evidence

Every live run (and the durable `Live-Verify-{INIT}-W{N}.md` artifact) records:

| Field | Rule |
|-------|------|
| Environment | Bound at **runtime** (class + access depth) — not guessed at plan time |
| Build / head | Exact SHA or wave-head ref under test — bound at runtime |
| Expected observations | From WorkManifest live intent / script pass criteria |
| Observed results | Command exit code + key output / UI observations (human evidence) |
| Match | yes / no per expectation — required for `pass` |
| Cleanup | Mandatory for sandbox (and any run that creates durable side effects) |
| Stop conditions | Mandatory for sandbox — when to abort rather than continue destructive steps |

Never mark live `pass` without expected-versus-observed rows filled.

## Commands and prerequisites

Read `tests_readme` for env activation, config files, bootstrap scripts, and
exact live-verify invocations. Wave `verify_command` is the live script entry —
not `{test_command}` / `make test`. Do not hardcode repo-specific env names in
the skill — defer to the runbook.

Do not skip documented prerequisites. Missing prerequisites → `blocked`, not
`failed` inventing a pass.

## Pass-1 gate vs optional `/verify`

The Pass-1 stop after `/loop-spec` is human-checkpoint `live-verify` (run the
co-shipped script). Skill `/verify` is `dispatch: manual` — optional aid; not
on the Pass-1 edge; not a substitute for co-shipping the script. Both use the
same `Live-Verify-*` evidence shape.

## Content / Forge boundary

Running the verify command is verification tooling, not Forge. Never commit
evidence, update a PR/tracker, or apply labels from this skill. Emit Forge
readiness (`commit_workspace`) when the durable report needs publication.

**Constitution:** `rules_glob` (include testing-verify rule when present)

**After human live-verify:** update `implementation-status.md` live-verified
column locally when in scope; capture command evidence in `Live-Verify-*`; tip
hygiene before Pass-2 closeout. Tracker/PR publication is Forge/human, not
this skill's mutation.
