# Agent 4: Orchestrator

**Job:** Run the whole team in one command: hand each agent's output to the next, check the work, and report total time and cost.

**Pipeline:**
1. Company Diagnostic: company dossier in, strategic bets out
2. Discovery (optional): customer feedback in, problem themes out
3. Prioritization: diagnosis (plus discovery, if provided) in, RICE-ranked roadmap out
4. PRD: top-ranked item in, buildable PRD out

With `--full`, it also runs Pricing & Billing (after the Diagnostic, and fed into Prioritization) and, after the PRD, Delivery, Launch / GTM and Analytics, then the Reviewer (independent check of all reports) and the Executive Brief (one-page summary): all 10 agents.

**Inputs:** company dossier (required); `--feedback` file, `--context` file, `--item N`, `--full`, `--baseline` / `--mde` (Analytics sample-size math), `--manual-minutes N` (your hand-done baseline), `--no-log`.

**Outputs:** every stage report plus `outputs/pipeline_summary.md`: per-stage time, tokens, cost, quality-gate results, totals, and time saved if a baseline was given. Also appends a row to `evals/results.csv` (skip with `--no-log`).

**Quality gate:** deterministic structure check. Did each stage return every required section? It flags missing sections. It does not judge whether the content is correct; a human reviews that.

**Principles:** Stops with a clear message if a stage fails. Never hides cost. Output is hypotheses to validate, not decisions.

**Success metrics:** End-to-end run time and cost vs. a manual baseline; share of runs that pass the quality gate; PRD is reviewable by an engineer without rework.
