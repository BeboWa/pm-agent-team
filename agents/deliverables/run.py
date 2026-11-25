"""Build the client deliverables: deck, report document, and your private prep sheet.

Usage:
  python -m agents.deliverables.run examples/company_dossier_sample.json            # uses reports in outputs/
  python -m agents.deliverables.run examples/company_dossier_sample.json --rebuild  # re-render from your edited outputs/deliverables/deck.json (no model call)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from shared.llm import call_llm
from shared.outputs import load_outputs
from shared.paths import out_dir, out_file
from agents.diagnostic.metrics import compute_metrics
from agents.pricing_billing.pricing_math import pricing_scenarios
from agents.reviewer.grounding import find_ungrounded
from .deck import build_deck
from .docx_builder import build_docx
from .prompt import SYSTEM_PROMPT
from .schema import deck_text, parse_json, validate

PRESENTER_STAGES = ["Executive Brief", "Company Diagnostic", "Pricing & Billing", "Prioritization"]


def _load_all() -> tuple:
    reports = load_outputs()
    for name, fname in (("Executive Brief", "executive_brief.md"),):
        p = out_file(fname)
        if p.exists():
            reports[name] = p.read_text()
    rp = out_file("review_report.md")
    return reports, (rp.read_text() if rp.exists() else "(No review available.)")


def _presenter(company: str, metrics: dict, scenarios: dict, reports: dict, review: str) -> dict:
    msg = (
        f"## Company\n\n{company}\n\n"
        "## Computed metrics (ground truth)\n\n```json\n" + json.dumps(metrics, indent=2) + "\n```\n\n"
        "## Computed pricing scenarios (ground truth)\n\n```json\n" + json.dumps(scenarios, indent=2) + "\n```\n\n"
        "## Reviewer report (internal)\n\n" + review + "\n\n## Reports\n"
    )
    for name in PRESENTER_STAGES:
        if name in reports:
            msg += f"\n### {name}\n\n{reports[name]}\n"
    last_err = None
    for attempt in range(2):
        text, _ = call_llm(SYSTEM_PROMPT, msg + ("\n\nReturn valid JSON only." if attempt else ""), max_tokens=7000)
        try:
            return parse_json(text)
        except (ValueError, json.JSONDecodeError) as e:
            last_err = e
    raise ValueError(f"The Presenter did not return valid JSON: {last_err}")


def _prep_sheet(deck: dict, ungrounded: list, warnings: list) -> str:
    lines = ["# Readout prep (private, for you only)", "",
             "Do not send this file to the client.", "",
             "## Before you present: verify these", ""]
    items = list(deck.get("validation_items", []))
    for f in ungrounded:
        items.append(f"Deck figure ${f['figure_usd']:,} was not found in the source data or earlier reports. Context: {f['context']}")
    items += warnings
    lines += [f"- {x}" for x in items] or ["- Nothing flagged. Still read every slide."]
    lines += ["", "## Talk track", ""]
    for i, s in enumerate(deck["slides"], 1):
        lines += [f"**Slide: {s['title']}**", "", s.get("notes", "") or "(no notes)", ""]
    lines += ["## Likely objections and suggested answers", ""]
    for o in deck["objections"]:
        lines += [f"**Objection:** {o['objection']}", "", f"**Suggested answer:** {o['answer']}", ""]
    return "\n".join(lines)


def run(reports: dict | None = None, review_text: str | None = None,
        dossier_path: str = "examples/company_dossier_sample.json", rebuild: bool = False) -> str:
    dossier = json.loads(Path(dossier_path).read_text())
    company = dossier.get("company", "Company")
    metrics, scenarios = compute_metrics(dossier), pricing_scenarios(dossier)
    deliver_dir = out_dir() / "deliverables"
    deliver_dir.mkdir(parents=True, exist_ok=True)
    json_path = deliver_dir / "deck.json"

    if reports is None:
        reports, loaded_review = _load_all()
        review_text = review_text or loaded_review
    if not reports and not rebuild:
        sys.exit("No stage reports found in outputs/. Run the pipeline first.")

    if rebuild:
        if not json_path.exists():
            sys.exit(f"{json_path} not found. Run without --rebuild first.")
        deck = parse_json(json_path.read_text())
    else:
        deck = _presenter(company, metrics, scenarios, reports, review_text or "")
    deck, warnings = validate(deck)
    json_path.write_text(json.dumps(deck, indent=2))

    flagged = find_ungrounded({**reports, "Deck": deck_text(deck)}, [dossier, metrics, scenarios]).get("Deck", []) if reports else []

    build_deck(deck, metrics, company, str(deliver_dir / "deck.pptx"))
    build_docx(reports, company, str(deliver_dir / "report.docx")) if reports else None
    (deliver_dir / "readout_prep.md").write_text(_prep_sheet(deck, flagged, warnings))

    lines = ["# Deliverables built", "",
             f"- {deliver_dir}/deck.pptx: {len(deck['slides']) + 3} slides with speaker notes (client-facing)",
             f"- {deliver_dir}/report.docx: full report (client-facing)",
             f"- {deliver_dir}/readout_prep.md: figures to verify, talk track, objections (private)",
             f"- {deliver_dir}/deck.json: editable deck content (edit, then run with --rebuild)", ""]
    if flagged:
        lines.append(f"Heads up: {len(flagged)} dollar figure(s) in the deck were not found in the sources. See readout_prep.md.")
    for w in warnings:
        lines.append(f"Warning: {w}")
    out = "\n".join(lines) + "\n"
    print(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier", nargs="?", default="examples/company_dossier_sample.json")
    ap.add_argument("--rebuild", action="store_true", help="Re-render from outputs/deliverables/deck.json without calling the model")
    a = ap.parse_args()
    run(None, None, a.dossier, a.rebuild)
