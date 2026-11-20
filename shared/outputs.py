"""Where each stage writes its report, in pipeline order."""
from pathlib import Path

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


def load_outputs(folder: str = "outputs") -> dict:
    """Load whichever stage reports exist, in pipeline order."""
    found = {}
    for name, fname in STAGE_FILES:
        p = Path(folder) / fname
        if p.exists():
            found[name] = p.read_text()
    return found
