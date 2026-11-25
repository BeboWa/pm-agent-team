# pm-agent-team

![tests](https://github.com/BeboWa/pm-agent-team/actions/workflows/tests.yml/badge.svg)

A team of AI agents that covers the full product management lifecycle, from company diagnosis and customer discovery to launch and post-launch analytics, built to cut PM cycle time and cost.

> **Status:** All 12 components are built: the Company Diagnostic, 10 specialist agents (including an independent Reviewer, a one-page Executive Brief and a Deliverables builder that makes the client deck and Word document) and the Orchestrator that runs them end to end.

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
| 11 | Deliverables | Client-ready deck (with speaker notes) and Word report, plus a private prep sheet with objections | Built |

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
python -m agents.deliverables.run examples/company_dossier_sample.json
```

## Collect a company's numbers (intake)

Open `intake/intake_form.html` in a browser. The company fills it in (aggregate figures only; nothing is uploaded) and downloads a dossier file. `python -m intake.validate <file>` checks it, and the same check runs automatically before every pipeline run. See `intake/README.md`.

## Run the whole team in one command

```bash
python -m agents.orchestrator.run examples/company_dossier_sample.json \
  --feedback examples/feedback_sample.json \
  --context examples/context_sample.json \
  --manual-minutes 240

# all 11 agents (adds the Reviewer, Executive Brief and Deliverables):
python -m agents.orchestrator.run examples/company_dossier_sample.json --full
```

The Orchestrator runs Diagnostic, Discovery, Prioritization and PRD in order (add `--full` for Pricing & Billing, Delivery, Launch / GTM, Analytics, the Reviewer and the Executive Brief), checks each output for required sections, and writes `outputs/pipeline_summary.md` with per-stage time, tokens and cost, plus time saved against your manual baseline.

## Separate folder per client

```bash
python -m agents.orchestrator.run client_dossier.json --full --client "Acme Inc"
```

Everything is saved under `runs/acme-inc/<timestamp>/` with the inputs and a `manifest.json` (model, code version, input fingerprints, per-stage time, tokens, cost and quality-gate results). Without `--client`, output goes to `outputs/`.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The suite uses a fake model, so it is free and fast. It covers the metric and pricing math, the number-grounding check, the output-continuation logic, the intake validator, the deck and Word builders, and a full pipeline run. It runs automatically on GitHub for Python 3.9 and 3.12.

## Check what is pushed

```bash
bash scripts/check_push_status.sh
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
