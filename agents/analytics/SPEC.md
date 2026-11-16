# Agent 7: Analytics

**Job:** Define how a feature's success will be measured and how the decision will be made: metric framework, tracking plan, experiment design, decision rules, and a readout template that feeds learning back into Discovery and the Company Diagnostic.

**Inputs:** PRD (Markdown, default `outputs/prd_item_1.md`); optional Company Diagnostic report; optional `--baseline` conversion rate and `--mde` relative minimum detectable effect.

**Process:** `stats.py` computes the required sample size per arm in code (two-proportion test, 95% confidence, 80% power). The model designs the measurement plan around that number and never does the arithmetic.

**Output:** Markdown plan with:
1. Metric framework (primary, secondary, guardrail)
2. Tracking plan (events and properties)
3. Experiment design with the computed sample size
4. Decision rules (ship, iterate, kill)
5. Readout template
6. Feedback loop into the next planning cycle
7. Run metrics

**Principles:** Pre-commit to decision rules before seeing data. Always include guardrail metrics. State when an experiment is not feasible at the available traffic. Output is a plan; a human owns the decision.

**Success metrics:** Time vs. manual measurement planning; analysts say the tracking plan is implementable; decision rules are unambiguous.
