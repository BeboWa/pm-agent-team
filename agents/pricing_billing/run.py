"""Run the Pricing & Billing agent.

Usage:
  python -m agents.pricing_billing.run examples/company_dossier_sample.json
  python -m agents.pricing_billing.run examples/company_dossier_sample.json outputs/diagnostic_report.md
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

from shared.agent import run_agent, read_optional
from .pricing_math import pricing_scenarios
from .prompt import SYSTEM_PROMPT


def run(dossier_path: str, diagnostic_path: str | None = None) -> str:
    dossier = json.loads(Path(dossier_path).read_text())
    scenarios = pricing_scenarios(dossier)
    msg = (
        "## Company dossier\n\n```json\n" + json.dumps(dossier, indent=2) + "\n```\n\n"
        "## Computed scenario math (use exactly as given)\n\n```json\n" + json.dumps(scenarios, indent=2) + "\n```"
    )
    diag = read_optional(diagnostic_path)
    if diag:
        msg += "\n\n## Company Diagnostic report (context)\n\n" + diag
    return run_agent(SYSTEM_PROMPT, msg, "pricing_billing_report.md", max_tokens=16000)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python -m agents.pricing_billing.run <company_dossier.json> [diagnostic_report.md]")
    run(*sys.argv[1:3])
