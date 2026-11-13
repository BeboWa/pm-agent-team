"""Deterministic SaaS metrics. The LLM interprets these; it does not calculate them."""


def _div(a, b):
    try:
        return a / b if b else None
    except TypeError:
        return None


def compute_metrics(d: dict) -> dict:
    m = {}
    start = d.get("mrr_start")
    end = d.get("mrr_end")
    exp = d.get("expansion_mrr", 0) or 0
    con = d.get("contraction_mrr", 0) or 0
    churn = d.get("churned_mrr", 0) or 0
    new = d.get("new_mrr", 0) or 0

    if end is not None:
        m["arr_end"] = end * 12
    if start and end is not None:
        m["arr_growth_pct"] = round((end - start) / start * 100, 1)
        m["nrr_pct"] = round((start + exp - con - churn) / start * 100, 1)
        m["grr_pct"] = round((start - con - churn) / start * 100, 1)
        m["mrr_bridge_check"] = start + new + exp - con - churn - end  # should be 0
    if start:
        m["churned_mrr_pct_of_start"] = round(churn / start * 100, 1)
        m["expansion_mrr_pct_of_start"] = round(exp / start * 100, 1)

    share = d.get("involuntary_churn_share")
    if share is not None and churn:
        m["involuntary_churned_mrr"] = round(churn * share)
        m["involuntary_churn_annualized_arr_at_risk"] = round(churn * share * 12)

    cs, ce = d.get("customers_start"), d.get("customers_end")
    cc = d.get("churned_customers")
    if ce and end:
        m["arpa_monthly"] = round(end / ce, 1)
    if cs and cc is not None:
        m["logo_churn_pct"] = round(cc / cs * 100, 1)

    cac = d.get("blended_cac")
    gm = d.get("gross_margin")
    arpa = m.get("arpa_monthly")
    if cac and arpa and gm:
        m["cac_payback_months"] = round(cac / (arpa * gm), 1)
        monthly_churn = d.get("monthly_logo_churn")
        if monthly_churn is None and m.get("logo_churn_pct") is not None:
            monthly_churn = (m["logo_churn_pct"] / 100) / 12
        if monthly_churn:
            m["ltv"] = round(arpa * gm / monthly_churn)
            m["ltv_to_cac"] = round(m["ltv"] / cac, 1)

    f = d.get("funnel") or {}
    if f.get("visitors") and f.get("signups"):
        m["visitor_to_signup_pct"] = round(f["signups"] / f["visitors"] * 100, 2)
    if f.get("signups") and f.get("activated"):
        m["signup_to_activated_pct"] = round(f["activated"] / f["signups"] * 100, 1)
    if f.get("activated") and f.get("paid"):
        m["activated_to_paid_pct"] = round(f["paid"] / f["activated"] * 100, 1)
    return m
