"""Run the PRD agent.

Usage:
  python -m agents.prd.run                                   # top item from outputs/prioritization_report.md
  python -m agents.prd.run examples/prioritization_report_sample.md
  python -m agents.prd.run <report.md> --item 2              # PRD for the 2nd ranked item
  python -m agents.prd.run <report.md> --context examples/context_sample.json
"""
from __future__ import annotations
import argparse
from pathlib import Path

from shared.llm import call_llm
from .prompt import SYSTEM_PROMPT


def run(report_path: str = "outputs/prioritization_report.md", item: int = 1, context_path: str | None = None) -> str:
    report = Path(report_path).read_text()
    user_msg = (
        f"Write a PRD for roadmap item #{item} (by rank) from the Prioritization report below.\n\n"
        "## Prioritization report\n\n" + report
    )
    if context_path:
        user_msg += "\n\n## Business context\n\n" + Path(context_path).read_text()

    prd, m = call_llm(SYSTEM_PROMPT, user_msg, max_tokens=6000)
    prd += (
        f"\n\n---\n_Run metrics: {m.seconds:.1f}s, "
        f"{m.input_tokens} in / {m.output_tokens} out tokens, ~${m.cost_usd}_\n"
    )
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"prd_item_{item}.md"
    out.write_text(prd)
    print(prd)
    print(f"\nSaved to {out}")
    return prd


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("report", nargs="?", default="outputs/prioritization_report.md")
    ap.add_argument("--item", type=int, default=1)
    ap.add_argument("--context", default=None)
    a = ap.parse_args()
    run(a.report, a.item, a.context)
