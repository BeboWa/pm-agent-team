"""Run the Analytics agent.

Usage:
  python -m agents.analytics.run                                              # uses outputs/prd_item_1.md
  python -m agents.analytics.run outputs/prd_item_1.md --baseline 0.208 --mde 0.10
  python -m agents.analytics.run outputs/prd_item_1.md --diagnostic outputs/diagnostic_report.md
"""
import argparse
import json
from pathlib import Path

from shared.agent import run_agent, read_optional
from .prompt import SYSTEM_PROMPT
from .stats import sample_size_per_arm


def run(prd_path: str = "outputs/prd_item_1.md", diagnostic_path: str | None = None,
        baseline: float | None = None, mde: float | None = None) -> str:
    msg = "## PRD\n\n" + Path(prd_path).read_text()
    diag = read_optional(diagnostic_path)
    if diag:
        msg += "\n\n## Company Diagnostic report (context)\n\n" + diag
    if baseline is not None and mde is not None:
        calc = sample_size_per_arm(baseline, mde)
        msg += "\n\n## Computed sample size (use exactly as given)\n\n```json\n" + json.dumps(calc, indent=2) + "\n```"
    return run_agent(SYSTEM_PROMPT, msg, "analytics_plan.md", max_tokens=6000)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prd", nargs="?", default="outputs/prd_item_1.md")
    ap.add_argument("--diagnostic", default=None)
    ap.add_argument("--baseline", type=float, default=None, help="baseline conversion rate, e.g. 0.208")
    ap.add_argument("--mde", type=float, default=None, help="relative minimum detectable effect, e.g. 0.10")
    a = ap.parse_args()
    run(a.prd, a.diagnostic, a.baseline, a.mde)
