"""Run the Delivery agent.

Usage:
  python -m agents.delivery.run                                  # uses outputs/prd_item_1.md
  python -m agents.delivery.run outputs/prd_item_1.md examples/context_sample.json
"""
import sys
from pathlib import Path

from shared.agent import run_agent, read_optional
from .prompt import SYSTEM_PROMPT


def run(prd_path: str = "outputs/prd_item_1.md", context_path: str | None = None) -> str:
    msg = "## PRD\n\n" + Path(prd_path).read_text()
    ctx = read_optional(context_path)
    if ctx:
        msg += "\n\n## Team and business context\n\n" + ctx
    return run_agent(SYSTEM_PROMPT, msg, "delivery_plan.md", max_tokens=6000)


if __name__ == "__main__":
    run(*sys.argv[1:3])
