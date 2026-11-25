"""Run the Prioritization agent.

Usage:
  python -m agents.prioritization.run                              # uses discovery_report.md in the output folder
  python -m agents.prioritization.run examples/discovery_report_sample.md
  python -m agents.prioritization.run outputs/diagnostic_report.md examples/context_sample.json
"""
from __future__ import annotations
import sys
from pathlib import Path

from shared.agent import run_agent, read_optional
from shared.paths import out_file
from .prompt import SYSTEM_PROMPT


def run(report_path: str | None = None, context_path: str | None = None) -> str:
    report = Path(report_path or out_file("discovery_report.md")).read_text()
    user_msg = "## Input report\n\n" + report
    ctx = read_optional(context_path)
    if ctx:
        user_msg += "\n\n## Business context\n\n" + ctx
    return run_agent(SYSTEM_PROMPT, user_msg, "prioritization_report.md", max_tokens=7000)


if __name__ == "__main__":
    args = sys.argv[1:]
    run(*(args[:2]))
