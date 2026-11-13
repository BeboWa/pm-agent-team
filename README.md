# pm-agent-team

A team of AI agents that covers the full product management lifecycle, from company diagnosis and customer discovery to launch and post-launch analytics, built to cut PM cycle time and cost.

> **Status:** Company Diagnostic, Discovery, Prioritization and PRD agents are built. Others are scaffolded and shipping one at a time.

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
| 4 | Orchestrator | Routing, context handoff, quality checks | Planned |
| 5 | Delivery | Backlog, sprint planning, risks, status updates | Planned |
| 6 | Launch / GTM | Release notes, positioning, enablement | Planned |
| 7 | Analytics | Success metrics, experiment readouts, feedback loop | Planned |
| 8 | Pricing & Billing | Pricing/packaging analysis, billing-feature specs | Planned |

## Quick start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python -m agents.diagnostic.run examples/company_dossier_sample.json
python -m agents.discovery.run examples/feedback_sample.json
python -m agents.prioritization.run outputs/discovery_report.md examples/context_sample.json
python -m agents.prd.run outputs/prioritization_report.md --item 1
```

## Design principles

- One agent, one job, explicit inputs and outputs (see each agent's `SPEC.md`).
- Numbers are computed in code; the model interprets them and never does the arithmetic.
- Every agent run is measured: time, tokens, cost.
- Output is hypotheses to validate. A human stays in the loop on decisions.

## Author

Built by Karishma Wadhwani, product leader with 10+ years in billing, payments and subscription lifecycle.

## License

MIT
