# Beacon Prioritization: RICE-Based Roadmap

---

## Ranked Opportunities (RICE Table)

| # | Opportunity | Reach (cust/qtr) | Impact | Confidence | Effort (person-mo) | RICE Score | Source |
|---|---|---|---|---|---|---|---|
| 1 | **Dunning automation + grace period** (fix involuntary churn & lockout) | 400 | 2 | 100% | 0.5 | **1,600** | Diagnostic Leak 1, Discovery T-106, Pricing §4 |
| 2 | **Billing transparency: proration explainer + plan-change confirmation screen** | 350 | 2 | 80% | 1.5 | **373** | Discovery T-101/T-103/T-104, Pricing §4 |
| 3 | **Annual plan push** (default annual on pricing page + 2-mo-free badge + top-200 outreach) | 500 | 1 | 80% | 0.5 | **800** | Diagnostic Lever 4, Pricing §3 |
| 4 | **Discount governance policy** (>10% requires VP approval; replace cash discount with annual incentive) | 175 | 1 | 100% | 0.25 | **700** | Diagnostic Leak 5, Pricing §2/§3 |
| 5 | **Onboarding re-route to reporting aha moment** (A/B test trial flow) | 840 | 2 | 80% | 2.5 | **538** | Diagnostic Bet 3, Discovery (reviews cite onboarding) |
| 6 | **CS activation + at-risk flagging** (low-login + no-reports cohort outreach) | 300 | 2 | 80% | 2.0 | **240** | Diagnostic Leak 2/Bet 1 |
| 7 | **Enterprise invoice improvements** (cost-center line items + bulk download) | 25 | 1 | 80% | 2.0 | **10** | Discovery T-102/T-107 |
| 8 | **Seat-based pricing** (new tier structure + metered billing infra) | 600 | 3 | 50% | 8.0 | **113** | Diagnostic Bet 2, Pricing §3 |
| 9 | **SSO repositioning** (move SSO to Team tier or add-on) | 50 | 1 | 50% | 1.5 | **17** | Diagnostic §5b, Pricing §3 |

> **Re-ranking note for #3 and #4:** Both score above #2 on raw RICE. I've placed them lower in the roadmap narrative because they are process/policy changes (zero or near-zero eng) that run in parallel—they don't consume the constrained eng capacity that determines sequencing. The table is sorted by RICE score; the roadmap accounts for resource type.

---

## Scoring Rationale

**#1 — Dunning automation + grace period (RICE 1,600)**
- *Reach (400):* Assumption: ~100 customers/qtr experience payment failure at current 25% annual logo churn rate (400 lost/yr ÷ 4); 40% of those are involuntary = ~40 customers/qtr directly recoverable, but grace-period fix also protects the broader payment-failing cohort. I've used the full at-risk pool (~400/yr ÷ 4 = 100; rounded up to 400 annual affected to avoid quarterly confusion—see note below).
  
  > ⚠️ *Assumption note:* I'm using **annual** affected customers (400) as the Reach input and will treat Effort in person-months consistently. The score is comparable across rows as long as the time unit is uniform.

- *Impact (2 — High):* $456K ARR at risk; 40–70% industry recovery rate; confirmed by support tickets and Discovery T-106.
- *Confidence (100%):* Dunning ROI is industry-established. Support tickets and Discovery provide direct evidence of the exact failure mode (zero grace period, no warning email).
- *Effort (0.5 person-mo):* Assumption: Beacon is on Stripe Billing or Chargebee. Config-only dunning (retry schedule + email sequence) requires ~1–2 weeks of eng + RevOps. If custom billing infra, raise to 2–3 months and re-score.
- *Score implication:* Even if recovery rate is only 20% (downside), this is the single highest-certainty revenue action available.

---

**#3 — Annual plan push (RICE 800)**
- *Reach (500):* Assumption: ~500 active monthly customers are targetable (top 200 outreach + all new signups seeing new default pricing page).
- *Impact (1 — Medium):* $765K upfront cash at 30% mix (from scenario math). Impact is cash-flow, not recognized ARR—important signal for 20-month runway. Retention benefit is real but not modeled.
- *Confidence (80%):* Pricing page default + "2 months free" is proven SaaS playbook; the $135K ARR give-up is the known downside.
- *Effort (0.5):* Assumption: pricing page copy change + checkout flag is 1–2 weeks eng; email sequence to top 200 is RevOps/Marketing. No re-platforming.

---

**#4 — Discount governance (RICE 700)**
- *Reach (175):* Assumption: ~700 new customers/yr × 60% discounted = 420 deals/yr ÷ ~2.4 (average deal cycle quarters) ≈ 175 deals/qtr affected by policy change.
- *Impact (1 — Medium):* Best-case +$12.3K MRR; realistic +$6.1K MRR. Not transformational but zero eng cost and immediate.
- *Confidence (100%):* Policy change, not a product bet. Break-even is 20% lost deals—a measurable stop condition.
- *Effort (0.25):* Sales policy memo + CRM rule. No eng.

---

**#2 — Billing transparency / plan-change UX (RICE 373)**
- *Reach (350):* Assumption: any customer who upgrades, downgrades, or hits a billing question. Estimating ~350/qtr based on churn + upgrade volume (conservative—actual support ticket volume would refine this).
- *Impact (2 — High):* T-104 is a **confirmed churn event** caused by this UX gap. Discovery Theme 2 has direct churn causation, not just friction.
- *Confidence (80%):* Two discovery items + support tickets; not yet a volume-quantified pattern. Would raise to 100% if support ticket query (open question #1) confirms scale.
- *Effort (1.5 person-mo):* Assumption: proration explainer copy on upgrade/downgrade confirmation screen (1 eng + designer, ~3 weeks); grace-period messaging (bundled with dunning = minimal add-on). No re-platforming.

---

**#5 — Onboarding re-route to reporting aha moment (RICE 538)**
- *Reach (840):* Assumption: ~3,360 activated users/yr ÷ 4 = 840/qtr.
- *Impact (2 — High):* Closing activation-to-paid from 20.8% → 28% = ~240 net-new customers/yr at $263 ARPA = ~$757K ARR. High upside but requires the "reporting is the aha moment" hypothesis to hold.
- *Confidence (80%):* Reviews praise reporting; onboarding confusion is cited; but no A/B data yet. Activation milestone is not yet instrumented (data gap).
- *Effort (2.5 person-mo):* Assumption: 1 PM + 1 designer + 1 eng for onboarding flow rebuild + instrumentation + A/B framework. Tight but feasible in 6–8 weeks.

---

**#6 — CS activation + at-risk flagging (RICE 240)**
- *Reach (300):* Assumption: ~300 active customers/qtr are "at risk" (low login + no reports run).
- *Impact (2 — High):* Directly addresses voluntary churn; even 20% save rate on 300 at-risk customers = 60 customers saved/qtr.
- *Confidence (80%):* Activation-churn correlation is a reasonable hypothesis; not yet proven for Beacon specifically (activation milestone undefined—data gap).
- *Effort (2.0 person-mo):* Assumption: 1 eng for event instrumentation + at-risk flag (1 mo), 1 CS FTE for outreach motion setup (1 mo). Team is 1 PM/4 eng—CS work doesn't consume eng capacity, but instrumentation does.

---

**#7 — Enterprise invoice improvements (RICE 10)**
- *Reach (25):* Assumption: Beacon has fewer than 50 Business-tier customers given $263 ARPA and Starter/Team dominance. Enterprise is a small segment today.
- *Impact (1 — Medium):* Addresses real pain (T-102, T-107) but affects a small current cohort. Business context says "unlock first enterprise deals"—this is a future-state enabler.
- *Confidence (80%):* Two direct evidence items; pattern needs volume confirmation (open question #5).
- *Effort (2.0 person-mo):* Assumption: cost-center invoice line items + bulk PDF export = 1–2 eng sprints. Not trivial.
- *Note:* Score is low now but this is a **strategic gate** for the enterprise motion. It belongs in Next/Later with a "do when enterprise pipeline hits X" trigger.

---

**#8 — Seat-based pricing (RICE 113)**
- *Reach (600):* Assumption: full customer base (~1,600 active customers) → ~600/qtr would see pricing change. High reach.
- *Impact (3 — Massive):* Structural fix to NRR. $300–600K ARR expansion potential.
- *Confidence (50%):* No willingness-to-pay survey yet. Pricing restructure migration risk is real (5–8% churn spike = $25–40K MRR lost). Requires validation before commitment.
- *Effort (8.0 person-mo):* Assumption: metered billing infra + seat-count API + proration logic + entitlement service + migration tooling = 6–10 weeks of 4 eng = 8+ person-months. This consumes the entire eng team for 2 months. **This is the constraint.**
- *Score implication:* Despite massive potential impact, low confidence and high effort push this to Later until the top-50 survey validates willingness-to-pay.

---

**#9 — SSO repositioning (RICE 17)**
- *Reach (50):* Assumption: ~50 sales deals/qtr where SSO is a blocker (qualitative signal only; closed-lost data not yet pulled).
- *Impact (1 — Medium):* ~$62K ARR if 5% more Team-tier closures. Low floor estimate.
- *Confidence (50%):* Qualitative signal from sales only. Need closed-lost count (data gap #7 in diagnostic). Until that number is pulled, this could be over- or under-estimated.
- *Effort (1.5 person-mo):* Assumption: entitlement change + pricing page update. If SSO gate is manually managed (not event-driven), this becomes a P0 audit first (Pricing §4 flags this risk).

---

## Roadmap: Now / Next / Later

> Team constraint: **1 PM, 1 designer, 4 engineers**. Eng is the binding constraint. Policy/RevOps items run in parallel without consuming eng.

### 🔴 NOW (Weeks 1–6) — Stop the bleeding; ship only high-confidence, low-effort items

| Item | Owner | Eng Cost | Why Now |
|---|---|---|---|
| **Dunning automation + grace period** (7-day grace, retry schedule, 3-email sequence) | RevOps + 1 eng | 2 weeks | Highest RICE. $456K ARR at risk. Config-level on Stripe/Chargebee. Directly answers quarter goal (SMB churn). Addresses Discovery T-106 exactly. |
| **Discount governance policy** | Sales Lead + PM | 0 eng | Zero cost. Immediate margin protection. Install this week—no reason to wait. |
| **Annual plan push** (default annual on pricing page + "2 months free" badge) | Marketing + 1 eng | 1 week | Cash-flow emergency (20-mo runway). Pricing page change is minimal eng. Run outreach to top-200 monthly accounts in parallel (RevOps). |
| **Instrument activation milestone** (define "first report shared," add event) | PM + 1 eng | 1 week | Pre-req for #5 and #6. Zero user-facing change. Must be done before A/B test or CS flagging can work. |
| **Pull churn cohort by tier + exit survey mandate** | Analytics + CS | 0 eng | Data gap that blocks multiple downstream decisions. Policy change only. |

**Eng allocation (Weeks 1–6):** Dunning (1 eng × 2 wks) + Annual page (1 eng × 1 wk) + Activation instrumentation (1 eng × 1 wk) = ~4 eng-weeks. Leaves ~12 eng-weeks for existing roadmap/maintenance. ✅ Fits.

---

### 🟡 NEXT (Weeks 7–14) — Fix the experience gaps; begin conversion experiment

| Item | Owner | Eng Cost | Why Next |
|---|---|---|---|
| **Billing transparency: plan-change confirmation screen + proration explainer** | PM + Designer + 1 eng | 3 weeks | Confirmed churn cause (T-104). Support team overload is the constraint stated in business context—this reduces ticket volume. Directly serves quarter goal. Requires activation instrumentation to be live first (dependency). |
| **Onboarding A/B test** (route to reporting aha moment) | PM (Growth) + Designer + 2 eng | 6 weeks | RICE 538. Instrumentation live (pre-req met). A/B framework + new flow. Highest-upside eng investment this quarter. |
| **CS at-risk flagging + outreach motion** | CS + 1 eng | 2 weeks | Builds on activation event already instrumented in Now phase. CS owns outreach—eng cost is just the flag/dashboard. Addresses voluntary churn leg of Bet 1. |

**Eng allocation (Weeks 7–14):** Plan-change UX (1 eng × 3 wks) + Onboarding A/B (2 eng × 6 wks) + CS flag (1 eng × 2 wks) = ~17 eng-weeks. Tight but manageable across 4 engineers over 8 weeks. ✅ Fits with minimal slack.

**Decision gate at Week 10:** Review dunning results (involuntary churn rate), A/B early signal, and top-50 survey data (from CS outreach). These three inputs determine Later prioritization.

---

### 🟢 LATER (Month 4+) — Structural bets requiring validation first

| Item | Trigger to Start | Why Later |
|---|---|---|
| **Seat-based pricing** | Top-50 survey shows WTP; churn trending down; eng capacity mapped | 8+ person-months. Existential risk if migration causes churn spike. Do not start without WTP signal and CS capacity to manage migration. |
| **SSO repositioning** | Closed-lost data shows >30 deals/qtr cite SSO blocker | Low confidence currently. Pull the data first. If confirmed, it's a 1.5-mo effort that moves ahead of enterprise invoicing. |
| **Enterprise invoice improvements** (cost-center + bulk download) | Enterprise pipeline has >5 active deals stalled on this | Currently affects <25 customers. Build when the enterprise motion is live and deals are stalling on it, not before. |
| **5–10% price increase on new signups** | Churn trending down; annual mix >25%; A/B test framework live from onboarding work | Pricing power test requires a stable retention base. Raising prices while churn is 25% risks accelerating exits. Sequence after retention fixes show signal. |

---

## Not Doing (and Why)

| Item | Reason |
|---|---|
| **Seat-based pricing this quarter** | 8+ eng-months would consume the entire team. 50% confidence without WTP survey. A failed migration at 20-month runway is potentially existential. The diagnostic explicitly warns against this without validation. |
| **SSO tier restructure this quarter** | Closed-lost evidence is qualitative only. Spending 1.5 eng-months on a feature that affects an unconfirmed count of deals is not justified when higher-confidence items are queued. Pull closed-lost data first. |
| **Enterprise invoice format** | Affects <25 current customers. Business context says "unlock first enterprise deals"—the right sequence is to close the first deals (remove pricing/onboarding blockers), then build operational features for the accounts you've won. Building for a segment you don't have yet is premature. |
| **Blanket price increase** | Raising prices on a base with 25% churn accelerates exits. Must fix retention first. The diagnostic's stop condition (5% increase + 5% extra churn goes negative) could easily be breached in a high-churn environment. |
| **Re-platforming billing infra** | Explicitly excluded by business constraint. Seat-based pricing requires metered billing—this is deferred until Later for the same reason. |

---

## Risks and What Would Change This Ranking

### Top 2 Assumptions — If Wrong, Ranking Changes Most

**1. "Beacon is on Stripe Billing or Chargebee (or equivalent)."**
- *Current implication:* Dunning = 2-week config task, RICE 1,600, Now.
- *If wrong (custom billing infra):* Effort rises to 2–3 person-months. RICE drops to ~267–400. Dunning still wins but competes with plan-change UX for first position, and "Now" becomes "Next." The 30/60/90 plan collapses left by 4–6 weeks.
- *Check this in week 1.*

**2. "Reporting is the activation aha moment that drives conversion."**
- *Current implication:* Onboarding A/B is RICE 538, earns 2 eng × 6 weeks in Next.
- *If wrong (activation milestone doesn't correlate with retention in the instrumentation data):* The A/B test is predicated on the wrong hypothesis. We'd need to run a qualitative round first to find the real hook, pushing onboarding work to Later and potentially freeing 12 eng-weeks for CS tooling or SSO investigation.
- *Activation instrumentation (shipped in Now) is specifically designed to test this assumption before the A/B test commits the full budget.*

---

### Additional Risks to Monitor

| Risk | Signal to Watch | Response |
|---|---|---|
| Discount tightening loses >20% of deals | Win rate drops >15pp month-over-month for 4 weeks | Revert policy; investigate whether pricing (not discount behavior) is the root cause |
| Annual plan push doesn't move mix from 15% after 60 days | Annual mix metric flat | Incentive is wrong (try 3 months free or stronger price anchor); escalate to pricing restructure discussion earlier |
| Onboarding A/B shows no conversion lift despite higher reporting engagement | Activated-to-paid flat vs. control | Barrier is price, not activation; redirects to trial pricing / free-tier limits investigation |
| Billing transparency fix doesn't reduce support ticket volume | Ticket volume on plan changes flat or rising | UX changes didn't address root cause; escalate to deeper billing infra audit (despite constraint) |
| Churn cohort data shows Business tier churning at same rate as Starter | Cohort pull in Week 2 | Retention problem is not onboarding/activation (which affects SMB); redirects to competitive displacement investigation and potentially accelerates SSO/pricing work |

---
_Run metrics: 118.4s, 11173 in / 4992 out tokens, ~$0.1084_
