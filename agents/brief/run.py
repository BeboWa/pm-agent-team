"""Run the Executive Brief agent on the reports in outputs/.

Usage:
  python -m agents.brief.run examples/company_dossier_sample.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

from shared.agent import run_agent
from shared.outputs import load_outputs
from agents.diagnostic.metrics import compute_metrics
from agents.pricing_billing.pricing_math import pricing_scenarios
from .prompt import SYSTEM_PROMPT

EXCERPT_CHARS = 6000  # long operational reports are excerpted; strategy reports are included in full
FULL_STAGES = {"Company Diagnostic", "Pricing & Billing", "Prioritization"}


def run(reports: dict | None = None, review_text: str | None = None,
        dossier_path: str = "examples/company_dossier_sample.json") -> str:
    reports = reports or load_outputs()
    if not reports:
        sys.exit("No stage reports found in outputs/. Run the pipeline first.")
    if review_text is None:
        rp = Path("outputs/review_report.md")
        review_text = rp.read_text() if rp.exists() else "(No review available.)"
    dossier = json.loads(Path(dossier_path).read_text())

    msg = (
        "## Company\n\n" + str(dossier.get("company", "company")) + "\n\n"
        "## Computed metrics (ground truth)\n\n```json\n" + json.dumps(compute_metrics(dossier), indent=2) + "\n```\n\n"
        "## Computed pricing scenarios (ground truth)\n\n```json\n" + json.dumps(pricing_scenarios(dossier), indent=2) + "\n```\n\n"
        "## Reviewer report\n\n" + review_text + "\n\n## Stage reports\n"
    )
    for stage, text in reports.items():
        body = text if stage in FULL_STAGES else text[:EXCERPT_CHARS] + ("\n...(excerpt)" if len(text) > EXCERPT_CHARS else "")
        msg += f"\n### STAGE: {stage}\n\n{body}\n"
    return run_agent(SYSTEM_PROMPT, msg, "executive_brief.md", max_tokens=3500)


if __name__ == "__main__":
    run(None, None, sys.argv[1] if len(sys.argv) > 1 else "examples/company_dossier_sample.json")
