# Agent 5: Delivery

**Job:** Turn a PRD into a plan the team can execute: a ticketed backlog, a dependency map, a sprint plan sized to real capacity, and a stakeholder update.

**Inputs:** PRD (Markdown, default `outputs/prd_item_1.md`); optional `context.json` (team size, sprint length, constraints).

**Output:** Markdown plan with:
1. Backlog: epics and tickets with story-point estimates and acceptance-criteria pointers
2. Dependencies and critical path
3. Sprint plan sized to the stated team capacity
4. Risks and mitigations
5. Draft stakeholder status update
6. Run metrics

**Principles:** Estimates are rough and labeled as such; the team re-estimates. Never schedule more than stated capacity. Surface dependencies on other teams (finance, legal, security, support) explicitly.

**Success metrics:** Time vs. manual backlog grooming; engineers say "I could start Monday"; every ticket traces to a PRD requirement.
