# Agent 3: PRD

**Job:** Turn the top-ranked roadmap item into a clear, buildable Product Requirements Document.

**Inputs:**
- A Prioritization report (Markdown), by default `outputs/prioritization_report.md`
- Optional `--item N` to pick the Nth ranked item (default: 1, the top item)
- Optional `--context context.json` with company, team and constraints

**Output:** Markdown PRD with:
1. Problem statement and evidence
2. Goals and explicit non-goals
3. Target users / segments
4. Requirements (must / should / could)
5. User stories with testable acceptance criteria
6. Success metrics (leading and lagging) with targets stated as hypotheses
7. Risks, dependencies, and open questions
8. Rollout and launch plan outline
9. Run metrics (time, tokens, cost)

**Principles:** Stay grounded in the upstream evidence and never invent customer data. Mark assumptions. Acceptance criteria must be testable. Open questions go to the PM, not buried in prose.

**Success metrics:** PRD time vs. manual writing; engineer/designer review: "could we start building from this?"; every requirement traces back to a problem in the evidence.
