# pm-agent-team

A team of AI agents that covers the full product management lifecycle, from company diagnosis and customer discovery to launch and post-launch analytics, built to cut PM cycle time and cost.

> **Status:** All 11 components are built: the Company Diagnostic, 9 specialist agents (including an independent Reviewer and a one-page Executive Brief) and the Orchestrator that runs them end to end.

## Results (updated as agents ship)

| Deliverable | Manual baseline | With agents | Time saved | Cost per run |
|---|---|---|---|---|
| Company diagnosis (SaaS case) | _measure_ | _tbd_ | _tbd_ | _tbd_ |
| Feedback synthesis (50 items) | _measure_ | _measure_ | _tbd_ | _tbd_ |
| Prioritized roadmap | _measure_ | _tbd_ | _tbd_ | _tbd_ |
| PRD | _measure_ | _tbd_ | _tbd_ | _tbd_ |

## The team

| # | Agent | Owns | Status |
|---|---|---|---|
| 0 | Company Diagnostic | Diagnoses revenue leaks and levers, proposes strategic bets (Head-of-Product front end) | Built |
| 1 | Discovery | Synthesizes feedback, tickets, interviews into themes | Built |
| 2 | Prioritization | Scores opportunities, drafts roadmap with reasoning | Built |
| 3 | PRD | PRDs, user stories, acceptance criteria | Built |
| 4 | Orchestrator | Runs the team end to end, hands off context, quality-gates, reports time and cost | Built |
| 5 | Delivery | Backlog, sprint planning, risks, status updates | Built |
| 6 | Launch / GTM | Release notes, positioning, enablement | Built |
| 7 | Analytics | Success metrics, experiment readouts, feedback loop | Built |
| 8 | Pricing & Billing | Pricing/packaging analysis, billing-feature specs | Built |
| 9 | Reviewer | Independent check: number grounding (in code), cross-stage consistency, unsupported claims | Built |
| 10 | Executive Brief | One-page CEO brief: diagnosis, top bets, plan, decisions, open validation items | Built |

## Quick start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python -m agents.diagnostic.run examples/company_dossier_sample.json
python -m agents.discovery.run examples/feedback_sample.json
python -m agents.prioritization.run outputs/discovery_report.md examples/context_sample.json
python -m agents.prd.run outputs/prioritization_report.md --item 1
python -m agents.pricing_billing.run examples/company_dossier_sample.json
python -m agents.delivery.run outputs/prd_item_1.md
python -m agents.launch.run outputs/prd_item_1.md
python -m agents.analytics.run outputs/prd_item_1.md --baseline 0.208 --mde 0.10
python -m agents.reviewer.run examples/company_dossier_sample.json
python -m agents.brief.run examples/company_dossier_sample.json
```

## Run the whole team in one command

```bash
python -m agents.orchestrator.run examples/company_dossier_sample.json \
  --feedback examples/feedback_sample.json \
  --context examples/context_sample.json \
  --manual-minutes 240

# all 10 agents (adds the Reviewer and the Executive Brief):
python -m agents.orchestrator.run examples/company_dossier_sample.json --full
```

The Orchestrator runs Diagnostic, Discovery, Prioritization and PRD in order (add `--full` for Pricing & Billing, Delivery, Launch / GTM, Analytics, the Reviewer and the Executive Brief), checks each output for required sections, and writes `outputs/pipeline_summary.md` with per-stage time, tokens and cost, plus time saved against your manual baseline.

## Design principles

- One agent, one job, explicit inputs and outputs (see each agent's `SPEC.md`).
- Numbers are computed in code; the model interprets them and never does the arithmetic.
- Every agent run is measured: time, tokens, cost.
- Output is hypotheses to validate. A human stays in the loop on decisions.

## Author

Built by Karishma Wadhwani, product leader with 10+ years in billing, payments and subscription lifecycle.

## License

MIT
