"""Run the Discovery agent: python -m agents.discovery.run examples/feedback_sample.json"""
import json
import sys
from pathlib import Path

from shared.llm import call_llm
from .prompt import SYSTEM_PROMPT


def run(feedback_path: str) -> str:
    items = json.loads(Path(feedback_path).read_text())
    user_msg = "Customer feedback items:\n\n" + "\n".join(
        f"[{i['id']}] ({i.get('source', 'unknown')}, segment: {i.get('segment', 'n/a')}) {i['text']}"
        for i in items
    )
    report, m = call_llm(SYSTEM_PROMPT, user_msg)
    report += (
        f"\n\n---\n_Run metrics: {m.seconds:.1f}s, "
        f"{m.input_tokens} in / {m.output_tokens} out tokens, ~${m.cost_usd}_\n"
    )
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "discovery_report.md"
    out.write_text(report)
    print(report)
    print(f"\nSaved to {out}")
    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m agents.discovery.run <feedback.json>")
    run(sys.argv[1])
