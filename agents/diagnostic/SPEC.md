# Agent 0: Company Diagnostic

**Job:** Diagnose where a company's revenue is, where it leaks, and which few strategic bets would grow it fastest. This is the Head-of-Product front end that feeds the rest of the team.

**Inputs:** A company dossier (JSON): description, revenue movements (new / expansion / contraction / churned MRR), customer counts, CAC and margin, pricing tiers, funnel, competitors, qualitative signals, constraints. Missing fields are allowed; the agent flags data gaps instead of guessing.

**Process:**
1. `metrics.py` computes the numbers deterministically (ARR, NRR, GRR, churn, CAC payback, LTV/CAC, funnel conversion). The LLM never does the arithmetic.
2. The agent interprets the numbers, finds the leaks and levers, and estimates $ impact with stated assumptions.

**Output:** Markdown report with:
1. Business model snapshot
2. Health scorecard (computed metrics vs. rule-of-thumb benchmarks)
3. Revenue equation: what actually drives growth
4. Leaks and levers, ranked by estimated annual $ impact, with assumptions
5. Monetization opportunities (pricing, packaging, expansion, involuntary churn)
6. Top 3 strategic bets, each with a hypothesis and how to validate it
7. Data gaps and what to request first
8. 30/60/90-day validation plan
9. Handoff: bets formatted for the Prioritization agent
10. Run metrics

**Principles:** Hypotheses, not verdicts. Every $ estimate carries its assumptions. Benchmarks are rules of thumb and vary by segment and stage. A human validates before anyone acts.

**Success metrics:** Exec review: "would a Head of Product say this?"; every claim traces to a provided number; bets are specific and testable; time vs. a manual diagnostic.
