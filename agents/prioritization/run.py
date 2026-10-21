"""Run the Prioritization agent.

Usage:
  python -m agents.prioritization.run                              # uses outputs/discovery_report.md
  python -m agents.prioritization.run examples/discovery_report_sample.md
  python -m agents.prioritization.run <report.md> examples/context_sample.json
"""
import sys
from pathlib import Path

from shared.llm import call_llm
from .prompt import SYSTEM_PROMPT


def run(report_path: str = "outputs/discovery_report.md", context_path: str | None = None) -> str:
    report = Path(report_path).read_text()
    user_msg = "## Discovery report\n\n" + report
    if context_path:
        user_msg += "\n\n## Business context\n\n" + Path(context_path).read_text()

    result, m = call_llm(SYSTEM_PROMPT, user_msg, max_tokens=5000)
    result += (
        f"\n\n---\n_Run metrics: {m.seconds:.1f}s, "
        f"{m.input_tokens} in / {m.output_tokens} out tokens, ~${m.cost_usd}_\n"
    )
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "prioritization_report.md"
    out.write_text(result)
    print(result)
    print(f"\nSaved to {out}")
    return result


if __name__ == "__main__":
    args = sys.argv[1:]
    run(*(args[:2]))
