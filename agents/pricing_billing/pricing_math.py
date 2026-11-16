"""Deterministic pricing scenarios. The LLM interprets these; it does not calculate them.

All scenario inputs that are not in the dossier are ILLUSTRATIVE ASSUMPTIONS and are labeled as such.
"""


def pricing_scenarios(d: dict) -> dict:
    out = {"assumptions": []}

    # 1) Involuntary churn recovery (failed payments)
    churn, share = d.get("churned_mrr"), d.get("involuntary_churn_share")
    if churn and share is not None:
        lost = churn * share
        out["involuntary_mrr_lost_in_period"] = round(lost)
        out["involuntary_recovery"] = [
            {"recovery_rate_pct": r, "recovered_mrr": round(lost * r / 100),
             "annualized_arr": round(lost * r / 100 * 12)} for r in (20, 35, 50)
        ]
        out["assumptions"].append("Recovery rates of 20/35/50% of involuntary churn are illustrative, not benchmarks.")

    # 2) Price increase vs. extra churn
    mrr_end = d.get("mrr_end")
    if mrr_end:
        rows = []
        for inc in (5, 10):
            for loss in (1, 3, 5):
                new = mrr_end * (1 + inc / 100) * (1 - loss / 100)
                rows.append({"price_increase_pct": inc, "extra_churn_pct_of_base": loss,
                             "net_mrr_change": round(new - mrr_end),
                             "net_arr_change": round((new - mrr_end) * 12)})
        out["price_increase"] = rows
        out["assumptions"].append("Price increase applied to the whole base; extra churn rates of 1/3/5% are illustrative. Real elasticity differs by tier and must be tested.")

    # 3) Discount leakage and break-even
    new_mrr, ds, disc = d.get("new_mrr"), d.get("discounted_deal_share"), d.get("avg_discount")
    if new_mrr and ds is not None and disc is not None:
        gross = new_mrr / (1 - ds * disc)  # new MRR at list price
        out["new_mrr_at_list_price"] = round(gross)
        out["discount_leakage_mrr"] = round(gross - new_mrr)
        out["discount_leakage_annualized_arr"] = round((gross - new_mrr) * 12)
        rows = []
        for cut in (25, 50):
            for lost in (0, 10, 20):
                # discounted deals' list MRR = gross*ds; removing discount on `cut`% of them:
                net = gross * ds * (cut / 100) * (disc - lost / 100)
                rows.append({"share_of_discounted_deals_changed_pct": cut, "deals_lost_pct": lost,
                             "net_mrr_change": round(net), "net_arr_change": round(net * 12)})
        out["discount_reduction"] = rows
        out["discount_break_even_lost_deals_pct"] = round(disc * 100, 1)
        out["assumptions"].append("Discount scenarios assume removed-discount deals either close at list price or are lost entirely. Break-even lost-deal rate equals the average discount.")

    # 4) Shift to annual plans
    a = d.get("annual_plan_share")
    if mrr_end and a is not None:
        rows = []
        for target in (30, 40):
            shifted = mrr_end * (target / 100 - a)
            if shifted <= 0:
                continue
            rows.append({"target_annual_share_pct": target,
                         "shifted_mrr": round(shifted),
                         "upfront_cash_at_15pct_annual_discount": round(shifted * 12 * 0.85),
                         "annual_revenue_given_up_to_discount": round(shifted * 12 * 0.15)})
        out["annual_plan_shift"] = rows
        out["assumptions"].append("Annual-plan discount of 15% is an assumption. Retention benefit of annual plans is NOT modeled; the agent must reason about it qualitatively.")

    return out
