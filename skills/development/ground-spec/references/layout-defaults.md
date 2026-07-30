# Layout defaults (`/ground-spec`)

When `.harness/profile.yaml` is absent, use:

| Key | Default |
|-----|---------|
| `constitution` | `AGENTS.md` |
| `rules_glob` | `.cursor/rules/*.mdc` |
| `product_spec_dir` | `docs/specification/product` |
| `as_built` | `docs/specification/as-built/implementation-status.md` |
| `adr_dir` | `docs/specification/adr` |
| `reports_dir` | `docs/specification/reports` |
| `tests_readme` | `tests/README.md` |
| `source_roots` | `src/` |
| `unit_tests_dir` | `tests/unit` |
| `live_verify_dir` | `tests/verify` |
| `debug_tests_dir` | `tests/debug` |

Reports filename: `Ground-Report-{SPEC}-W{N}.md` under `reports_dir`.
Related wave artifacts: `Wave-Execution-{INIT}-W{N}.md`,
`Live-Verify-{INIT}-W{N}.md`, `Learning-Extract-{INIT}-W{N}.md`.
