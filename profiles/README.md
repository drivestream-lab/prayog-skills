# Harness profiles

Stack-specific layout keys for development skills. **launchpad `sync-harness`** copies `profiles/{profile}.yaml` → `.harness/profile.yaml` in the consumer app repo (profile name from `.harness-pin.yaml`).

| Profile | Consumer repos | `source_roots` |
|---------|----------------|----------------|
| [python-backend.yaml](python-backend.yaml) | FastAPI microservices | `src/` |
| [frontend.yaml](frontend.yaml) | Next.js BFF portals | `app/`, `lib/`, `components/`, `hooks/` |

Skills resolve paths from `.harness/profile.yaml` when present; else per-skill `references/layout-defaults.md` (generic fallback only).
