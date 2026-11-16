"""Deterministic experiment math. The LLM uses these numbers; it does not calculate them."""
from math import ceil, sqrt
from statistics import NormalDist


def sample_size_per_arm(baseline: float, relative_mde: float, alpha: float = 0.05, power: float = 0.80) -> dict:
    """Two-sided, two-proportion z-test sample size per arm (normal approximation)."""
    p1 = baseline
    p2 = baseline * (1 + relative_mde)
    if not (0 < p1 < 1) or not (0 < p2 < 1):
        raise ValueError("baseline and baseline*(1+mde) must be between 0 and 1")
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    p_bar = (p1 + p2) / 2
    n = ((z_a * sqrt(2 * p_bar * (1 - p_bar)) + z_b * sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / ((p2 - p1) ** 2)
    return {
        "baseline_rate": p1,
        "target_rate": round(p2, 5),
        "relative_mde": relative_mde,
        "alpha": alpha,
        "power": power,
        "sample_size_per_arm": ceil(n),
        "total_sample_size": ceil(n) * 2,
    }
