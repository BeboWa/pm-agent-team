"""Check a company dossier before the pipeline runs on it.

Catches arithmetic that does not add up, impossible values, and personal data that should
never be in an aggregate dossier. Errors block the run; warnings are shown and the run continues.

Usage:
  python -m intake.validate path/to/dossier.json
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REQUIRED_NUMBERS = [
    "mrr_start", "new_mrr", "expansion_mrr", "contraction_mrr", "churned_mrr", "mrr_end",
    "customers_start", "new_customers", "churned_customers", "customers_end", "gross_margin",
]
FRACTIONS = ["gross_margin", "involuntary_churn_share", "discounted_deal_share", "avg_discount", "annual_plan_share"]
RECOMMENDED = {
    "involuntary_churn_share": "the pricing and billing recovery scenarios will be skipped",
    "discounted_deal_share": "the discount scenarios will be skipped",
    "avg_discount": "the discount scenarios will be skipped",
    "annual_plan_share": "the annual-plan scenarios will be skipped",
    "blended_cac": "CAC payback and LTV:CAC cannot be computed",
    "funnel": "funnel conversion cannot be computed",
}

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<!\d)(?:\+?\d{1,2}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
CARD = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")


def _luhn(digits: str) -> bool:
    total, flip = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if flip:
            d *= 2
            d -= 9 if d > 9 else 0
        total += d
        flip = not flip
    return total % 10 == 0


def _strings(obj, path=""):
    """Yield (path, text) for every string value, skipping keys that start with an underscore."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).startswith("_"):
                yield from _strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _strings(v, f"{path}[{i}]")


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate_dossier(d: dict) -> dict:
    errors, warnings = [], []

    if not isinstance(d.get("company"), str) or not d["company"].strip():
        errors.append("'company' is required (a name for the report).")

    for k in REQUIRED_NUMBERS:
        if k not in d:
            errors.append(f"'{k}' is required.")
        elif not _is_num(d[k]):
            errors.append(f"'{k}' must be a number.")
        elif d[k] < 0:
            errors.append(f"'{k}' cannot be negative.")

    for k in FRACTIONS:
        v = d.get(k)
        if v is None or not _is_num(v):
            continue
        if v > 1:
            errors.append(f"'{k}' must be a fraction between 0 and 1 (for example 0.4 for 40%), got {v}.")
        elif v < 0:
            errors.append(f"'{k}' cannot be negative.")

    if not isinstance(d.get("pricing"), list) or not d.get("pricing"):
        errors.append("'pricing' needs at least one tier (name and monthly price).")

    for k, why in RECOMMENDED.items():
        if k not in d or d[k] in (None, "", {}):
            warnings.append(f"'{k}' is missing: {why}.")

    # Revenue bridge: start + new + expansion - contraction - churn = end
    if all(_is_num(d.get(k)) for k in ("mrr_start", "new_mrr", "expansion_mrr", "contraction_mrr", "churned_mrr", "mrr_end")):
        expected = d["mrr_start"] + d["new_mrr"] + d["expansion_mrr"] - d["contraction_mrr"] - d["churned_mrr"]
        diff = abs(expected - d["mrr_end"])
        if diff > max(0.01 * d["mrr_end"], 1):
            errors.append(f"MRR does not add up: start + new + expansion - contraction - churned = {expected:,.0f}, but mrr_end is {d['mrr_end']:,.0f}.")
        elif diff > 1:
            warnings.append(f"MRR is off by {diff:,.0f} (under 1%). Fine if due to rounding.")

    # Customer bridge
    if all(_is_num(d.get(k)) for k in ("customers_start", "new_customers", "churned_customers", "customers_end")):
        expected = d["customers_start"] + d["new_customers"] - d["churned_customers"]
        diff = abs(expected - d["customers_end"])
        if diff > max(0.01 * d["customers_end"], 2):
            errors.append(f"Customers do not add up: start + new - churned = {expected:,.0f}, but customers_end is {d['customers_end']:,.0f}.")

    # CAC consistency
    sm, nc, cac = d.get("sales_marketing_spend"), d.get("new_customers"), d.get("blended_cac")
    if _is_num(sm) and _is_num(nc) and _is_num(cac) and nc:
        exp = sm / nc
        if abs(cac - exp) / exp > 0.05:
            warnings.append(f"blended_cac ({cac:,.0f}) differs from sales_marketing_spend / new_customers ({exp:,.0f}) by more than 5%.")

    # Funnel
    f = d.get("funnel")
    if isinstance(f, dict):
        steps = [(k, f.get(k)) for k in ("visitors", "signups", "activated", "paid") if _is_num(f.get(k))]
        for (a, av), (b, bv) in zip(steps, steps[1:]):
            if bv > av:
                errors.append(f"Funnel is not decreasing: {b} ({bv:,}) is larger than {a} ({av:,}).")
        if _is_num(f.get("paid")) and _is_num(nc) and nc and abs(f["paid"] - nc) / nc > 0.25:
            warnings.append(f"funnel.paid ({f['paid']:,}) and new_customers ({nc:,}) differ by more than 25%. Check they cover the same period.")

    # Personal data scan: aggregate dossiers must not contain any
    for path, text in _strings(d):
        if EMAIL.search(text):
            errors.append(f"Possible email address in '{path}'. Remove personal data; only aggregate figures belong here.")
        if SSN.search(text):
            errors.append(f"Possible government ID number in '{path}'. Remove it.")
        if any(_luhn(re.sub(r"\D", "", m.group())) for m in CARD.finditer(text) if 13 <= len(re.sub(r"\D", "", m.group())) <= 19):
            errors.append(f"Possible payment card number in '{path}'. Remove it.")
        if PHONE.search(text):
            errors.append(f"Possible phone number in '{path}'. Remove personal data.")
        if len(text) > 400:
            warnings.append(f"'{path}' is long ({len(text)} characters). Keep notes short and free of customer names.")

    # Consent record (required for real client data; synthetic samples are exempt)
    intake = d.get("_intake")
    synthetic = "synthetic" in str(d.get("_note", "")).lower()
    if not synthetic and not (isinstance(intake, dict) and intake.get("consent") is True):
        warnings.append("No consent record (_intake.consent). For real client data, get written permission first.")

    return {"errors": errors, "warnings": warnings}


def validate_file(path: str) -> dict:
    return validate_dossier(json.loads(Path(path).read_text()))


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m intake.validate <dossier.json>")
        return 2
    res = validate_file(argv[0])
    for e in res["errors"]:
        print(f"ERROR:   {e}")
    for w in res["warnings"]:
        print(f"warning: {w}")
    if not res["errors"] and not res["warnings"]:
        print("OK: no problems found.")
    elif not res["errors"]:
        print("OK to run (warnings only).")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
