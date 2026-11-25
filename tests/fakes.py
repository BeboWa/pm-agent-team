"""A fake Anthropic client so tests never call the real API."""
import json
import types

HEADINGS = "\n".join([
    "## 1. Business Model Snapshot", "## 2. Health Scorecard", "## 3. The Revenue Equation", "## 4. Leaks and Levers",
    "## 5. Monetization Opportunities", "## 6. Top 3 Strategic Bets", "## 7. Data Gaps", "## 9. Handoff to Prioritization",
    "## 1. Current Monetization Model", "## 2. Scenario Math", "## 3. Recommended Pricing and Packaging Changes",
    "## 4. Billing and Payments Implications", "## 5. Migration and Rollout", "## 6. Test Plan and Risks",
    "## Top Themes", "## Evidence by Theme", "## Segments Affected", "## Open Questions",
    "## Ranked Opportunities", "## Scoring Rationale", "## Roadmap: Now / Next / Later", "## Not Doing", "## Risks and What Would Change",
    "## 1. Problem and Evidence", "## 2. Goals and Non-Goals", "## 3. Target Users", "## 4. Requirements", "## 5. User Stories",
    "## 6. Success Metrics", "## 7. Risks", "## 8. Rollout Plan",
    "## Backlog", "## Dependencies and Critical Path", "## Sprint Plan", "## Risks and Mitigations", "## Stakeholder Status Update",
    "## Positioning", "## Messaging by Audience", "## Release Notes", "## Launch Plan and Checklist",
    "## Sales and Support Enablement", "## Launch Risks",
    "## Metric Framework", "## Tracking Plan", "## Experiment Design", "## Decision Rules", "## Readout Template", "## Feedback Loop",
    "## Overall Verdict", "## Stage-by-Stage Review", "## Cross-Stage Consistency", "## Figures to Verify", "## Top Issues for the Human",
    "# Executive Brief", "## The Diagnosis", "## Top 3 Bets", "## 30/60/90-Day Plan", "## Decisions Needed", "## Key Risks",
    "## Needs Human Validation",
])

SLOTS = ["diagnosis", "leaks", "bets", "pricing", "plan", "decisions", "risks"]


def presenter_json():
    return json.dumps({
        "title": "Deck title", "subtitle": "Subtitle",
        "slides": [{"slot": s, "title": f"Title for {s}", "bullets": ["Point one about $456K.", "Point two.", "Point three."],
                    "notes": f"Notes for {s}"} for s in SLOTS],
        "objections": [{"objection": f"Q{i}", "answer": "A"} for i in range(4)],
        "validation_items": ["Check X"],
    })


class FakeClient:
    """Returns schema-correct text for every agent. Records every call."""
    calls = []

    def __init__(self, *a, **k):
        self.messages = types.SimpleNamespace(create=self._create)

    def _create(self, **kw):
        FakeClient.calls.append(kw)
        text = presenter_json() if kw["system"].startswith("You are the Presenter") else HEADINGS
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(type="text", text=text)],
            stop_reason="end_turn",
            usage=types.SimpleNamespace(input_tokens=1000, output_tokens=700),
        )
