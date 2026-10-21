# Agent 2: Prioritization

**Job:** Turn Discovery's problem themes into a ranked, scored roadmap with visible reasoning.

**Inputs:**
- A Discovery report (Markdown), by default `outputs/discovery_report.md`
- Optional `context.json`: business goals, constraints (team size, quarter, strategy), so scoring reflects reality

**Output:** Markdown report with:
1. RICE-scored table (Reach, Impact, Confidence, Effort, Score), ranked
2. Reasoning for each score, with assumptions stated
3. Now / Next / Later roadmap
4. What we are deliberately NOT doing, and why
5. Biggest risks and what would change the ranking
6. Run metrics (time, tokens, cost)

**Principles:** Scores are estimates, not facts. Every number carries a stated assumption, low-confidence items are flagged, and a human makes the final call.

**Success metrics:** Time vs. manual prioritization; PM agreement with the top 3 ranked items; every score has a written rationale.
