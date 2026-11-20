# Company Diagnostic report

# Beacon — Company Diagnostic

---

## 1. Business Model Snapshot

**What Beacon is:** B2B SaaS, project management and reporting for agencies (10–200 people). Primarily self-serve with a sales assist layer for larger accounts.

**How it makes money:** Flat per-workspace subscriptions across three tiers ($49/$149/$399/mo). No seat-based or usage-based expansion. Revenue growth is almost entirely dependent on new logo acquisition.

**The core tension:** Beacon is growing (25% ARR growth), has efficient unit economics on paper (LTV:CAC 5.7x, payback 8.3 months), but is bleeding customers at an alarming rate — erasing nearly a third of the expansion it creates. The business is a leaky bucket with a good pump.

---

## 2. Health Scorecard

| Metric | Beacon | Rule of Thumb | Signal |
|---|---|---|---|
| ARR | $6.0M | — | ✅ Solid Series A |
| ARR Growth | 25% | >40–60% healthy at this stage | ⚠️ Slowing, not growing into Series B |
| NRR | 80% | >100% (best-in-class), >90% minimum | 🔴 Critical — contracting base |
| GRR | 70% | >85–90% | 🔴 Critical — logo and revenue churn destroying compounding |
| Logo Churn | 25% | <10% annually (B2B SaaS) | 🔴 Severe — losing 1 in 4 customers per year |
| Churned MRR % of Start | 23.8% | <10% healthy | 🔴 Alarming |
| Expansion MRR % | 10% | Should offset contraction+churn | ⚠️ Expansion exists but far too small |
| CAC Payback | 8.3 months | <12–18 months | ✅ Strong |
| LTV:CAC | 5.7x | >3x | ✅ Looks good — but only because LTV assumes current retention; LTV is at risk |
| ARPA Monthly | $263 | Context-dependent | ⚠️ Low for B2B; pricing model suppresses expansion |
| Involuntary Churn ARR at Risk | $456K | Typically 20–40% of total churn | 🔴 High — $38K MRR leaking from fixable payment failures |
| Annual Plan Mix | 15% | 30–50% healthy | 🔴 Cash flow and retention opportunity untapped |
| Visitor → Signup | 4% | 2–5% | ✅ Healthy |
| Signup → Activated | 35% | 40–60% typical | ⚠️ Below benchmark; onboarding friction confirmed |
| Activated → Paid | 20.8% | 25–35% typical | ⚠️ Conversion gap despite product praise |

**Summary verdict:** The unit economics look attractive in isolation, but NRR of 80% means Beacon must run hard just to stay flat. At this churn rate, the LTV calculation is fragile. This is a retention-first emergency with a monetization opportunity layered on top.

---

## 3. The Revenue Equation

**Current driver:** New logos (~$180K new MRR/yr). Expansion is minimal ($40K). Retention is destroying value ($95K churned MRR, $25K contraction).

**The math of the problem:**
- Beacon added 700 customers and lost 400. Net 300 added — a 57% churn offset rate.
- For every $1 of new MRR acquired, ~$0.67 is lost to churn and contraction before the year ends.
- NRR of 80% means the existing base shrinks 20% annually without new sales. Sales team is essentially filling a hole.

**What *should* drive growth at this stage (but doesn't yet):**
1. **Retention** — fixing GRR from 70% → 85%+ would add ~$900K ARR annually from the existing base alone (illustrative: 15pp × $6M ARR, rough estimate, assumes proportional recovery).
2. **Expansion** — flat per-workspace pricing structurally prevents NRR >100%. Beacon has no mechanism to grow revenue with customers.
3. **New logos** — the funnel is working reasonably well but activated-to-paid conversion has room.

**Growth is currently new-logo dependent in a leaky bucket. The fix is retention + expansion monetization.**

---

## 4. Leaks and Levers (Ranked by Est. Annual $ Impact and Speed)

### 🔴 Leak 1 — Involuntary Churn (Payment Failures)
**Est. annual impact:** $456K ARR at risk (computed). This is recoverable revenue.
**Speed:** 4–8 weeks to implement.
**What's happening:** 40% of churned MRR ($38K/mo) is from failed payments, not product dissatisfaction. Support tickets confirm "failed-card lockouts." This is a pure ops/billing fix.
**Action:** Deploy dunning automation (Stripe Billing, Chargebee, or similar). Smart retry logic, pre-expiry card alerts, in-app payment update prompts. Best-practice recovery rates are 40–70% of involuntary churn.
**Conservative recovery estimate:** $180K–$320K ARR recovered. Confidence: High — this is industry-standard recoverable revenue.

---

### 🔴 Leak 2 — Logo Churn (25% annually)
**Est. annual impact:** $1.14M ARR lost per year (400 customers × $263 ARPA × 12). Even recovering 20% of churned logos = ~$228K ARR.
**Speed:** First interventions in 30–60 days; full impact 6–12 months.
**What's happening:** 25% logo churn is 2–3x a healthy B2B SaaS rate. Causes are layered: onboarding confusion (reviews), product-fit mismatch (smaller customers on Starter may not activate deeply), and pricing cliffs that offer no path to stay.
**Actions:**
- Instrument and define a "healthy customer" activation milestone (tied to reporting feature, which gets praised).
- Build a churn prediction model (even simple: low login cadence + no reports run = at-risk flag).
- Assign a Customer Success motion to the top 20% of accounts by ARR (Business tier + high-usage Team tier).
- Exit survey every churned customer — currently flying blind on causes.

---

### 🟡 Leak 3 — Activated-to-Paid Conversion Gap
**Est. annual impact:** 3,360 activated users, 20.8% convert. Closing to 28% (benchmark low end) = ~240 additional paid customers. At $263 ARPA: ~$757K ARR. Assumption: same ARPA mix; confidence moderate.
**Speed:** 60–90 days for onboarding changes to show signal.
**What's happening:** Reviews cite confusing onboarding. 35% signup-to-activation rate and 20.8% activation-to-paid suggest friction between "sees value" and "pays." The reporting feature is the hook — onboarding should route every trial user to their first report within session one.
**Actions:** Define the "aha moment" (likely: first report shared with a client). Rebuild trial onboarding around that milestone. Add an in-app upgrade prompt at moment of value delivery.

---

### 🟡 Lever 4 — Annual Plan Conversion (15% → 30%+)
**Est. annual impact:** Upfront cash + ~10–15% lower churn on annual customers (industry benchmark). At $6M ARR, moving from 15% to 30% annual mix on new and renewing customers unlocks ~$540K in cash flow acceleration and meaningfully improves GRR. Confidence: moderate (depends on incentive structure).
**Speed:** 30–60 days (pricing page + sales motion change).
**Action:** Offer a 1–2 month discount for annual commitment on the checkout flow. Train sales to default to annual. Stop competing with the 20% monthly discount (see below).

---

### 🟠 Leak 5 — Discounting Erosion
**Est. annual impact:** 60% of deals discounted at 20%. On $180K new MRR, that's ~$108K MRR affected × 20% = ~$21.6K MRR / ~$259K ARR given away annually. Confidence: moderate (some discounting is unavoidable in competitive deals).
**Speed:** Immediate policy change.
**What's happening:** When 60% of deals need a 20% discount to close, it usually signals one of three things: the price is wrong, the value isn't landing, or sales has no guardrails. Given competitive pressure (Asana, Monday), some discount is expected — but 60% frequency is a sales process problem, not a market problem.
**Action:** Create a discount approval threshold (e.g., >15% requires VP sign-off). Replace cash discounting with annual-plan incentives. Track win rates vs. discount rate — if win rate doesn't fall when discounts tighten, they were unnecessary.

---

## 5. Monetization Opportunities

### 5a. Introduce Seat-Based Pricing (High Impact, Slower)
**The problem with flat workspace pricing:** Beacon has zero expansion revenue from account growth. An agency that grows from 10 to 50 people pays the same. This is the single biggest structural cap on NRR.
**Opportunity:** Larger agencies explicitly request per-seat pricing. At $15–25/seat/month (common for this category), a 30-person agency would pay $450–$750/mo vs. $149 today. Even 10% of the customer base adopting a seat-based tier could represent $200–400K+ ARR expansion.
**Assumption note:** Requires product and pricing work, grandfathering decisions, and customer communication. This is a 6–12 month bet, not a quick win.

### 5b. Move SSO Down-Market (or Create a Mid-Market Add-On)
**The problem:** Sales is losing deals because SSO is gated to the $399 Business tier. At $149 (Team), buyers need SSO but won't pay $399. This is a conversion blocker, not a tier-defense mechanism.
**Options:** (a) Add SSO as a $49/mo add-on at Team tier; (b) lower the Business tier price threshold; (c) offer SSO as a trial-to-close incentive.
**Estimated impact:** Even capturing 5% more Team-tier closures on this blocker: 35 customers × $149 = ~$62K ARR. Low estimate but fast.

### 5c. Client-Facing Dashboard as an Expansion SKU
**The signal:** Larger agencies explicitly ask for client-facing dashboards. This is a natural expansion product — agencies have 10–50 clients each; a "client portal" seat or workspace is a volume multiplier.
**Hypothesis:** A $X/client-workspace/month add-on, or a "Agency+" tier, could make expansion revenue structural.
**Requires:** Validation that this is a willingness-to-pay feature, not just a request. Survey the top 50 accounts.

---

## 6. Top 3 Strategic Bets

### Bet 1: "Stop the Bleed" — Retention & Involuntary Churn Recovery
**Hypothesis:** A meaningful portion of Beacon's 25% logo churn is preventable. 40% is already confirmed as involuntary (payment failures). The remaining voluntary churn is concentrated in under-activated customers who never reached the reporting "aha moment." Fixing both improves GRR from 70% → 80%+ within 12 months.

**Validation test:** (1) Deploy dunning — measure involuntary churn rate at 90 days. Target: reduce by 50%. (2) Define and instrument the activation milestone. Measure whether customers who hit it in trial churn at a lower rate. If yes, focus onboarding there.

**Owner type:** Head of Customer Success (CS) + Billing/RevOps.

**What would prove it wrong:** Churn cohort analysis shows churned customers *did* activate and use reporting heavily — meaning churn is competitive displacement or pricing, not onboarding. That would redirect to competitive positioning or pricing restructure.

---

### Bet 2: "Fix the Ceiling" — Introduce Seat-Based Expansion Pricing
**Hypothesis:** Flat per-workspace pricing is the structural reason NRR is 80% and expansion MRR is only $40K/year. Introducing a per-seat pricing layer (or a seat-based tier above $399) will make NRR positive and reduce pressure on new-logo acquisition.

**Validation test:** Survey top 50 Business-tier customers — would they prefer seat-based pricing at $X/seat if it included [feature]? Run a pricing experiment with new Business-tier sign-ups only. Measure ARPA at 6 months vs. control.

**Owner type:** Head of Product + Revenue/Pricing.

**What would prove it wrong:** Survey and cohort data shows larger customers prefer flat pricing and would churn rather than accept seat-based. In that case, the expansion lever is add-ons (client dashboards, integrations) rather than seat restructure.

---

### Bet 3: "Increase Funnel Yield" — Activation-to-Paid Conversion Optimization
**Hypothesis:** 3,360 users activate per year but only 700 pay. Onboarding does not reliably guide users to the highest-value moment (reporting). Re-engineering the trial flow around "first report shared" as the activation event will increase conversion rate from 20.8% to 27–30%, yielding 200+ additional customers annually at no incremental acquisition cost.

**Validation test:** A/B test a new onboarding flow that front-loads the reporting feature. Measure activated-to-paid rate at 30 days vs. current cohort. Run for 60 days.

**Owner type:** Product Manager (Growth) + Marketing.

**What would prove it wrong:** A/B test shows no difference in conversion despite higher reporting engagement — meaning the barrier to paid conversion is price, not activation. Would then point to trial pricing, free-tier limits, or competitive comparison as the lever.

---

## 7. Data Gaps

Request these before the next strategy session:

1. **Churn reasons / exit survey data** — Without this, churn intervention is guesswork. What % is competitive displacement vs. not enough value vs. pricing vs. company closure?
2. **Cohort retention curves by tier** — Does Starter churn at 40%+ while Business churns at 10%? Knowing this changes where to invest in CS and whether the Starter tier is structurally unprofitable.
3. **MRR by tier** — What % of $500K MRR comes from each tier? ARPA of $263 suggests heavy Starter/Team mix — need to confirm.
4. **Activation milestone definition and data** — What does "activated" mean currently? Is it correlated with retention? This is prerequisite to Bet 1 and Bet 3.
5. **CAC by channel** — Blended CAC is $1,714 but split between self-serve and sales-assisted is unknown. If sales CAC is $5K+ and targets the same SMB, that's a resource misallocation problem.
6. **Expansion MRR source** — What drove the $40K expansion? Tier upgrades or more workspaces? Knowing this tells us whether expansion is organic or sales-driven.
7. **Sales loss reasons** — The SSO/pricing concern is qualitative. How many closed-lost deals cite SSO or pricing tier as primary reason?
8. **Engineering capacity mapping** — Of the 8 engineers, what % of capacity is currently on infra/maintenance vs. product? Bet 2 (pricing) has real eng lift.

---

## 8. 30/60/90-Day Validation Plan

### 30 Days — Plug the Holes (No Eng Required)
| Action | Owner | Success Metric |
|---|---|---|
| Deploy dunning automation (Stripe/Chargebee) | RevOps | Involuntary churn rate drops 30%+ |
| Mandate exit survey for every churned customer | CS / CX | 50+ responses in 30 days |
| Freeze discounts >15% without VP approval | Sales Lead | Discount frequency tracked week-over-week |
| Pull churn cohort by tier (Starter/Team/Business) | Analytics | Data in hand for 60-day decisions |
| Define "aha moment" candidate (reporting milestone) | PM | Hypothesis documented, instrumentation plan written |

### 60 Days — Test and Learn
| Action | Owner | Success Metric |
|---|---|---|
| A/B test onboarding flow routing to reporting | PM (Growth) | Activated-to-paid rate lift >3pp at 30 days post-change |
| Annual plan push: add 1-month-free-on-annual to checkout | RevOps + Marketing | Annual mix increases from 15% → 20%+ |
| CS outreach to at-risk accounts (low login + no reports) | CS | Churn rate in flagged cohort vs. unflagged cohort |
| Survey top 50 Business/Team accounts on seat pricing & client dashboards | PM | Willingness-to-pay signal on expansion SKUs |
| SSO add-on pricing analysis | PM + Sales | Decision: add-on vs. tier restructure |

### 90 Days — Decide and Commit
| Decision Point | Based On |
|---|---|
| Commit to seat-based pricing roadmap (or not) | Survey data + competitive analysis |
| Prioritize client dashboard MVP (or not) | Top-50 survey + expansion MRR data |
| Set NRR target for next 6 months (90% by M18?) | Churn cohort data + dunning results |
| Reallocate sales effort (self-serve optimization vs. mid-market push?) | CAC-by-channel data |

---

## 9. Handoff to Prioritization

| # | Bet Name | Problem It Solves | Evidence | Est. Annual Impact |
|---|---|---|---|---|
| 1 | **Stop the Bleed** (dunning + CS activation) | NRR 80%, GRR 70%, 25% logo churn destroying compounding | $456K ARR in confirmed involuntary churn; support tickets confirm payment lockouts; reviews cite onboarding confusion | $450K–$900K ARR recovered/retained (moderate confidence) |
| 2 | **Fix the Ceiling** (seat-based expansion pricing) | Zero structural expansion; flat pricing caps NRR below 100% permanently | Larger agencies request per-seat pricing; $40K expansion MRR = only 10% of start MRR; NRR 80% | $300K–$600K ARR expansion within 12–18 months (lower confidence; requires validation) |
| 3 | **Increase Funnel Yield** (onboarding → reporting aha moment) | 20.8% activated-to-paid below benchmark; 2,660 activated users not converting | Reviews praise reporting; onboarding cited as confusing; conversion gap vs. 27–30% benchmark | $500K–$750K ARR from incremental conversions (moderate confidence; assumes mix holds) |

**Recommended sequencing:** Bet 1 first (fastest, lowest eng cost, highest confidence), Bet 3 in parallel (PM-led, A/B testable in 60 days), Bet 2 after validation data in hand (~90 days). With 8 engineers and 20 months runway, do not start Bet 2 without clear willingness-to-pay signal — a failed pricing restructure is an existential risk at this stage.

---
_Run metrics: 112.7s, 1507 in / 4795 out tokens, ~$0.0764_


# Pricing & Billing report

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


# Customer Discovery report

## Top Themes (ranked)

Ranking method: primary sort = frequency (number of distinct items); tie-break = severity (impact on the customer's core goal — paying accurately, keeping access, closing deals).

| Rank | Theme | Items | Freq | Severity |
|------|-------|-------|------|----------|
| 1 | **Billing transparency & predictability** | T-101, T-103, T-102 (partial) | 3 | High — drives confusion, churn, and manual work |
| 2 | **Plan change UX creates fear of data loss or unexpected charges** | T-101, T-104 | 2 | High — T-104 is confirmed churn |
| 3 | **Invoice management is manual and unscalable for Enterprise** | T-102, T-107 | 2 | High — recurring finance-team pain at quarter-end |
| 4 | **Failed payment handling causes abrupt account lockout** | T-106 | 1 | High — sudden loss of access is severe, though thin evidence |
| 5 | **Pricing model doesn't match Enterprise buying patterns** | T-105 | 1 | Medium — revenue risk, but single sales signal |

---

## Evidence by Theme

### Theme 1 — Billing Transparency & Predictability
**Underlying problem:** Customers cannot understand or anticipate what they will be charged, and the product offers no explanation when amounts change.
- **T-101** (SMB, support): Double charge after mid-cycle upgrade; proration logic never explained by support.
- **T-103** (SMB, interview): Bill amounts vary unexpectedly; customer has no way to audit why.
- **T-102** (Enterprise, support): Charges must be manually split by cost center — implies the invoice itself provides insufficient charge-level detail.

> Note: T-102 is primarily an invoice-format problem (Theme 3) but also reflects missing billing granularity.

---

### Theme 2 — Plan Change UX Creates Risk (Charges or Data Loss)
**Underlying problem:** The upgrade/downgrade flow does not clearly communicate consequences — financial or data-related — before the customer commits.
- **T-101** (SMB, support): Unexpected double charge after upgrade; customer didn't understand mid-cycle proration.
- **T-104** (SMB, review): Cancelled the product rather than risk downgrading without knowing whether data would survive. Confirmed churn.

---

### Theme 3 — Invoice Management is Manual and Unscalable for Enterprise
**Underlying problem:** Invoices lack cost-center attribution and cannot be retrieved in bulk, forcing AP teams to do expensive manual work.
- **T-102** (Enterprise, support): Finance manually splits invoices by cost center every month.
- **T-107** (Enterprise, interview): No bulk invoice download; quarter-end reconciliation takes hours.

---

### Theme 4 — Failed Payment Flow Causes Abrupt Account Lockout
**Underlying problem:** The dunning/recovery flow skips proactive communication and locks accounts immediately on payment failure, with no grace period or warning.
- **T-106** (SMB, support): Account locked instantly after failed payment; no warning email sent. Customer blindsided.

> ⚠️ Thin evidence — single item. Severity is high enough to warrant investigation before dismissing.

---

### Theme 5 — Pricing Model Doesn't Support Enterprise Buying Patterns
**Underlying problem:** The flat-tier pricing structure prevents closing deals that require usage-based pricing with committed minimums — a common Enterprise procurement pattern.
- **T-105** (Enterprise, sales): Active prospect lost or stalled due to pricing model mismatch.

> ⚠️ Thin evidence — single sales-call signal. Could reflect one outlier or a systemic gap; needs validation.

---

## Segments Affected

| Segment | Themes |
|---------|--------|
| **SMB** | Themes 1, 2, 4 — primarily billing confusion, churn risk, payment recovery |
| **Enterprise** | Themes 3, 5 — primarily operational finance burden and pricing model fit |
| **Both** | Theme 1 (billing transparency) has signals in both segments |

---

## Open Questions / Validate Next

1. **Theme 1 — How widespread is proration confusion?** Query support tickets for "proration," "charged twice," "billing question" — is T-101/T-103 a pattern or an edge case?
2. **Theme 2 — How often do users abandon plan changes mid-flow?** Pull funnel drop-off data on the upgrade/downgrade screens. T-104 is a churn data point but we don't know abandonment rate.
3. **Theme 4 — What is the current dunning sequence?** Audit the payment-failure workflow. Check whether a warning email is configured at all. Survey recent locked-out accounts to gauge frequency.
4. **Theme 5 — Is usage-based pricing a one-off ask or a sales pattern?** Interview 3–5 AEs: how often does pricing model come up as a blocker? Check CRM lost-deal reasons.
5. **Theme 3 — What invoice formats do Enterprise competitors offer?** Competitive teardown + 2–3 customer interviews to spec the minimum viable cost-center and bulk-download requirements.

---
_Run metrics: 27.8s, 402 in / 1250 out tokens, ~$0.02_
