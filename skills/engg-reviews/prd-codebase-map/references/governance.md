# Governance — product questions vs engineering appendix

## Routing rubric

| Topic | Audience | Where |
|-------|----------|-------|
| User-visible behaviour, UX, priority, scope in/out | **PM** | Product questions section + meta PR |
| “Already shipped vs still required” | **PM** | Product question (`exists` confirm) |
| Acceptance criteria / definition of done for users | **PM** | Product question |
| Module boundaries, ADR gaps, API shapes, test policy | **PE / eng** | Eng appendix only — not asked to PM |
| Implementation plan / waves / tasks | **Eng later** | Out of scope for engg-reviews |

Do **not** ask PM to choose architecture. Do **not** turn engg-reviews into
`/spec-draft` or `/initiative-feasibility`.

## Relationship to SDD

| Artifact / gate | Relationship |
|-----------------|--------------|
| Impact map + Gate 1 | Independent; map may use impact-map as candidate hint only |
| `/spec-draft` | Still blocked until meta merge + LGTM — engg-reviews does not change that |
| `/initiative-feasibility` | Later may optionally consume this map — not required in Phase 1 |

## Language

- Product questions: actors, journeys, outcomes, policy choices.
- Evidence citations may include file paths for PE trust, but the **question
  stem** must remain understandable without opening the repo.
