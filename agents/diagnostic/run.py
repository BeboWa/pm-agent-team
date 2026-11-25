"""Run the Company Diagnostic agent.

Usage:
  python -m agents.diagnostic.run examples/company_dossier_sample.json
"""
import json
import sys
from pathlib import Path

from shared.agent import run_agent
from .metrics import compute_metrics
from .prompt import SYSTEM_PROMPT


def run(dossier_path: str) -> str:
    dossier = json.loads(Path(dossier_path).read_text())
    metrics = compute_metrics(dossier)
    user_msg = (
        "## Company dossier\n\n```json\n" + json.dumps(dossier, indent=2) + "\n```\n\n"
        "## Computed metrics (use exactly as given)\n\n```json\n" + json.dumps(metrics, indent=2) + "\n```"
    )
    return run_agent(SYSTEM_PROMPT, user_msg, "diagnostic_report.md", max_tokens=9000)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m agents.diagnostic.run <company_dossier.json>")
    run(sys.argv[1])
