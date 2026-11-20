"""Run the Reviewer agent on the reports in outputs/.

Usage:
  python -m agents.reviewer.run examples/company_dossier_sample.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

from shared.agent import run_agent
from shared.outputs import load_outputs
from agents.diagnostic.metrics import compute_metrics
from agents.pricing_billing.pricing_math import pricing_scenarios
from .grounding import find_ungrounded
from .prompt import SYSTEM_PROMPT


def run(reports: dict | None = None, dossier_path: str = "examples/company_dossier_sample.json") -> str:
    reports = reports or load_outputs()
    if not reports:
        sys.exit("No stage reports found in outputs/. Run the pipeline first.")
    dossier = json.loads(Path(dossier_path).read_text())
    metrics = compute_metrics(dossier)
    scenarios = pricing_scenarios(dossier)
    ungrounded = find_ungrounded(reports, [dossier, metrics, scenarios])

    msg = (
        "## Source data (ground truth)\n\n```json\n" + json.dumps(dossier, indent=2) + "\n```\n\n"
        "## Computed metrics (ground truth)\n\n```json\n" + json.dumps(metrics, indent=2) + "\n```\n\n"
        "## Computed pricing scenarios (ground truth)\n\n```json\n" + json.dumps(scenarios, indent=2) + "\n```\n\n"
        "## Code pre-check: dollar figures NOT found in the sources or in earlier reports\n\n```json\n"
        + json.dumps(ungrounded, indent=2) + "\n```\n\n## Stage reports\n"
    )
    for stage, text in reports.items():
        msg += f"\n### STAGE: {stage}\n\n{text}\n"
    return run_agent(SYSTEM_PROMPT, msg, "review_report.md", max_tokens=8000)


if __name__ == "__main__":
    run(None, sys.argv[1] if len(sys.argv) > 1 else "examples/company_dossier_sample.json")
