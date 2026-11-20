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
