"""Where each stage writes its report, in pipeline order."""
from __future__ import annotations
from pathlib import Path

from shared.paths import out_dir

STAGE_FILES = [
    ("Company Diagnostic", "diagnostic_report.md"),
    ("Pricing & Billing", "pricing_billing_report.md"),
    ("Discovery", "discovery_report.md"),
    ("Prioritization", "prioritization_report.md"),
    ("PRD", "prd_item_1.md"),
    ("Delivery", "delivery_plan.md"),
    ("Launch / GTM", "launch_plan.md"),
    ("Analytics", "analytics_plan.md"),
]


def load_outputs(folder: str | None = None) -> dict:
    """Load whichever stage reports exist in the current output folder, in pipeline order."""
    base = Path(folder) if folder else out_dir()
    found = {}
    for name, fname in STAGE_FILES:
        p = base / fname
        if p.exists():
            found[name] = p.read_text()
    return found
