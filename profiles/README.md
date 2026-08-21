# Harness profiles

Stack-specific layout keys for development skills. **Identity equality:** the
filename stem, YAML `profile:` field, Launchpad harness profile name, and
`.harness-pin.yaml` `profile:` / `agent_skills.profile` must be the **same**
`stack_key` (no aliases).

**launchpad `apply-harness`** copies `profiles/{stack_key}.yaml` →
`.harness/profile.yaml` in the consumer app repo.

| Profile | Consumer repos | Skill list key |
|---------|----------------|----------------|
| [meta-pm.yaml](meta-pm.yaml) | `<slug>-meta` (PM lane) | `requirements_skills` |
| [python-backend.yaml](python-backend.yaml) | FastAPI microservices | `development_skills` |
| [nextjs-frontend.yaml](nextjs-frontend.yaml) | Next.js BFF portals | `development_skills` |
| [terraform-iac.yaml](terraform-iac.yaml) | Terraform IaC | `development_skills` |
| [flink.yaml](flink.yaml) | Flink streaming monorepos | `development_skills` |
| [edge-agent.yaml](edge-agent.yaml) | Edge agent services | `development_skills` |
| [edge-inference-engine.yaml](edge-inference-engine.yaml) | Edge inference engine | `development_skills` |
| [android-kotlin.yaml](android-kotlin.yaml) | Android / Kotlin apps | `development_skills` |
| [ios-swift.yaml](ios-swift.yaml) | iOS / Swift apps | `development_skills` |

Domain/team names (e.g. `data-platform-devs`) are **not** prayog profile names.
There is no `data-platform` or `frontend` profile.
