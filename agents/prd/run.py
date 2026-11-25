"""Run the PRD agent.

Usage:
  python -m agents.prd.run                                   # top item from prioritization_report.md in the output folder
  python -m agents.prd.run examples/prioritization_report_sample.md
  python -m agents.prd.run <report.md> --item 2              # PRD for the 2nd ranked item
  python -m agents.prd.run <report.md> --context examples/context_sample.json
"""
from __future__ import annotations
import argparse
from pathlib import Path

from shared.agent import run_agent, read_optional
from shared.paths import out_file
from .prompt import SYSTEM_PROMPT


def run(report_path: str | None = None, item: int = 1, context_path: str | None = None) -> str:
    report = Path(report_path or out_file("prioritization_report.md")).read_text()
    user_msg = (
        f"Write a PRD for roadmap item #{item} (by rank) from the Prioritization report below.\n\n"
        "## Prioritization report\n\n" + report
    )
    ctx = read_optional(context_path)
    if ctx:
        user_msg += "\n\n## Business context\n\n" + ctx
    return run_agent(SYSTEM_PROMPT, user_msg, f"prd_item_{item}.md", max_tokens=8000)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("report", nargs="?", default=None)
    ap.add_argument("--item", type=int, default=1)
    ap.add_argument("--context", default=None)
    a = ap.parse_args()
    run(a.report, a.item, a.context)
