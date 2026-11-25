"""Run the Discovery agent: python -m agents.discovery.run examples/feedback_sample.json"""
import json
import sys
from pathlib import Path

from shared.agent import run_agent
from .prompt import SYSTEM_PROMPT


def run(feedback_path: str) -> str:
    items = json.loads(Path(feedback_path).read_text())
    user_msg = "Customer feedback items:\n\n" + "\n".join(
        f"[{i['id']}] ({i.get('source', 'unknown')}, segment: {i.get('segment', 'n/a')}) {i['text']}"
        for i in items
    )
    return run_agent(SYSTEM_PROMPT, user_msg, "discovery_report.md", max_tokens=5000)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m agents.discovery.run <feedback.json>")
    run(sys.argv[1])
