# Agent 9: Reviewer

**Job:** Independently check the team's work before a human relies on it: are the numbers grounded, do the stages agree with each other, and are any claims unsupported?

**Inputs:** All stage reports (from the Orchestrator, or from `outputs/`), plus the company dossier. Optional feedback is already reflected in the Discovery report.

**Process:**
1. `grounding.py` runs a deterministic check in code. It finds every dollar figure of $1,000 or more in each report and tests whether it appears in the source data, the computed metrics, the computed pricing scenarios (including simple x12 and /12 conversions), or an earlier stage's report. Anything else is listed as a figure to verify.
2. The model reviews the reports against the sources and the pre-check list: grounding, cross-stage consistency, unsupported claims, overclaimed certainty, and missing review flags (finance, legal, tax) for billing changes.

**Output:** Markdown review with:
1. Overall verdict
2. Stage-by-stage verdicts (PASS / PASS WITH NOTES / REVISE) with specific issues, severity and suggested fixes
3. Cross-stage consistency findings
4. Figures to verify (from the code pre-check, with the model's judgment on each)
5. Top issues for the human
6. Run metrics

**Known limitation:** the check allows 2% rounding and simple x12 and /12 conversions, so an unsupported figure that happens to land near a legitimate one can slip through (a coincidental match). It is a flag generator, not proof of grounding.

**Principles:** Skeptical but fair. Specific, not vague. Does not rewrite the work. Does not invent issues. This is an LLM review plus a code check; it will miss things, so a human still owns the final read.

**Success metrics:** Issues found are real on human spot-check; catches planted errors in test inputs; low false-alarm rate.
