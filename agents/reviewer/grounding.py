"""Deterministic number-grounding check. Code does this, not the model.

Finds dollar figures (>= $1,000) in each stage report and checks whether each one traces to:
  - the source dossier, computed metrics or computed pricing scenarios (also x12 and /12 conversions), or
  - a figure that already appeared in an EARLIER stage report.
Anything else is returned as a figure to verify. These are flags, not errors: a labeled
estimate is legitimate, but a human should confirm it.
"""
import re

SUFFIX = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9}
MONEY = re.compile(r"\$\s?(\d[\d,]*(?:\.\d+)?)(?:\s?(million|thousand|billion)|([KkMmBb])(?![A-Za-z]))?")
TOLERANCE = 0.02  # 2% to allow rounding ($295K vs $294,540)


def money_figures(text: str):
    out = []
    for m in MONEY.finditer(text):
        num = float(m.group(1).replace(",", ""))
        suffix = (m.group(2) or m.group(3) or "").lower()
        val = num * SUFFIX.get(suffix, 1)
        if val >= 1000:
            s, e = max(0, m.start() - 60), min(len(text), m.end() + 60)
            out.append((val, " ".join(text[s:e].split())))
    return out


def numeric_leaves(obj):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        yield float(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from numeric_leaves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from numeric_leaves(v)


def _variants(v: float):
    v = abs(v)
    yield v
    if v:
        yield v * 12
        yield v / 12


def _is_grounded(val: float, allowed) -> bool:
    return any(abs(val - a) <= TOLERANCE * max(a, 1.0) for a in allowed)


def find_ungrounded(reports: dict, source_objects: list, per_stage_limit: int = 15) -> dict:
    allowed = set()
    for obj in source_objects:
        for leaf in numeric_leaves(obj):
            allowed.update(_variants(leaf))

    result = {}
    for stage, text in reports.items():
        figs = money_figures(text)
        flagged, seen = [], set()
        for val, ctx in figs:
            key = round(val)
            if key in seen:
                continue
            seen.add(key)
            if not _is_grounded(val, allowed):
                flagged.append({"figure_usd": round(val), "context": ctx})
        if flagged:
            result[stage] = flagged[:per_stage_limit]
        for val, _ in figs:  # later stages may restate this stage's figures
            allowed.update(_variants(val))
    return result
