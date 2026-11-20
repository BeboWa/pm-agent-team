# Measurement & Experimentation Plan: BEACON-001 Dunning Automation + Grace Period

---

## Metric Framework

### Primary Metric
**Payment Failure Recovery Rate** — percentage of accounts that enter a dunning sequence and successfully recover payment within the 7-day grace period.

- **Baseline:** 0% (no dunning mechanism exists; all failures result in immediate lockout)
- **Target:** ≥40% recovery rate within 60 days of launch
- **Why this is primary:** It is the direct, proximal outcome the feature controls, it moves fast enough to be observable within one billing cycle, and it is a leading indicator of all downstream revenue metrics. Involuntary churn rate and ARR recovered are consequences of this rate.

### Supporting Metrics

| Metric | Baseline | Target | Cadence |
|---|---|---|---|
| Involuntary churn logos per quarter | Unknown — establish in Week 1 via churn cohort tagging | ≥40% reduction within 60 days | Monthly |
| ARR recovered from dunning cohort | $0 | ≥$90K in first two quarters | Quarterly |
| Dunning email open rate (Day 0 email) | No prior sends | ≥25% floor; flag below this as deliverability issue | Weekly for first 4 weeks |
| Dunning email click-through rate (payment link) | No prior sends | Track as directional signal; no hard target yet | Weekly |
| Median days-to-recovery for accounts that do recover | Unknown | Establish distribution; watch for "Day 1 spike" indicating transient failures self-resolving | Per cohort |
| Grace period accounts that reach Day 7 without recovery | 100% today | Decreasing trend | Weekly |

### Guardrail Metrics
These must not degrade. Any regression triggers an immediate review gate before continuing rollout.

| Guardrail | Threshold to Pause | Why |
|---|---|---|
| **Duplicate charge rate** | Any confirmed duplicate charge → auto-pause dunning + page on-call eng | Idempotency failure; legal and customer trust risk |
| **Failed-payment rate** (new failures entering dunning per week) | >20% week-over-week increase vs. 4-week rolling average | Could signal retry logic triggering new failures or data quality issue |
| **Refund rate** | >2× pre-launch baseline | Indicates customers being charged incorrectly during retry sequence |
| **Billing-related support ticket volume** | Should fall ≥50% within 30 days; if it *increases* >20% above baseline → investigate immediately | Rising tickets post-launch may indicate email deliverability failure or confusing lockout UX |
| **Involuntary churn rate** | Should not increase; any increase vs. pre-launch baseline at 30 days → halt and audit | The feature must not make involuntary churn worse (e.g., via retry exhaustion triggering earlier lockouts) |
| **Transactional email bounce/spam rate** | >5% hard bounce or >0.1% spam complaint rate → halt email sends, audit ESP configuration | Deliverability failure means customers receive no warning; grace period becomes invisible |

---

## Tracking Plan

All events should be logged to your analytics warehouse and mirrored in the support audit log (M-6). Instrument before Phase 2 rollout begins.

### Event Definitions

| Event Name | Trigger | Key Properties |
|---|---|---|
| `dunning_sequence_started` | Payment failure detected by billing platform, dunning sequence initialized | `account_id`, `plan_tier` (Starter/Team), `failure_reason` (from processor), `mrr_at_risk`, `billing_contact_email_hash`, `timestamp`, `billing_platform` |
| `dunning_retry_attempted` | Automated retry fires per schedule | `account_id`, `retry_number` (1/2/3), `retry_day` (1/3/7), `outcome` (success/failure), `failure_reason_on_retry`, `timestamp` |
| `dunning_email_sent` | Each warning email dispatched by ESP | `account_id`, `email_type` (day_0_warning / day_3_reminder / day_6_final), `recipient_role` (billing_contact / account_admin), `esp_message_id`, `timestamp` |
| `dunning_email_delivered` | Delivery confirmation received from ESP | `account_id`, `email_type`, `esp_message_id`, `timestamp` |
| `dunning_email_opened` | Open event from ESP | `account_id`, `email_type`, `hours_since_send`, `timestamp` |
| `dunning_email_clicked` | Click on payment update link | `account_id`, `email_type`, `link_destination`, `timestamp` |
| `dunning_email_bounced` | Hard or soft bounce from ESP | `account_id`, `email_type`, `bounce_type` (hard/soft), `timestamp` |
| `dunning_payment_recovered` | Successful payment processed during grace period | `account_id`, `recovery_day` (0–7), `recovery_trigger` (retry_success / customer_updated_method), `plan_tier`, `mrr_recovered`, `timestamp` |
| `dunning_account_locked` | Grace period elapsed, all retries exhausted, lockout enforced | `account_id`, `plan_tier`, `mrr_lost`, `total_retries_attempted`, `emails_sent_count`, `timestamp` |
| `dunning_sequence_cancelled` | Account recovers mid-sequence; sequence halted | `account_id`, `cancel_reason` (payment_recovered), `day_in_sequence`, `timestamp` |
| `dunning_banner_viewed` | In-app banner displayed to user (if S-1 ships) | `account_id`, `user_id`, `days_remaining_in_grace`, `page_context`, `timestamp` |
| `dunning_banner_clicked` | User clicks CTA on in-app banner | `account_id`, `user_id`, `cta_destination`, `timestamp` |
| `support_ticket_created` | New inbound support ticket (tag existing pipeline) | `account_id` (if resolvable), `ticket_category` (billing_lockout / billing_other / non_billing), `channel`, `timestamp` — **this is a retroactive tag, not new instrumentation; apply to historical data for baseline** |

### Measurement Notes
- `account_id` is the unit of analysis throughout. All metrics are account-level, not user-level.
- `mrr_at_risk` and `mrr_recovered` enable direct ARR impact calculation without additional joins.
- `failure_reason` from the processor (insufficient_funds, card_expired, do_not_honor, etc.) should be preserved raw; it will be needed to diagnose why some accounts don't recover.
- The `support_ticket_created` tag requires a manual or rule-based categorization pass on the existing support queue — assign to Support Lead, zero eng cost.

---

## Experiment Design

### Why a Randomized A/B Test Is Not the Right design here

A classical A/B test (hold-back group receives no dunning) is **not recommended** for this feature:

1. **Ethical and legal exposure:** A hold-back group would deliberately receive no warning before lockout. Given that PRD §7 flags a potential ToS obligation and legal review of the grace period policy, running a control group with intentional lockout is not advisable.
2. **Traffic volume:** The at-risk pool is ~40 accounts per quarter (~3–4 accounts per week). A hold-back A/B would require many months to reach significance on account-level outcomes.
3. **Baseline is unambiguous:** Recovery rate is 0% today by construction (no mechanism exists). Any positive recovery rate is a confirmed improvement; the direction of effect is not in question.

**Recommended design: Phased Rollout with Pre/Post Controls**

| Phase | Accounts | Treatment | Purpose |
|---|---|---|---|
| Phase 0 (Week 1–2 pre-launch) | All accounts | No dunning (status quo) | Establish baselines: support ticket volume, involuntary churn tagging, accounts entering payment failure state |
| Phase 2 rollout (Week 3+) | New payment failures only (forward-looking) | Full dunning sequence | Measure recovery rate vs. 0% baseline; do not backfill historical failures |
| Ongoing | All new payment failures | Full dunning sequence | Track cohort-by-cohort recovery rates; compare each weekly cohort to the established baseline |

**Unit of randomization (if future variant testing is needed):** `account_id`. Do not randomize at user level — multiple users share one account's billing status.

**Future A/B opportunity (not in BEACON-001 scope):** Once dunning is live and baseline recovery rates are established (60+ days), variant testing on email copy, subject lines, send timing, or in-app banner variants is feasible and appropriate. At that point, test at the `account_id` level within the dunning-entered cohort. Required inputs before designing that test: baseline recovery rate (will be available after this rollout), minimum detectable effect (suggest 10pp lift as meaningful), and weekly dunning-entry volume (available from `dunning_sequence_started` events).

**When a phased rollout is not feasible:** If billing platform confirmation (OQ-1) reveals custom infrastructure, the effort timeline shifts to 2–3 person-months. In that case, all measurement plan inputs remain valid, but Phase 0 baseline collection should begin immediately and independently of the build, buying clean pre-launch data.

**Duration guidance:** Monitor for a minimum of 60 days post-launch before making a "ship / iterate / kill" call on the feature as designed. The primary cohorts are quarterly billing cycles; 60 days captures 2 billing cycles and gives enough dunning-entry events at 3–4/week to draw directional conclusions (expect 25–35 accounts in the cohort by Day 60).

---

## Decision Rules

Pre-committed before data arrives. Do not adjust thresholds after seeing results.

### At Day 30 Review

| Condition | Decision |
|---|---|
| Recovery rate ≥20% AND no guardrail breaches | ✅ **Continue to Day 60 review.** Feature is working at minimum viable threshold. |
| Recovery rate <20% AND email open rate <25% | 🔁 **Iterate on deliverability first.** Audit ESP, SPF/DKIM/DMARC, bounce handling. Do not conclude the mechanism is broken until email is confirmed to be reaching customers. |
| Recovery rate <20% AND email open rate ≥25% | 🔁 **Iterate on conversion path.** Emails are being read but customers aren't updating payment. Investigate: is the payment update link working? Is the in-app banner (S-1) live? Prioritize C-1 (magic link) in next sprint. |
| Any duplicate charge event confirmed | 🛑 **Kill/pause immediately.** Auto-pause dunning per rollout plan. Investigate idempotency failure. Do not resume until root cause is confirmed and fixed. |
| Billing support tickets increase >20% above pre-launch baseline | 🛑 **Pause and audit.** Rising tickets post-launch indicates the feature is creating confusion, not resolving it. |

### At Day 60 Review (Primary Decision Gate)

| Condition | Decision |
|---|---|
| Recovery rate ≥40% AND involuntary churn trending down ≥40% | ✅ **Ship as permanent feature.** Report ARR recovered. Begin scoping S-1 banner if not already live and email-only variants (C-1, C-2) for next iteration. |
| Recovery rate 20–39% | 🔁 **Iterate.** Feature is producing value but below target. Prioritize: (1) in-app banner S-1 if deferred, (2) magic-link C-1, (3) billing-contact data quality audit. Reset 30-day target after each change. |
| Recovery rate <20% after deliverability and conversion path are confirmed working | 🔁 **Escalate.** Root cause is likely data quality (stale billing contact emails) or structural (customers have no valid payment method to switch to). Pull sample of non-recovered accounts; interview 5–10. This is a CS/product discovery issue, not a measurement issue. |
| Involuntary churn rate is flat or increasing despite recovery rate ≥20% | 🔁 **Audit churn tagging.** The classification of voluntary vs. involuntary churn may be wrong. Re-run churn cohort pull with updated tagging logic. |
| Any guardrail breach sustained over 2+ weeks | 🛑 **Kill/pause.** Do not proceed to full validation until breach is resolved and root cause is documented. |

### ARR Recovery Target (Quarters 1–2)

- If ARR recovered from dunning cohort is on track for ≥$90K annualized at Day 60 → feature is meeting its revenue hypothesis; no reprioritization needed.
- If ARR recovered is tracking toward <$45K annualized → flag to PM and leadership at Day 60 readout; reassess whether BEACON-001's ARR recovery assumption was correct or whether the at-risk pool ($456K) was overstated.

---

## Readout Template

**Use at Day 30 and Day 60. Circulate to PM, RevOps, CS Lead, Engineering Lead, and Finance.**

---

```
BEACON-001 Dunning Automation — [Day 30 / Day 60] Readout
Reporting period: [start date] → [end date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIMARY METRIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Payment Failure Recovery Rate
  Accounts entered dunning:        [N]
  Accounts recovered:               [N] ([X]%)
  Target:                           ≥40% by Day 60
  Status:                           [On track / At risk / Breached]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUPPORTING METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Involuntary churn logos (this period vs. pre-launch baseline):
  Pre-launch baseline (quarterly run rate):  [N logos]
  This period (annualized):                  [N logos] ([Δ]%)
  
ARR recovered from dunning:
  This period:        $[X]K
  Projected Q1–Q2:    $[X]K  (target: $90K)

Dunning email funnel:
  Sent:               [N]
  Delivered:          [N] ([X]%)
  Opened:             [N] ([X]%)  ← flag if <25%
  Clicked (pay link): [N] ([X]%)

Billing support tickets:
  Pre-launch baseline (weekly avg): [N]
  Post-launch (weekly avg):          [N] ([Δ]%)
  Target:                            -50% by Day 30

Recovery timing distribution:
  Recovered Day 0–1 (transient failures):  [N] ([X]%)
  Recovered Day 2–4:                       [N] ([X]%)
  Recovered Day 5–7:                       [N] ([X]%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GUARDRAIL STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Duplicate charges:          [0 / N — BREACH if >0]
Refund rate:                [X%] vs. baseline [X%]
Email bounce/spam rate:     [X%]  ← flag if >5% hard bounce
Support ticket trend:       [Up / Flat / Down]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Ship / continue as-is
[ ] Iterate — specific action: [description]
[ ] Pause — reason: [description]
[ ] Kill — reason: [description]

Rationale: [1–3 sentences linking data to decision rule]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPEN ISSUES / BLOCKERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[List any unresolved OQs from the PRD, e.g., billing contact data quality,
churn tagging completeness, legal ToS update status]
```

---

## Feedback Loop

### What Flows Back to Discovery

| Signal | Destination | Trigger | Action |
|---|---|---|---|
| Recovery rate <20% after deliverability confirmed | Discovery backlog | Day 30 or Day 60 | Scope magic-link payment update (C-1) or investigate billing contact data quality as a new discovery workstream |
| >50% of non-recovered accounts share a common `failure_reason` (e.g., do_not_honor, card_blocked) | Discovery + CS | Day 60 | These accounts may need proactive CS outreach or a self-serve payment method update UI before dunning is initiated — scope as follow-on feature |
| Dunning email open rate is healthy but click-through is low | Discovery | Day 30 | The payment update page (link destination) may have UX friction; scope a usability review of the payment update flow |
| `dunning_banner_viewed` events show high volume but `dunning_banner_clicked` is low | Discovery | If S-1 ships; Day 30 | Banner copy or CTA is not driving action; A/B test banner variants in next sprint |
| ARR recovered is on track but involuntary churn is not declining proportionally | Analytics | Day 60 | Churn tagging methodology may be wrong; or some "involuntary churn" is actually voluntary — refeed into churn cohort analysis |

### What Flows Back to the Company Diagnostic

| Metric | Diagnostic Update | Timing |
|---|---|---|
| Confirmed payment failure recovery rate at Day 60 | Updates Diagnostic Leak 1 estimate. If recovery rate ≥40%: revise GRR trajectory upward; revise the "$456K at-risk ARR" to show confirmed recovery. If <40%: revise the $180K–$320K recovery confidence downward and flag for Bet 1 reassessment. | Day 60 readout |
| Actual ARR recovered in Q1–Q2 | Replaces the "conservative recovery estimate" in the Diagnostic with observed data; recalculates NRR trajectory | End of Q2 |
| Churn cohort tagging output (involuntary vs. voluntary breakdown) | Fills Data Gap #1 in the Diagnostic (churn reasons); directly informs whether Bet 1 ("Stop the Bleed") is on track or whether voluntary churn requires a separate intervention | Week 2 baseline, then ongoing |
| Support ticket volume trend | Validates or invalidates the assumption that immediate lockout is driving support load; if tickets do not drop, root cause may be elsewhere — feeds into CS workload planning | Day 30 |
| `failure_reason` distribution across dunning cohort | New data the Diagnostic did not have. If a majority of failures are card_expired (predictable), this supports building pre-expiry alerts as BEACON-001 follow-on. If majority are do_not_honor (bank declines), recovery ceiling may be structurally lower than 40–70% industry benchmark — recalibrate projections. | Day 60 |

### Standing Feedback Cadence

- **Weekly (Weeks 3–6):** RevOps reviews `dunning_sequence_started` count, email delivery rate, and guardrail dashboard. Flags anomalies to PM same day.
- **Day 30:** Full readout per template above. PM and Analytics lead update the Diagnostic Leak 1 section with observed data.
- **Day 60:** Primary decision gate. Readout feeds directly into the Week 10 roadmap decision gate (per PRD §8) alongside dunning data, top-50 survey results, and onboarding A/B early signal.
- **Quarterly:** ARR recovered from dunning is reported to Finance as a line item; updates the $456K at-risk calculation with actuals.

---
_Run metrics: 114.8s, 9896 in / 5079 out tokens, ~$0.1059_
