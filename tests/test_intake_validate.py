import copy

from intake.validate import validate_dossier


def test_sample_dossier_is_clean(sample):
    res = validate_dossier(sample)
    assert res["errors"] == [] and res["warnings"] == []


def _errors(d):
    return " | ".join(validate_dossier(d)["errors"])


def test_catches_revenue_that_does_not_add_up(sample):
    d = copy.deepcopy(sample); d["mrr_end"] = 650_000
    assert "MRR does not add up" in _errors(d)


def test_catches_customers_that_do_not_add_up(sample):
    d = copy.deepcopy(sample); d["customers_end"] = 3000
    assert "Customers do not add up" in _errors(d)


def test_percent_entered_instead_of_fraction(sample):
    d = copy.deepcopy(sample); d["gross_margin"] = 78
    assert "fraction" in _errors(d)


def test_funnel_must_shrink(sample):
    d = copy.deepcopy(sample); d["funnel"]["paid"] = 99_999
    assert "Funnel is not decreasing" in _errors(d)


def test_missing_required_fields(sample):
    d = copy.deepcopy(sample); del d["mrr_start"]; del d["pricing"]
    e = _errors(d)
    assert "'mrr_start' is required" in e and "pricing" in e


def test_personal_data_is_blocked(sample):
    for bad in ("Contact jane@example.com", "Call 508-555-0142", "SSN 123-45-6789", "Card 4111 1111 1111 1111"):
        d = copy.deepcopy(sample); d["qualitative"].append(bad)
        assert "Possible" in _errors(d), bad


def test_ordinary_numbers_do_not_trigger_personal_data_check(sample):
    d = copy.deepcopy(sample); d["qualitative"].append("Revenue grew 25% to $6,000,000 with 1,900 customers")
    assert validate_dossier(d)["errors"] == []


def test_real_client_data_needs_a_consent_record(sample):
    d = copy.deepcopy(sample); d.pop("_note")
    assert any("consent" in w for w in validate_dossier(d)["warnings"])
    d["_intake"] = {"consent": True}
    assert validate_dossier(d)["warnings"] == []
