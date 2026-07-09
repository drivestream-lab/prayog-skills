# Harness profiles

Stack-specific layout keys for development skills. **launchpad `sync-harness`** copies `profiles/{profile}.yaml` → `.harness/profile.yaml` in the consumer app repo (profile name from `.harness-pin.yaml`).

| Profile | Consumer repos | Skill list key |
|---------|----------------|----------------|
| [meta-pm.yaml](meta-pm.yaml) | `<slug>-meta` (PM lane) | `requirements_skills` |
| [python-backend.yaml](python-backend.yaml) | FastAPI microservices | `development_skills` |
| [frontend.yaml](frontend.yaml) | Next.js BFF portals | `development_skills` |

Stack-specific layout keys live in each profile YAML. **launchpad `apply-harness`** copies
`profiles/{profile}.yaml` → `.harness/profile.yaml` in app repos only (not meta).
