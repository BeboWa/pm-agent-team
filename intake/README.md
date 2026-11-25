# Intake: getting a company's numbers into the pipeline

The pipeline runs on a one-page **dossier** (a JSON file of aggregate figures). This folder makes collecting it painless and safe.

## Files
- `intake_form.html`: a self-contained form. Open it in any browser. Nothing is uploaded; the company fills it in and downloads `dossier_<company>.json`. You can email the file, or host it later (for example with GitHub Pages).
- `validate.py`: checks a dossier before the pipeline runs. It runs automatically at the start of every orchestrator run.

## Workflow for a pilot
1. Send the company `intake_form.html` (or fill it in yourself during a 30-minute intake call).
2. They send back the downloaded `dossier_<company>.json`.
3. Check it: `python -m intake.validate dossier_acme.json`
4. Run it, with a separate folder per client:
   `python -m agents.orchestrator.run dossier_acme.json --full --client "Acme Inc"`
   Everything lands in `runs/acme-inc/<timestamp>/`, with a `manifest.json` recording inputs, cost and quality-gate results.

## What the validator catches
- Revenue and customer counts that do not add up (start + new + expansion - contraction - churned = end)
- Percentages entered as 40 instead of 0.4
- A funnel that grows instead of shrinking
- Personal data: email addresses, phone numbers, ID numbers, payment card numbers
- Missing consent record for real client data (warning)

## What is deliberately not collected
Customer names, contact details, individual accounts or transactions. Aggregate totals and averages only.

## Before using with a real company
Get written permission covering data use, confidentiality and deletion, and note that figures are processed by a third-party AI provider. This is not legal advice; have a lawyer review your agreement.
