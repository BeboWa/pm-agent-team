## 1. Current Monetization Model

Beacon sells flat per-workspace subscriptions at three tiers: Starter ($49/mo, 5 users), Team ($149/mo, 25 users), and Business ($399/mo, 100 users + SSO). There is no seat-based or usage-based expansion mechanism—a customer can double in size and pay nothing more.

**Structural problems this creates:**

- **NRR is structurally capped below 100%.** With no expansion lever, NRR can only improve through upgrades or reduced churn. At 80% NRR, the base shrinks 20% annually without new sales.
- **Pricing cliffs create churn, not upgrades.** The jump from Team ($149) to Business ($399) is 2.7×. Customers who outgrow Team have a painful binary: pay 2.7× more or leave. Many leave.
- **Discounting is uncontrolled.** 60% of deals close at a ~20% discount. This is both a margin problem (~$295K ARR given away annually per computed data) and a signal that pricing isn't landing its value story.
- **Annual plan penetration is weak.** At 15% annual mix, Beacon collects almost no upfront cash—critical with 20 months of runway—and foregoes the well-documented retention benefit of annual commitments.
- **SSO gated too high.** Locking SSO to the $399 Business tier is losing mid-market deals where buyers need SSO but won't absorb a 2.7× price jump. This is a conversion blocker masquerading as a tier defense.

**ARPA at $263/mo is low for B2B SaaS in this segment.** It reflects heavy Starter/Team concentration and zero expansion revenue. Validate the tier MRR split before committing to any repricing—this is listed as a data gap.

---

## 2. Scenario Math (computed, assumptions labeled)

All numbers below are taken exactly from the computed scenarios. Recovery rates, price-increase churn assumptions, and annual-plan discount (15%) are **illustrative**; real elasticity must be measured.

**Involuntary churn recovery** is the fastest, highest-confidence lever. $38K MRR ($456K ARR) is currently lost to payment failures. At a 35% recovery rate—a reasonable mid-case for a well-configured dunning stack—that is **$13.3K MRR / $159.6K ARR recovered** with no pricing change and minimal eng lift. The 50% case yields $19K MRR / $228K ARR. Even the 20% downside case ($7.6K MRR / $91.2K ARR) is positive ROI.

**Price increase:** A 5% increase with 3% extra churn yields **+$9.25K MRR / +$111K ARR**—the downside case to plan against. The 5%/5%-extra-churn scenario goes slightly negative (−$1.25K MRR), which is the stop condition. A 10% increase with even 3% extra churn yields **+$33.5K MRR / +$402K ARR**, which is the central case if Beacon validates that it has pricing power. Do not apply a blanket increase to all tiers simultaneously—test on new cohorts first (see Section 5).

**Discount governance:** The break-even lost-deal rate is exactly 20%—meaning if tightening discounts causes more than 20% of affected deals to be lost, there is no net gain. The best-case scenario (reducing 50% of discounted deals, 0% lost) yields **+$12.3K MRR / +$147K ARR**. A realistic middle case (50% of deals touched, 10% lost) yields **+$6.1K MRR / +$73.6K ARR**. The 20% lost-deal scenario washes out to zero—that is the floor to watch.

**Annual plan shift:** Moving from 15% to 30% annual mix on $500K MRR generates **$765K in upfront cash** (at 15% annual discount), giving up $135K ARR annually in perpetuity. At 40% annual mix, the upfront cash is **$1.275M**—meaningful against a 20-month runway. The revenue give-up is real; the retention benefit offsets some of it but is not modeled here. Plan for the give-up; assume the retention benefit as a qualitative bonus until measured.

---

## 3. Recommended Pricing and Packaging Changes

Ranked by impact × speed:

### Priority 1 — Seat-Based Value Metric on New Business Tier (High Impact, 3–6 months)

Replace or augment the flat per-workspace cap with a per-seat pricing layer at the Team and Business tiers. The value metric should be **active seats** (not workspace count), because agency headcount is the natural unit of value delivery and the most common expansion signal. Suggested structure:

| Tier | Price | Seats Included | Overage |
|---|---|---|---|
| Starter | $49/mo | 5 seats, hard cap | No overage; must upgrade |
| Team | $149/mo | 10 seats included | +$12/seat/mo above 10 |
| Business | $399/mo | 25 seats included | +$10/seat/mo above 25; SSO included |
| Agency (new) | $799/mo | 50 seats included | +$9/seat/mo; client dashboards included |

*Prices are recommendations, not validated by survey yet. Validate with top-50 Business/Team account interviews before launch.*

A 30-person agency on Team today pays $149. Under per-seat, they pay $149 + (20 × $12) = $389—close to Business tier, with a smoother upgrade path rather than a cliff. This is the structural fix for NRR. The diagnostic estimates $300–600K ARR expansion potential at 12–18 months; validate willingness-to-pay first.

**Feature fences that matter most:**

- **SSO:** Move to Team tier ($149+) as an included feature or $29/mo add-on. The current placement at $399 is costing deals, not protecting revenue. Sales is confirming this qualitatively; validate with closed-lost data.
- **Client-facing dashboards:** Reserve for a new Agency tier or as a $X/client-workspace add-on. This is an expansion SKU for the top 10–15% of customers; don't give it away in Business.
- **Reporting depth / white-labeling:** Business and above. Reporting is the praised feature—it should anchor the upgrade case.
- **API / integrations:** Business and above.

### Priority 2 — Discount Governance (High Impact, Immediate)

Implement a discount approval policy this week: any discount >10% requires VP of Sales approval; >15% requires CFO sign-off. Replace cash discounts with **annual-plan incentives**—instead of 20% off monthly, offer 2 months free on annual (equivalent to ~17% off). This converts discount spend into cash-flow-positive commitments. At 50% of discounted deals touched with 10% lost, the computed upside is **+$6.1K MRR / +$73.6K ARR**. The break-even is 20% lost deals—track win rate weekly after policy change.

### Priority 3 — Annual Plan Push (Medium Impact, 30–60 days)

Target 30% annual mix within 6 months. Tactics: (a) display annual pricing as the default on the pricing page; (b) add a "2 months free" badge prominently; (c) train sales to default to annual proposals; (d) offer a one-time annual migration incentive to the top 200 monthly accounts (≈those spending $200+/mo). Computed upside at 30% mix: **$765K upfront cash** at the cost of $135K ARR annually. With 20 months of runway, the cash is worth the trade.

### Priority 4 — 5–10% Price Increase on New Customers Only (Medium Impact, 60–90 days)

Do not raise prices on the existing base until annual plan migrations are complete and churn is trending down. For new signups: test a 5% increase on Team tier first (lowest churn risk, most price-sensitive tier is Starter). The 5%/3%-extra-churn scenario yields +$9.25K MRR; the 5%/5%-extra-churn scenario goes slightly negative—that's the stop signal. Run for one cohort (60 days) before rolling to Business or Starter.

---

## 4. Billing and Payments Implications

### Dunning and Involuntary Churn (ship first)

Engineering scope: 2–4 weeks using Stripe Billing or Chargebee's built-in dunning engine.

- **Retry schedule:** Attempt on day 1, 3, 7, 14 post-failure. Use Stripe's smart retry (ML-optimized timing) if on Stripe.
- **Card expiry alerts:** Email at 60 days and 7 days before card expiry. In-app banner for account owners on the billing page.
- **Grace period:** Do not lock access immediately on first failure. Implement a 7-day grace period before downgrading to read-only; a 14-day grace before full suspension. Communicate clearly at each step. (Support tickets cite "lockouts"—the current zero-grace policy is driving avoidable cancellations.)
- **Customer communication:** Three emails in the dunning sequence: (1) "Your payment failed—update here," (2) "Access will be limited in X days," (3) "Account suspended—reactivate here." All must include one-click payment update link.
- **Revenue recognition:** Payment failure does not immediately reduce recognized revenue if within grace period—confirm with finance whether ASC 606 / IFRS 15 treatment requires adjustment at day 1 or at suspension. **Flag for finance review.**

### Proration and Mid-Cycle Changes (required for seat-based pricing)

- **Seat additions mid-cycle:** Prorate to end of billing period. Line item: "X additional seats, Y days remaining, $Z." Show this on the confirmation screen before charge—this is what causes "surprise charges" per support tickets.
- **Seat removals:** Credit to next invoice (not cash refund) unless the customer is on annual and removes seats before mid-year—treat that as a contraction event and issue a credit memo. **Finance must define the credit memo policy.**
- **Tier upgrades:** Charge the prorated difference immediately; new entitlements activate immediately.
- **Tier downgrades:** Apply at next billing cycle. Entitlements reduce at cycle end (do not remove SSO mid-cycle if a customer is downgrading—that creates support chaos).
- **Annual-to-monthly changes:** Disallow mid-year downgrades from annual to monthly except on renewal. Document this in terms of service. **Legal review required.**

### Invoicing

- Each invoice must show: tier name, billing period, base seats, overage seats (count × rate), any add-ons (SSO if sold separately, client dashboards), subtotal, tax (see below), total.
- For annual prepay: single line item for the full annual amount with a "prepaid through [date]" note. Earned revenue recognized monthly 1/12th of annual amount. **Revenue recognition schedule must be generated per invoice—engineering needs to generate a deferred revenue schedule at invoice creation. Finance/audit requirement.**
- **Tax:** Beacon likely has sales tax nexus in multiple US states (SaaS taxability varies by state) and potentially VAT obligations if any EU customers exist. **Tax review required before any price changes are communicated publicly.** Use TaxJar or Avalara to automate; do not hardcode rates.
- **Currency:** Dossier is USD-only. If geo tests (see Section 5) touch non-USD markets, add currency handling before launch, not after. Stripe supports multi-currency invoicing natively.

### Entitlement and Access Changes

- Entitlements must be driven by a single source of truth (a billing/entitlement service, not hardcoded in the app). When a customer's plan changes—upgrade, downgrade, payment failure, cancellation—the entitlement service must receive an event and update access within seconds, not on next login.
- SSO provisioning/deprovisioning must be tied to entitlement events, not manual ops tickets. **Engineering must audit whether the current SSO gate is event-driven or manually managed—if manual, that is a P0 fix before moving SSO to Team tier.**
- Audit trail: every entitlement change must log the trigger (payment event, manual change, plan migration), the actor (system/admin/user), and timestamp. Required for disputes and finance audits.

---

## 5. Migration and Rollout

### Grandfathering Policy

Existing customers on flat per-workspace pricing at the time of the seat-based rollout should be **grandfathered at their current rate for 12 months** with a clear sunset date communicated upfront. This reduces involuntary churn from price shock and gives CS time to manage the transition. Customers who voluntarily upgrade during the grandfathering window get the new seat-based pricing immediately.

Annual plan customers must be grandfathered through their current annual term regardless. Do not reprice mid-contract. **Legal review required on existing subscription terms.**

### Notice Periods

- Price increase on new customers: no notice required (new signups, new price).
- Price increase on existing monthly customers: 30-day written notice minimum. Email from CEO/founder, not a billing system auto-send. Explain the value received and what's new.
- Plan restructure (seat-based migration): 60-day notice for existing customers. Provide a migration calculator ("here's what you'd pay under the new model") and a one-click path to lock in the grandfathered rate for 12 months.

### Rollout Sequence

1. **Weeks 1–4:** Dunning automation live. No pricing change. Measure involuntary churn rate.
2. **Weeks 4–8:** Discount policy tightened. Annual plan default on pricing page. Annual push to top 200 monthly accounts.
3. **Weeks 8–12:** 5% price increase on new Team-tier signups only. Monitor conversion rate and cohort churn at day 30.
4. **Month 3–4:** SSO add-on or move to Team tier (after validating engineering scope and closed-lost data). Survey top-50 accounts on seat pricing.
5. **Month 4–6:** Seat-based pricing in beta for new Business-tier signups. Grandfathering notice sent to existing base.
6. **Month 6–9:** Full rollout of seat-based pricing. Migration window for existing customers.

### Cohort and Geo Testing

- Run the 5% price increase as a true A/B: 50% of new Team signups see old price, 50% see new price. Measure conversion-to-paid and 30-day retention. Run for 60 days minimum (need statistical significance given ~58 new Team customers/month estimated).
- If international customers exist: consider a geo-isolated test of annual plan push in one English-speaking market (e.g., UK or AU) before global rollout.

### Stop Conditions

| Test | Stop If |
|---|---|
| 5% price increase on Team tier | Paid conversion drops >5pp vs. control at 30 days |
| Discount tightening | Win rate drops >15pp month-over-month for 4 weeks |
| Annual plan push | Annual mix does not move from 15% after 60 days (indicates incentive is wrong, not the goal) |
| Seat-based beta | Blended ARPA for beta cohort is not >20% above flat-pricing cohort at 90 days |
| Dunning rollout | Support ticket volume on billing increases (indicates communications are confusing, not helping) |

---

## 6. Test Plan and Risks

### What to Validate First (Data Gaps)

- **Churn by tier:** If Starter churns at 40%+ and Business at 10%, the interventions are completely different. Pull this cohort before committing to any tier-level repricing.
- **MRR by tier:** ARPA of $263 suggests Starter/Team dominance. If >60% of MRR is on tiers below $149, a Business-tier seat expansion does not move the needle as much as modeled.
- **Closed-lost reasons citing SSO:** Qualitative signal from sales exists, but need the count. If fewer than 20 deals/year cite SSO, the add-on investment may not pencil out.
- **Expansion MRR source:** Was the $40K from tier upgrades or additional workspaces? If it's workspaces, there's already organic expansion behavior to build on.
- **CAC by channel:** If sales-assisted CAC is >$5K targeting the same SMB segment as self-serve, that's a resource misallocation that pricing changes alone will not fix.

### Key Risks

**Seat-based pricing migration causes voluntary churn spike.** Some flat-pricing customers will be paying below what they'd pay per-seat; the migration feels like a price increase. Mitigation: 12-month grandfather, migration calculator, CS-assisted outreach to accounts that would see >25% increase. Downside scenario: 5–8% of base churns on migration notice = $25–40K MRR lost. This is the scenario that could be existential with 20 months runway—do not rush the migration without CS capacity in place.

**Discount tightening loses more deals than the break-even rate.** The computed break-even is exactly 20% lost deals. If the sales team is relying on discounts to close competitively against Monday.com and Asana, win rate could fall faster than modeled. Mitigation: pilot with one sales rep or one geo before full rollout. Track weekly.

**Dunning automation creates compliance or communication issues.** Aggressive retry behavior can trigger card network flags or customer complaints. Use Stripe/Chargebee's built-in retry rather than custom logic. Have legal review the dunning email copy for accuracy of "account suspension" language in relevant jurisdictions.

**Engineering capacity.** Seat-based pricing requires metered billing infrastructure, a seat-count API, proration logic, and entitlement updates—easily 6–10 weeks of backend work for a team of 8. If the team is already committed to product roadmap, the pricing change will slip. Scope this explicitly with the engineering lead before committing to the timeline above. The dunning and annual plan changes should require minimal custom eng if Beacon is on Stripe Billing or Chargebee.

**Revenue recognition complexity on annual plans.** Moving from 15% to 30%+ annual mix increases deferred revenue on the balance sheet. At $1.275M in upfront cash (40% mix scenario), deferred revenue grows materially. The board wants a path to profitability—make sure the CFO understands the GAAP vs. cash distinction before presenting the annual plan push as a "revenue increase." It is a **cash flow** improvement, not a recognized revenue improvement in the period of collection.

---
_Run metrics: 117.7s, 7341 in / 4558 out tokens, ~$0.0904_
