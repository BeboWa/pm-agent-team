# Agent 1: Discovery

**Job:** Turn raw customer signal into ranked, evidence-backed problem themes.

**Inputs:** JSON list of feedback items: `{id, source, text, segment?}` (support tickets, interview notes, reviews, sales call notes).

**Output:** Markdown report with:
1. Top themes, ranked by frequency and severity
2. Evidence for each theme (item ids, short paraphrases)
3. Affected segments
4. Open questions and what to validate next
5. Run metrics (time, tokens, cost)

**Not in scope:** Deciding what to build (that is the Prioritization agent).

**Success metrics:** Time vs. manual synthesis; theme accuracy vs. a human-labeled sample; every theme cites at least 2 item ids.
