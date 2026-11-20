"""Orchestrator: run the whole PM agent team in one command.

Usage:
  python -m agents.orchestrator.run examples/company_dossier_sample.json
  python -m agents.orchestrator.run examples/company_dossier_sample.json \
      --feedback examples/feedback_sample.json \
      --context examples/context_sample.json \
      --manual-minutes 240
  python -m agents.orchestrator.run examples/company_dossier_sample.json --full   # all 8 agents
"""
import argparse
import contextlib
import csv
import io
import json
import os
import sys
import time
from pathlib import Path

from shared import llm
from agents.diagnostic.run import run as run_diagnostic
from agents.discovery.run import run as run_discovery
from agents.pricing_billing.run import run as run_pricing
from agents.prioritization.run import run as run_prioritization
from agents.prd.run import run as run_prd
from agents.delivery.run import run as run_delivery
from agents.launch.run import run as run_launch
from agents.analytics.run import run as run_analytics
from agents.reviewer.run import run as run_reviewer
from agents.brief.run import run as run_brief

REQUIRED_SECTIONS = {
    "Company Diagnostic": ["Business Model Snapshot", "Health Scorecard", "Revenue Equation",
                           "Leaks and Levers", "Monetization", "Strategic Bets", "Data Gaps",
                           "Handoff to Prioritization"],
    "Pricing & Billing": ["Current Monetization Model", "Scenario Math", "Recommended Pricing and Packaging",
                          "Billing and Payments Implications", "Migration and Rollout", "Test Plan and Risks"],
    "Discovery": ["Top Themes", "Evidence by Theme", "Segments Affected", "Open Questions"],
    "Prioritization": ["Ranked Opportunities", "Scoring Rationale", "Now / Next / Later",
                       "Not Doing", "Risks"],
    "PRD": ["Problem and Evidence", "Goals and Non-Goals", "Target Users", "Requirements",
            "User Stories", "Success Metrics", "Risks", "Rollout"],
    "Delivery": ["Backlog", "Dependencies and Critical Path", "Sprint Plan", "Risks and Mitigations",
                 "Stakeholder Status Update"],
    "Launch / GTM": ["Positioning", "Messaging by Audience", "Release Notes", "Launch Plan and Checklist",
                     "Sales and Support Enablement", "Launch Risks"],
    "Analytics": ["Metric Framework", "Tracking Plan", "Experiment Design", "Decision Rules",
                  "Readout Template", "Feedback Loop"],
    "Reviewer": ["Overall Verdict", "Stage-by-Stage Review", "Cross-Stage Consistency",
                 "Figures to Verify", "Top Issues for the Human"],
    "Executive Brief": ["The Diagnosis", "Top 3 Bets", "30/60/90", "Decisions Needed", "Key Risks",
                        "Needs Human Validation"],
}


def missing_sections(stage_name: str, text: str) -> list:
    low = text.lower()
    return [s for s in REQUIRED_SECTIONS[stage_name] if s.lower() not in low]


def run_stage(index: int, total: int, name: str, fn, *args, **kwargs) -> dict:
    print(f"[{index}/{total}] {name} ...", flush=True)
    before = len(llm.RUN_LOG)
    start = time.time()
    with contextlib.redirect_stdout(io.StringIO()):  # keep the console readable
        output = fn(*args, **kwargs)
    elapsed = round(time.time() - start, 1)
    calls = llm.RUN_LOG[before:]
    rec = {
        "name": name,
        "seconds": elapsed,
        "input_tokens": sum(c.input_tokens for c in calls),
        "output_tokens": sum(c.output_tokens for c in calls),
        "cost": round(sum(c.cost_usd for c in calls), 4),
        "missing": missing_sections(name, output),
        "truncated": any(c.truncated for c in calls),
        "continuations": sum(c.continuations for c in calls),
        "output": output,
    }
    gate = "checks passed" if not rec["missing"] else "MISSING: " + ", ".join(rec["missing"])
    if rec["truncated"]:
        gate += " | TRUNCATED (output hit max_tokens even after continuing)"
    elif rec["continuations"]:
        gate += f" | auto-continued {rec['continuations']}x after hitting the length limit"
    print(f"      done in {elapsed}s, ${rec['cost']}, {gate}")
    return rec


def build_summary(company: str, stages: list, wall: float, manual_minutes) -> str:
    total_cost = round(sum(s["cost"] for s in stages), 4)
    total_in = sum(s["input_tokens"] for s in stages)
    total_out = sum(s["output_tokens"] for s in stages)
    lines = [
        f"# Pipeline summary: {company}",
        "",
        "| Stage | Time (s) | Tokens in / out | Cost (USD) | Quality gate |",
        "|---|---|---|---|---|",
    ]
    for s in stages:
        gate = "pass" if not s["missing"] else "missing: " + ", ".join(s["missing"])
        if s.get("truncated"):
            gate = ("TRUNCATED, end of report may be cut off" if not s["missing"]
                    else gate + " | TRUNCATED")
        elif s.get("continuations"):
            gate += f" (auto-continued {s['continuations']}x)"
        lines.append(f"| {s['name']} | {s['seconds']} | {s['input_tokens']} / {s['output_tokens']} | ${s['cost']} | {gate} |")
    lines += [
        f"| **Total** | **{round(wall, 1)}** | **{total_in} / {total_out}** | **${total_cost}** | |",
        "",
    ]
    if manual_minutes:
        saved = round(manual_minutes - wall / 60, 1)
        lines += [f"Manual baseline: {manual_minutes} min. Pipeline: {round(wall / 60, 1)} min. Time saved: about {saved} min.", ""]
    lines += [
        f"All stage reports are saved in: {Path('outputs').resolve()}",
        "",
        "_The quality gate checks structure only (are all required sections present). "
        "A human should review the substance. Everything here is a hypothesis to validate._",
    ]
    return "\n".join(lines) + "\n"


def log_to_evals(company: str, stages: list, wall: float, manual_minutes) -> None:
    path = Path("evals/results.csv")
    path.parent.mkdir(exist_ok=True)
    new = not path.exists()
    note = "quality gate: all passed" if not any(s["missing"] or s.get("truncated") for s in stages) else "quality gate: sections missing or output truncated"
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["agent", "task", "manual_minutes", "agent_seconds", "cost_usd", "quality_notes"])
        w.writerow(["pipeline", f"{company} full run ({len(stages)} stages)", manual_minutes or "", round(wall, 1),
                    round(sum(s["cost"] for s in stages), 4), note])


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the PM agent team end to end.")
    ap.add_argument("dossier", help="Company dossier JSON")
    ap.add_argument("--feedback", help="Optional customer feedback JSON (adds the Discovery stage)")
    ap.add_argument("--context", help="Optional business context JSON")
    ap.add_argument("--item", type=int, default=1, help="Which ranked item to write the PRD for (default 1)")
    ap.add_argument("--full", action="store_true",
                    help="Also run Pricing & Billing, Delivery, Launch / GTM, Analytics, then the Reviewer and Executive Brief")
    ap.add_argument("--baseline", type=float, help="Analytics: baseline conversion rate, e.g. 0.208")
    ap.add_argument("--mde", type=float, help="Analytics: relative minimum detectable effect, e.g. 0.10")
    ap.add_argument("--manual-minutes", type=float, help="How long this took you by hand, to compute time saved")
    ap.add_argument("--no-log", action="store_true", help="Do not append a row to evals/results.csv")
    a = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Run: export ANTHROPIC_API_KEY=your_key")

    company = json.loads(Path(a.dossier).read_text()).get("company", "company")
    total = 3 + (1 if a.feedback else 0) + (6 if a.full else 0)
    stages, i = [], 0
    wall_start = time.time()
    try:
        i += 1
        diag = run_stage(i, total, "Company Diagnostic", run_diagnostic, a.dossier)
        stages.append(diag)
        combined = "# Company Diagnostic report\n\n" + diag["output"]
        reports = {"Company Diagnostic": diag["output"]}

        if a.full:
            i += 1
            pricing = run_stage(i, total, "Pricing & Billing", run_pricing, a.dossier, "outputs/diagnostic_report.md")
            stages.append(pricing)
            reports["Pricing & Billing"] = pricing["output"]
            combined += "\n\n# Pricing & Billing report\n\n" + pricing["output"]

        if a.feedback:
            i += 1
            disc = run_stage(i, total, "Discovery", run_discovery, a.feedback)
            stages.append(disc)
            reports["Discovery"] = disc["output"]
            combined += "\n\n# Customer Discovery report\n\n" + disc["output"]

        prio_input = "outputs/diagnostic_report.md"
        if a.full or a.feedback:
            prio_input = "outputs/prioritization_input.md"
            Path("outputs").mkdir(exist_ok=True)
            Path(prio_input).write_text(combined)

        i += 1
        prio = run_stage(i, total, "Prioritization", run_prioritization, prio_input, a.context)
        stages.append(prio)
        reports["Prioritization"] = prio["output"]

        i += 1
        prd = run_stage(i, total, "PRD", run_prd, "outputs/prioritization_report.md", a.item, a.context)
        stages.append(prd)
        reports["PRD"] = prd["output"]
        prd_path = f"outputs/prd_item_{a.item}.md"

        if a.full:
            for name, fn, args in [
                ("Delivery", run_delivery, (prd_path, a.context)),
                ("Launch / GTM", run_launch, (prd_path, "outputs/diagnostic_report.md")),
                ("Analytics", run_analytics, (prd_path, "outputs/diagnostic_report.md", a.baseline, a.mde)),
            ]:
                i += 1
                rec = run_stage(i, total, name, fn, *args)
                stages.append(rec)
                reports[name] = rec["output"]

            i += 1
            review = run_stage(i, total, "Reviewer", run_reviewer, reports, a.dossier)
            stages.append(review)
            i += 1
            stages.append(run_stage(i, total, "Executive Brief", run_brief, reports, review["output"], a.dossier))
    except Exception as e:  # stop cleanly, show what finished
        print(f"\nPipeline stopped at stage {i}: {type(e).__name__}: {e}")
        print("Completed stages are saved in outputs/. Fix the issue and re-run.")
        sys.exit(1)

    wall = time.time() - wall_start
    summary = build_summary(company, stages, wall, a.manual_minutes)
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/pipeline_summary.md").write_text(summary)
    if not a.no_log:
        log_to_evals(company, stages, wall, a.manual_minutes)
    print("\n" + summary)
    print("Saved to outputs/pipeline_summary.md")


if __name__ == "__main__":
    main()
