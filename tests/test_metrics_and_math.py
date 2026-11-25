import pytest

from agents.analytics.stats import sample_size_per_arm
from agents.diagnostic.metrics import compute_metrics
from agents.pricing_billing.pricing_math import pricing_scenarios


def test_metrics_for_sample_company(sample):
    m = compute_metrics(sample)
    assert m["arr_end"] == 6_000_000
    assert m["nrr_pct"] == 80.0
    assert m["grr_pct"] == 70.0
    assert m["mrr_bridge_check"] == 0
    assert m["involuntary_churn_annualized_arr_at_risk"] == 456_000
    assert m["cac_payback_months"] == 8.3
    assert m["ltv_to_cac"] == 5.7


def test_metrics_skip_what_is_missing():
    m = compute_metrics({"mrr_start": 100, "mrr_end": 110})
    assert "nrr_pct" in m and "cac_payback_months" not in m


def test_pricing_scenarios_known_values(sample):
    s = pricing_scenarios(sample)
    assert abs(s["discount_leakage_annualized_arr"] - 294_545) <= 1
    assert s["discount_break_even_lost_deals_pct"] == 20.0
    row = next(r for r in s["discount_reduction"] if r["share_of_discounted_deals_changed_pct"] == 50 and r["deals_lost_pct"] == 10)
    assert row["net_arr_change"] == 73_636
    row = next(r for r in s["price_increase"] if r["price_increase_pct"] == 5 and r["extra_churn_pct_of_base"] == 3)
    assert row["net_arr_change"] == 111_000
    assert s["annual_plan_shift"][0]["upfront_cash_at_15pct_annual_discount"] == 765_000
    assert s["assumptions"], "every scenario set must carry its assumptions"


def test_break_even_means_zero_effect(sample):
    """Losing exactly as many deals as the discount size should cancel the gain."""
    s = pricing_scenarios(sample)
    s20 = [r for r in s["discount_reduction"] if r["deals_lost_pct"] == 20]
    assert all(r["net_mrr_change"] == 0 for r in s20)


def test_sample_size_matches_textbook_value():
    r = sample_size_per_arm(0.05, 0.20)  # 5% -> 6%
    assert 8000 <= r["sample_size_per_arm"] <= 8400
    assert r["total_sample_size"] == 2 * r["sample_size_per_arm"]


def test_sample_size_rejects_impossible_rates():
    with pytest.raises(ValueError):
        sample_size_per_arm(0.9, 0.5)
