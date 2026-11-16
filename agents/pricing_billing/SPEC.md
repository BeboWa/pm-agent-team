# Agent 8: Pricing & Billing

**Job:** Find and size the monetization opportunities in pricing, packaging, discounting, annual plans, and payment recovery, and spec the billing implications. This is the agent built on billing and payments domain expertise.

**Inputs:** Company dossier (JSON, same file as the Company Diagnostic); optional Company Diagnostic report.

**Process:**
1. `pricing_math.py` computes scenario tables in code: involuntary-churn recovery, price increases against assumed churn, discount leakage and break-even lost-deal rates, and annual-plan shift cash effects.
2. The agent interprets the tables, recommends pricing and packaging changes, and specs the billing and payments implications.

**Output:** Markdown report with:
1. Current monetization model
2. Scenario math (computed)
3. Recommended pricing and packaging changes (with value metric and fences)
4. Billing and payments implications (proration, dunning, invoicing, tax, revenue recognition, entitlements)
5. Migration and rollout (grandfathering, notice periods)
6. Test plan and risks
7. Run metrics

**Principles:** Scenarios are illustrative, driven by labeled assumptions, never forecasts. Always include the downside case. Flag legal, tax, and finance review for any change that touches customer billing. A human validates before anything ships.

**Success metrics:** Time vs. manual pricing analysis; a finance lead can reproduce every number; billing implications are specific enough for engineering to scope.
