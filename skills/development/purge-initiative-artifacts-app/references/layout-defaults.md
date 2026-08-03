# Layout defaults (`/purge-initiative-artifacts-app`)

When `.harness/profile.yaml` is absent, use:

| Key | Default |
|-----|---------|
| `product_spec_dir` | `docs/specification/product` |
| `adr_dir` | `docs/specification/adr` |
| `reports_dir` | `docs/specification/reports` |
| `source_roots` | `src/` |
| `unit_tests_dir` | `tests/unit` |
| `live_verify_dir` | `tests/verify` |

Purge note: `Purge-App-{INIT}.md` under `reports_dir`.
Allowlist SSOT: `../../../references/artifact-write-contract.md`.
