# Live smoke policy

Resolve paths from `.harness/profile.yaml` or [layout-defaults.md](layout-defaults.md).

Layer ownership for Pass-1 prove. There is **no** `/verify` content skill —
human smoke runs at checkpoint `wave-acceptance`. Content skills never apply
labels, commit, or merge (Forge / human / orch only).

## Layer ownership

| Layer | Who owns / runs | Location / evidence | Proves | Must not |
|-------|-----------------|---------------------|--------|----------|
| **Unit** | Agent (`/loop-spec`) | `unit_tests_dir` | Deterministic logic, branches, edge cases with mocked dependencies | Require a deployed/running stack; substitute for smoke/sandbox |
| **Integration / contract** | Agent or CI when the harness defines it | Contract/integration suite from `tests_readme` / profile | Cross-module wiring and interface shapes without full product UX | Duplicate unit-only assertions; substitute for live smoke/sandbox |
| **Smoke** | Human (checkpoint `wave-acceptance`) | `live_verify_dir` scripts | Critical path on a **running** stack | Assert deep edge cases already covered by unit; duplicate unit-only assertions |
| **Sandbox** | Human at `wave-acceptance` | `live_verify_dir` + documented sandbox env | Environment-dependent behavior with safe test data | Leave fixtures/processes running; skip cleanup/stop conditions; duplicate unit-only assertions |
| **Debug** | Exploratory | `debug_tests_dir` | Exploration and diagnosis | Gate Pass-1 or Pass-2 |

**Co-ship:** when a wave adds or materially changes a product surface, the same
wave ships ≥1 unit TEST **and** ≥1 FILE under `live_verify_dir` (plan check
P15). Agent implements the script; human executes it at `wave-acceptance`.
WorkManifest `verification.live` (when applicable) declares mode, command,
covers, prerequisites, expected observations, cleanup, and stop conditions —
observed results are human prove; the gate is checkpoint `pass` / label
`wave-accepted`, not a Live-Verify skill artifact.

**No overlap / forbid unit-as-live:** do not assert the same behavior in unit and
live smoke for the same feature. Wave `verify_command` /
`verification.live.command` must not be unit-only (`make test`, bare `pytest`,
`{test_command}`).

## Pass-1 gate

After `/loop-spec` + `wave-pr-action`, human-checkpoint `wave-acceptance`:

1. Run co-shipped `{verify_command}` (or accept P15 N/A).
2. Signal accept with GitHub label `wave-accepted` on the tip (phase-1) —
   humans or Gateflow consume this; **content skills do not apply labels**.
3. `pass` = **human approved** for this wave tip (only approval signal).
4. Park at `wave-awaiting-closeout`; Pass-2 closeout closes the wave.

## Content / Forge boundary

Running the smoke script is verification tooling, not Forge. Skills never
commit, label, or merge. Tracker/PR publication is ForgeClient / human forge
skills / human GitHub only.
