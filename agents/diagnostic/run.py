"""Run the Company Diagnostic agent.

Usage:
  python -m agents.diagnostic.run examples/company_dossier_sample.json
"""
import json
import sys
from pathlib import Path

from shared.llm import call_llm
from .metrics import compute_metrics
from .prompt import SYSTEM_PROMPT


def run(dossier_path: str) -> str:
    dossier = json.loads(Path(dossier_path).read_text())
    metrics = compute_metrics(dossier)
    user_msg = (
        "## Company dossier\n\n```json\n" + json.dumps(dossier, indent=2) + "\n```\n\n"
        "## Computed metrics (use exactly as given)\n\n```json\n" + json.dumps(metrics, indent=2) + "\n```"
    )
    report, m = call_llm(SYSTEM_PROMPT, user_msg, max_tokens=9000)
    report += (
        f"\n\n---\n_Run metrics: {m.seconds:.1f}s, "
        f"{m.input_tokens} in / {m.output_tokens} out tokens, ~${m.cost_usd}_\n"
    )
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "diagnostic_report.md"
    out.write_text(report)
    print(report)
    print(f"\nSaved to {out}")
    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m agents.diagnostic.run <company_dossier.json>")
    run(sys.argv[1])
