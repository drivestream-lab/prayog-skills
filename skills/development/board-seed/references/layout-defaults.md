# Layout defaults (board-seed)

When `.harness/profile.yaml` is absent, use:

| Key | Default |
|-----|---------|
| `reports_dir` | `docs/specification/reports` |
| `plan_prefix` | `Implementation-Plan` |
| Integration branch | `develop` |

Meta governance path (read-only): resolve from workspace sibling
`{meta_repo}/config/governance-<org>.yaml` or `launchpad board-bind --json`.

Stack profile affects **verify commands in wave bodies**, not board name or
seed hierarchy.
