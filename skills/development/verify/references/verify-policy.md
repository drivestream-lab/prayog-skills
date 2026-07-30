# Verify policy

Resolve paths from `.harness/profile.yaml` or [pre-implement layout defaults](../../pre-implement/references/layout-defaults.md).

| Layer | Who runs | Location (profile key) | Proves |
|-------|----------|------------------------|--------|
| Unit | Agent (`/loop-spec`) | `unit_tests_dir` | Logic, branches, edge cases (mocked dependencies) |
| Live verify | Human (checkpoint `live-verify`) | `live_verify_dir` | Product feature on **running** stack |
| Debug | Exploratory | `debug_tests_dir` | Exploration — not gating |

**Co-ship:** when a wave adds or materially changes a product surface, the same
wave ships ≥1 unit TEST **and** ≥1 FILE under `live_verify_dir` (plan check
P15). Agent implements the script; human executes it. Depth of inspection
follows env access (sandbox vs fuller stack).

**No overlap:** do not assert the same behavior in unit and live verify for the
same feature.

**Commands:** read `tests_readme` for env activation, config files, bootstrap
scripts, and exact live-verify invocations. Wave `verify_command` is the live
script entry — not `{test_command}` / `make test`. Do not hardcode
repo-specific env names in the skill — defer to the runbook.

**Pass-1 gate vs optional `/verify`:** the Pass-1 stop after `/loop-spec` is
human-checkpoint `live-verify` (run the co-shipped script). Skill `/verify` is
`dispatch: manual` — optional aid; not on the Pass-1 edge; not a substitute for
co-shipping the script.

**Constitution:** `rules_glob` (include testing-verify rule when present)

**After human live-verify:** update `implementation-status.md` live-verified
column; paste command evidence on PR / tracker Verify field; tip hygiene before
Pass-2 closeout.
