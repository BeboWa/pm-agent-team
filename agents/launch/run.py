"""Run the Launch / GTM agent.

Usage:
  python -m agents.launch.run                                     # uses outputs/prd_item_1.md
  python -m agents.launch.run outputs/prd_item_1.md outputs/diagnostic_report.md
"""
from __future__ import annotations
import sys
from pathlib import Path

from shared.agent import run_agent, read_optional
from .prompt import SYSTEM_PROMPT


def run(prd_path: str = "outputs/prd_item_1.md", diagnostic_path: str | None = None) -> str:
    msg = "## PRD\n\n" + Path(prd_path).read_text()
    diag = read_optional(diagnostic_path)
    if diag:
        msg += "\n\n## Company Diagnostic report (context)\n\n" + diag
    return run_agent(SYSTEM_PROMPT, msg, "launch_plan.md", max_tokens=6000)


if __name__ == "__main__":
    run(*sys.argv[1:3])
