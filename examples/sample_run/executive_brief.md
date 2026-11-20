# Executive Brief: Beacon

## The Diagnosis

Beacon is growing at 25% ARR to $6M, with solid unit economics on paper (8.3-month CAC payback, 5.7x LTV:CAC). The crisis is retention: 25% annual logo churn and 70% GRR mean the existing base shrinks 20% a year without new sales. For every dollar of new MRR acquired, roughly $0.67 is lost to churn and contraction before year-end. The sales team is filling a hole, not building a moat. With 20 months of runway, this is a retention-first emergency with a monetization opportunity layered on top.

---

## Top 3 Bets

**Bet 1 — Fix involuntary churn via dunning automation (ship in weeks 1–4)**
What: Configure automated payment retry (days 1/3/7) plus a 7-day grace period on the billing platform.
Why: 40% of churned MRR ($38K/month, $456K ARR annualized) is from payment failures, not dissatisfaction—a pure ops fix. A 35% recovery rate yields an estimated $159.6K ARR recovered; the 50% case yields $228K. Even the 20% downside case ($91.2K ARR) is strongly positive ROI at ~2 weeks of engineering. *Key assumption: Beacon runs on Stripe or Chargebee. Verify in week 1—custom billing infra raises effort to 2–3 months.*

**Bet 2 — Annual plan push (weeks 4–8)**
What: Set annual pricing as the default on the pricing page, add a "2 months free" badge, and run direct outreach to the top 200 monthly accounts.
Why: At 15% annual mix, Beacon collects almost no upfront cash against a 20-month runway. Moving to 30% annual mix generates an estimated $765K in upfront cash (at the modeled 15% annual discount), giving up $135K ARR annually. At 40% mix, upfront cash reaches an estimated $1.275M. Retention benefit of annual plans is not modeled but is a real qualitative upside. *Key assumption: 15% annual discount; retention benefit not quantified.*

**Bet 3 — Discount governance (immediate, zero engineering)**
What: Require VP approval for discounts above 10%; replace cash discounts with annual-plan incentives.
Why: 60% of deals close at ~20% discount, leaking an estimated $294.5K ARR annually (computed scenario). The break-even lost-deal rate is exactly 20%—if tightening discounts loses fewer than 1 in 5 affected deals, it's a net gain. At 50% of discounted deals touched with 10% lost, the computed upside is $73.6K ARR. *Key assumption: illustrative lost-deal rates; real elasticity must be measured.*

---

## 30/60/90-Day Plan

**30 days:** Confirm billing platform (gate on week 1). Deploy dunning automation and grace period. Implement discount governance policy. Instrument the activation milestone ("first report shared"). Mandate exit surveys for all churned customers. Pull churn cohort by tier.

**60 days:** Push annual plan default live on pricing page. Run outreach to top 200 monthly accounts. Begin A/B test routing trial users to the reporting feature. CS flags at-risk accounts (low login + no reports run). Review dunning results and win-rate data.

**90 days:** Decide on seat-based pricing roadmap (requires top-50 customer survey results and WTP signal). Decide on SSO repositioning (requires closed-lost data showing deal volume). Set NRR target for the next 6 months. Run first read on activated-to-paid cohort from A/B test.

---

## Decisions Needed

1. **Billing platform confirmation (week 1, blocking):** Is Beacon on Stripe/Chargebee or custom infra? If custom, the entire Now-phase timeline shifts 4–6 weeks and must be re-sequenced. *Recommendation: assign an engineer to answer this on day 1.*
2. **Annual plan discount depth:** The model uses 15% (2 months free). Leadership must decide whether to offer a deeper incentive (e.g., 3 months free) to accelerate mix shift, accepting a larger permanent ARR give-up. *Recommendation: start at 2 months free; test before deepening.*
3. **Seat-based pricing timing:** This is the structural fix for NRR but requires 8+ person-months of engineering and carries a real migration churn risk (estimated 5–8% churn spike = $25–40K MRR). *Recommendation: do not begin without WTP survey results and CS capacity in place. Defer decision to the 90-day gate.*

---

## Key Risks

- **Migration churn from seat-based pricing:** A poorly managed rollout could cause a churn spike that is existential at 20 months runway. Do not rush it.
- **Discount tightening exceeds break-even:** If win rate drops more than 20pp on affected deals, the policy nets zero or negative. Track weekly; revert at the 15pp drop signal.
- **Dunning on custom billing infra:** If Beacon is not on a modern billing platform, the highest-priority item becomes a 2–3 month engineering project, not a 2-week config task.
- **Annual plan cash vs. GAAP distinction:** Moving to 30–40% annual mix improves cash flow materially but does not increase recognized ARR in the same period. Ensure the board and CFO understand this before the next board meeting.

---

## Needs Human Validation

The following issues were flagged by the Reviewer and are unresolved:

- **High: Recovery rate target inconsistency across PRD, Launch, and Analytics.** The $90K ARR recovery figure corresponds to the 20% recovery scenario (computed: $91.2K ARR annualized). The PRD and Analytics set 40% recovery as the primary target, which corresponds to ~$182K ARR. These are not aligned. Leadership should confirm: is $91K the floor and $182K the primary target, or are they the same goal stated differently? Downstream incentive-setting depends on this.
- **High: Discount leakage figure inconsistency.** Two figures are in circulation internally: $259K ARR (Diagnostic, computed via a different method) and $294.5K ARR (computed scenario used in this brief). The $294.5K figure is used here as it comes from the computed scenarios. The Diagnostic figure should be corrected before this brief is shared with the sales team.
- **Medium: SSO repositioning requires ASC 606 SSP re-allocation review.** If SSO moves from Business tier to Team tier as an included feature, finance and audit must review standalone selling price allocations under ASC 606. This has not been flagged in the current compliance documentation.
- **Medium: 28% activated-to-paid conversion used as a sizing benchmark has no cited source.** It is used to estimate the onboarding opportunity (~$757K ARR). Treat as an internal working assumption, not an industry benchmark, until a source is identified.
- **Medium: RICE table mixes annual and quarterly Reach units**, making the top-ranked item's score (1,600) incomparable to others. The prioritization narrative accounts for this qualitatively, but the table should not be shared externally without normalization.

---
_Run metrics: 49.2s, 27926 in / 1763 out tokens, ~$0.1102_
