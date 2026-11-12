# Design checks (D1–D8)

Closed set for `/qa-test-design`. All eight pass before the pack is
published. A failed check is fixed in the pack, or the run stops and
names `/qa-requirements-review`. Do not publish a pack that fails a check.

| Id | Pass when |
|----|-----------|
| D1 | The review file exists. `pack` header `review_revision` matches it. `ready_for_test_design` is `yes`, or every open blocking `QQ-*` is on the accepted-risk list. |
| D2 | Every actor, expected result, numeric or time bound, and layer traces to a PRD quote or an answer quote. |
| D3 | Every REQ in the review inventory has at least one `EAC-*` and one `TC-*`, except accepted-risk REQs, which have zero `TC-*`. |
| D4 | Every `TC-*` cites at least one `REQ-*` and one `EAC-*`. Every `EAC-*` cites exactly one `REQ-*`. |
| D5 | `layer` is `ui`, `be`, or `both`, and the layer-plan row quotes the evidence. |
| D6 | Cases match the rung plan. `unit`, `capability`, and `journey` stay separate. A journey case is not treated as the capability case, or the reverse. |
| D7 | Cases contain no automation code, selectors, or routes, payloads, or status codes the PRD did not state. |
| D8 | RTM REQ ids equal the review inventory REQ ids. RTM `TC` ids equal the case-file ids. No orphan case. |

Check ids are not handoff blockers. Blockers stay `QQ-*`.
