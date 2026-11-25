from agents.diagnostic.metrics import compute_metrics
from agents.pricing_billing.pricing_math import pricing_scenarios
from agents.reviewer.grounding import find_ungrounded, money_figures


def _sources(sample):
    return [sample, compute_metrics(sample), pricing_scenarios(sample)]


def test_parses_money_formats():
    vals = sorted(round(v) for v, _ in money_figures("$456K, $1.2M, $3,200,000, $2.5 million, $50"))
    assert vals == [456_000, 1_200_000, 2_500_000, 3_200_000]  # $50 is below the $1,000 floor


def test_grounded_figures_pass_and_invented_ones_are_flagged(sample):
    reports = {"Company Diagnostic": "At risk: $456K. Leakage: $295K. Upside: $4.7M."}
    flagged = find_ungrounded(reports, _sources(sample))
    assert [f["figure_usd"] for f in flagged["Company Diagnostic"]] == [4_700_000]


def test_later_stage_may_restate_earlier_figures(sample):
    reports = {"Company Diagnostic": "Upside: $4.7M.", "PRD": "Chasing the $4.7M. New claim: $88K."}
    flagged = find_ungrounded(reports, _sources(sample))
    assert [f["figure_usd"] for f in flagged["PRD"]] == [88_000]
    assert flagged["Company Diagnostic"][0]["figure_usd"] == 4_700_000
