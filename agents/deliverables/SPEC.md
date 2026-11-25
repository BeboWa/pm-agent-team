# Agent 11: Deliverables

**Job:** Turn the pipeline's reports into client-ready material you can review and present: a readout deck, a full report document, and a private prep sheet with a talk track and likely objections.

**Inputs:** The stage reports, Executive Brief and Reviewer report in `outputs/` (or passed in by the Orchestrator), plus the company dossier.

**Process:**
1. A Presenter step (the model) writes the deck content as structured JSON: seven fixed slides (diagnosis, leaks, bets, pricing, plan, decisions, risks), speaker notes, and likely objections with suggested answers.
2. Code validates the JSON (required slides, bullet counts and lengths) and checks every dollar figure in the deck against the sources and the earlier reports.
3. Code renders the deck. The scorecard slide is built from the metrics computed in code, never written by the model.
4. Code renders the full report as a Word document from the Markdown reports. Internal material (the Reviewer report and run metrics) is left out.

**Outputs in `outputs/deliverables/`:**
- `deck.pptx`: about 10 slides with speaker notes (client-facing)
- `report.docx`: the full report (client-facing)
- `readout_prep.md`: figures to verify, talk track, likely objections (private, for you only)
- `deck.json`: the editable deck content

**Edit loop:** change anything in `deck.json`, then run with `--rebuild` to re-render the deck, document and prep sheet without another model call.

**Principles:** Hypotheses, not guarantees. No figure appears that is not in the sources. The deck and the document are drafts: a human reviews and approves everything before it goes to a client.

**Success metrics:** Time from reports to a presentable deck; edits needed before presenting; no ungrounded figures reach the client.
