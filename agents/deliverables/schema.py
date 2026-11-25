"""Parse and validate the Presenter's JSON. Code decides whether it is usable."""
from __future__ import annotations
import json
import re

SLOTS = ["diagnosis", "leaks", "bets", "pricing", "plan", "decisions", "risks"]


def parse_json(text: str) -> dict:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    start, end = t.find("{"), t.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in the Presenter output")
    return json.loads(t[start:end + 1])


def validate(deck: dict):
    """Return (deck, warnings). Raises ValueError if the deck is unusable."""
    warnings = []
    for key in ("title", "subtitle", "slides", "objections"):
        if key not in deck:
            raise ValueError(f"Deck JSON is missing '{key}'")
    by_slot = {s.get("slot"): s for s in deck["slides"] if isinstance(s, dict)}
    missing = [s for s in SLOTS if s not in by_slot]
    if missing:
        raise ValueError("Deck JSON is missing slides: " + ", ".join(missing))

    ordered = []
    for slot in SLOTS:
        s = by_slot[slot]
        if not isinstance(s.get("title"), str) or not s["title"].strip():
            raise ValueError(f"Slide '{slot}' has no title")
        bullets = s.get("bullets")
        if not isinstance(bullets, list) or not all(isinstance(b, str) for b in bullets) or not bullets:
            raise ValueError(f"Slide '{slot}' needs a list of text bullets")
        if len(bullets) > 6:
            warnings.append(f"Slide '{slot}' has {len(bullets)} bullets (target 3 to 5)")
        for b in bullets:
            if len(b.split()) > 28:
                warnings.append(f"Slide '{slot}' has a long bullet ({len(b.split())} words): {b[:50]}...")
        s.setdefault("notes", "")
        ordered.append(s)
    deck["slides"] = ordered

    objs = [o for o in deck["objections"] if isinstance(o, dict) and o.get("objection") and o.get("answer")]
    if len(objs) < 3:
        warnings.append("Fewer than 3 usable objections were returned")
    deck["objections"] = objs
    deck.setdefault("validation_items", [])
    return deck, warnings


def deck_text(deck: dict) -> str:
    parts = [deck["title"], deck["subtitle"]]
    for s in deck["slides"]:
        parts.append(s["title"])
        parts.extend(s["bullets"])
    return "\n".join(parts)
