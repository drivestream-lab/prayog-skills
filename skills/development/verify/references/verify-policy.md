# Verify policy

Resolve paths from `.harness/profile.yaml` or [pre-implement layout defaults](../../pre-implement/references/layout-defaults.md).

| Layer | Location (profile key) | Proves |
|-------|------------------------|--------|
| Unit | `unit_tests_dir` | Logic, branches, edge cases (mocked dependencies) |
| Verify | `live_verify_dir` | Product feature on **running** stack |
| Debug | `debug_tests_dir` | Exploration — not gating |

**No overlap:** do not assert the same behavior in unit and verify for the same feature.

**Commands:** read `tests_readme` for env activation, config files, bootstrap scripts, and exact verify invocations. Do not hardcode repo-specific env names in the skill — defer to the runbook.

**Constitution:** `rules_glob` (include testing-verify rule when present)

**After verify:** update `implementation-status.md` live-verified column; paste command in PR and tracker Verify field.
