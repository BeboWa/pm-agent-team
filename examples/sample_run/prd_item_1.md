# PRD: Dunning Automation + Grace Period

**Feature ID:** BEACON-001
**Priority Rank:** #1 (RICE 1,600)
**Status:** Ready for scoping
**Estimated Effort:** 0.5 person-months (~2 weeks eng + RevOps)
**PM Owner:** TBD
**Last Updated:** [Date]

---

## 1. Problem and Evidence

### What is happening

Beacon customers whose payment methods fail are being locked out of the product immediately, with no warning emails sent before lockout and no grace period to resolve the issue. The customer discovers the problem only after losing access.

### Evidence

| Source | Signal |
|---|---|
| **Diagnostic Leak 1** | Involuntary churn identified as a primary revenue leak; estimated 40% of churned logos (~40 customers/quarter) lost to payment failure, not dissatisfaction |
| **Discovery T-106** | Direct customer evidence of the exact failure mode: zero grace period, no warning email sent before lockout |
| **Pricing §4** | $456K ARR at risk from involuntary churn cohort |
| **Business context** | Support team is overloaded with billing tickets; immediate lockout drives support volume |

### Why this is #1

Industry dunning recovery rates run 40–70%. Even at a conservative 20% recovery rate on the at-risk pool, this is the highest-certainty, lowest-effort revenue action available. It is a configuration change on existing billing infrastructure, not a product build—making it uniquely asymmetric on effort vs. impact.

### Assumption flagged by upstream report

> ⚠️ **Critical assumption:** This effort estimate (0.5 person-months) assumes Beacon runs on Stripe Billing, Chargebee, or an equivalent platform with native dunning configuration. If Beacon uses custom billing infrastructure, effort rises to 2–3 person-months and sequencing must be revisited. **Verify billing platform in Week 1 before committing to this timeline.**

---

## 2. Goals and Non-Goals

### Goals

1. Eliminate involuntary churn caused by payment failure and immediate account lockout
2. Give customers fair warning and time to resolve payment issues before service is interrupted
3. Reduce inbound support ticket volume related to unexpected account lockouts
4. Recover a measurable portion of the $456K ARR currently at risk from payment failure

### Non-Goals

- **Not** rebuilding or re-platforming billing infrastructure this quarter
- **Not** changing pricing, plan structure, or proration logic (see BEACON-002)
- **Not** building a self-serve payment method update UI (may be a follow-on; not in scope here)
- **Not** retroactively recovering accounts already churned before this feature ships
- **Not** handling voluntary cancellations (separate CS motion, see BEACON-006)
- **Not** covering enterprise-specific invoice workflows (see BEACON-007)

---

## 3. Target Users

### Primary: SMB customers experiencing payment failure

- Starter and Team tier customers (Beacon's dominant segments by volume)
- Typically a founder, ops lead, or finance contact who set up billing and may not check email daily
- Not necessarily expecting a failure — card expiry and bank declines often surprise them
- Consequence of lockout is high: they lose access to a tool they depend on operationally

### Secondary: Beacon support team

- Currently overloaded with billing tickets
- Today they handle lockout complaints reactively; this feature shifts the resolution to the customer before escalation is needed

### Out of scope for this feature

- Prospects (pre-purchase)
- Business/enterprise tier customers (small cohort; different billing contacts and processes)

---

## 4. Requirements (Must / Should / Could)

### Must (required for initial ship)

| ID | Requirement |
|---|---|
| M-1 | Configure automated payment retry schedule: retry on Day 1, Day 3, and Day 7 after initial failure |
| M-2 | Send a warning email to the billing contact on Day 0 (payment failure detected), Day 3 (second failure), and Day 6 (final warning, 24 hours before lockout) |
| M-3 | Enforce a **7-day grace period**: account remains fully accessible from initial failure through Day 7 |
| M-4 | Lock account only after all retries are exhausted and the 7-day grace period has elapsed without resolution |
| M-5 | Each warning email must include: the reason for failure (where available from the payment processor), a direct link to update payment method, and the date access will be suspended if unresolved |
| M-6 | Log all dunning events (failure detected, retries attempted, emails sent, resolution or lockout) with timestamps in an auditable record accessible to Beacon's support team |

### Should (high value, include if timeline holds)

| ID | Requirement |
|---|---|
| S-1 | Display an in-app banner to the account owner when a payment failure is active, visible on every page within the app during the grace period |
| S-2 | Auto-resolve the dunning sequence (dismiss banner, stop email sequence, restore full status) immediately when a successful payment is processed, without requiring manual support intervention |
| S-3 | Send a confirmation email to the billing contact upon successful payment recovery |
| S-4 | Notify the assigned CS or account owner internally (Slack or CRM) when an account enters the dunning sequence, so CS can intervene proactively on high-value accounts |

### Could (nice-to-have, defer if timeline is at risk)

| ID | Requirement |
|---|---|
| C-1 | Allow the billing contact to update their payment method directly from the warning email (magic link or token-authenticated flow) without requiring login |
| C-2 | Segment dunning email copy by plan tier (Starter vs. Team) for relevance |
| C-3 | Expose a dunning-status field in the admin dashboard for support team filtering |

---

## 5. User Stories and Acceptance Criteria

---

### Story 1: Payment failure warning (billing contact)

**As a** billing contact whose payment method has failed,
**I want** to receive an immediate email notification explaining the failure and telling me how to fix it,
**so that** I can resolve the issue before losing access to Beacon.

**Acceptance Criteria:**

1. **Given** a payment attempt fails, **when** the failure event is received from the payment processor, **then** a warning email is sent to the billing contact within 15 minutes of failure detection.
2. **Given** the warning email is sent, **when** the billing contact opens it, **then** it contains: (a) a plain-language description of the failure reason, (b) the date on which account access will be suspended if unresolved, and (c) a working direct link to the payment method update page.
3. **Given** the payment has not been resolved, **when** Day 3 and Day 6 are reached, **then** follow-up reminder emails are sent automatically with the same required content elements.
4. **Given** the billing contact successfully updates their payment method and payment is processed, **when** recovery is confirmed, **then** no further dunning emails are sent and the billing contact receives a payment-confirmed email.

---

### Story 2: Grace period — account remains accessible

**As a** Beacon user at a company with a failed payment,
**I want** to continue using the product for 7 days while my billing contact resolves the issue,
**so that** my team's work is not disrupted by a payment processing delay.

**Acceptance Criteria:**

1. **Given** a payment failure is detected, **when** the account is in the grace period (Day 0 through Day 7), **then** all users at that account retain full access to all features they had before the failure.
2. **Given** the grace period has not elapsed, **when** an account owner logs in, **then** an in-app banner is displayed indicating the payment issue, the resolution deadline, and a link to fix it. *(Depends on S-1 shipping.)*
3. **Given** Day 7 has passed and all retries have failed and the payment method has not been updated, **when** the system checks account status, **then** the account is locked and users see a clear lockout screen with instructions to contact billing (not a generic error).
4. **Given** the billing contact resolves payment on any day within the grace period, **when** payment is confirmed, **then** access continues uninterrupted with no lockout and the grace-period banner is dismissed.

---

### Story 3: Automated retry schedule

**As a** RevOps or support team member,
**I want** the system to automatically retry failed payments on a defined schedule,
**so that** transient card failures (e.g., temporary bank holds) recover without any manual intervention.

**Acceptance Criteria:**

1. **Given** an initial payment failure, **when** the retry schedule runs, **then** a retry is attempted on Day 1, Day 3, and Day 7 (maximum 3 retries after initial failure).
2. **Given** any retry attempt succeeds, **when** payment is confirmed, **then** the dunning sequence stops immediately, the account remains accessible, and a success record is logged.
3. **Given** all retries are exhausted without success, **when** Day 7 is reached, **then** the account lockout is triggered and the event is logged with a full timeline of attempts.
4. **Pass/fail:** Retry attempts must not double-charge a customer. If a retry succeeds on Day 3, no further retry runs on Day 7.

---

### Story 4: Audit log for support team

**As a** Beacon support team member,
**I want** to see a complete dunning event history for any account,
**so that** I can answer customer questions about billing without needing to investigate manually or escalate.

**Acceptance Criteria:**

1. **Given** an account has entered a dunning sequence, **when** a support team member looks up the account, **then** they can see a timestamped log of: payment failure event, retry attempts (and outcomes), emails sent (recipient, timestamp, delivery status), and resolution or lockout event.
2. **Given** a customer contacts support claiming they were not warned before lockout, **when** support reviews the audit log, **then** the log provides sufficient evidence to confirm or refute the claim (email send timestamp and delivery status are recorded).
3. **Pass/fail:** Audit log entries are immutable; no support team action can delete or modify a dunning event record.

---

## 6. Success Metrics

| Metric | Baseline | Target / Hypothesis |
|---|---|---|
| **Involuntary churn rate** (logos lost to payment failure per quarter) | Unknown; measure first by tagging churn cohort by reason in Week 1–2 | Hypothesis: reduce involuntary churn logos by ≥40% within 60 days of launch (industry benchmark: 40–70% recovery rate; we apply 40% as the conservative floor) |
| **Payment failure recovery rate** | 0% (no dunning; all failures result in lockout) | Hypothesis: ≥40% of accounts entering a dunning sequence recover payment within the 7-day grace period |
| **ARR recovered from dunning** | $0 (no mechanism exists) | Hypothesis: recover ≥$90K ARR in first two quarters (20% of $456K at-risk pool at conservative recovery rate) |
| **Billing-related support tickets** | Unknown; measure first (establish baseline in Week 1 from support queue audit) | Hypothesis: inbound tickets citing unexpected account lockout decrease by ≥50% within 30 days of launch |
| **Dunning email open rate** | No prior sends | Track as leading indicator; industry benchmark ~40–50% for transactional billing email. Flag if open rate falls below 25% (deliverability or list quality issue) |

> **Measurement note:** Involuntary vs. voluntary churn must be tagged before this ships. The churn cohort pull and exit survey mandate (identified as a parallel Now-phase action in the roadmap) is a prerequisite for clean baseline measurement.

---

## 7. Risks, Dependencies, Open Questions

### Risks

| Risk | Likelihood | Severity | Mitigation |
|---|---|---|---|
| **Beacon uses custom billing infrastructure** (not Stripe/Chargebee) | Unknown | High — effort triples; timeline shifts to Next phase | **Verify billing platform in Week 1 before any design or eng work begins.** If custom infra confirmed, re-score and re-sequence. |
| **Warning emails land in spam** (transactional deliverability failure) | Medium | High — customer never sees warning; grace period is invisible | Confirm transactional email is routed through a reputable ESP (SendGrid, Postmark, etc.) with proper SPF/DKIM/DMARC. Test deliverability before launch. |
| **Billing contact email on file is wrong or stale** | Medium | Medium — email sent but not received by decision-maker | Add in-app banner (S-1) as a redundant channel. Consider notifying account admin role separately if different from billing contact. |
| **Grace period creates bad debt exposure** | Low | Low — 7 days is industry standard; ARR at risk per account is modest | Monitor outstanding balances during grace period. Flag to finance if any single account's ARR during grace period exceeds a threshold (e.g., $5K MRR). |
| **Retry logic triggers duplicate charges** | Low | High — customer and legal/finance impact | Explicitly validate idempotency keys on retry calls to payment processor before shipping. Include in QA test plan. |

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Confirm billing platform (Stripe, Chargebee, or custom) | Engineering Lead | **Must resolve in Week 1** |
| Transactional email infrastructure is operational with deliverability monitoring | RevOps / Engineering | Confirm before launch |
| Churn cohort tagging by reason (involuntary vs. voluntary) | Analytics + CS | Needed for baseline; run in parallel (zero eng cost) |
| Payment method update page exists and is functional | Engineering | Confirm link destination before email copy is finalized |
| Support team briefing on new audit log location | CS / Support Lead | Pre-launch; no eng dependency |

### Flags for Legal, Finance, Security, and Compliance Review

> ⚠️ **Finance / Audit:** Dunning retry logic constitutes automated money movement. Retry schedule, charge amounts, and all outcomes must be logged in an immutable audit trail (addressed in M-6). Finance should confirm whether the retry schedule and grace period policy need to be reflected in Beacon's Terms of Service or customer billing agreements.

> ⚠️ **Legal / Compliance:** Review whether the 7-day grace period creates any contractual obligation (e.g., does it imply a service guarantee that modifies the existing SLA?). Confirm that warning email content (failure reason disclosure) is consistent with payment processor data-sharing agreements.

> ⚠️ **Security:** Token-authenticated or magic-link payment update flow (C-1, if built) must use short-lived, single-use tokens. Payment method update page must enforce HTTPS and comply with PCI-DSS scope rules — confirm that card data is not passed through Beacon's servers.

> ⚠️ **Tax / Proration:** This feature does not change billing amounts, proration, or refund logic. No tax implication expected. If a future iteration offers a grace-period discount to rescue a churning account, that would require a separate finance and legal review.

### Open Questions

| # | Question | Owner | Needed By |
|---|---|---|---|
| OQ-1 | What billing platform does Beacon run on? (Stripe, Chargebee, custom?) | Engineering Lead | Week 1 — blocks effort estimate |
| OQ-2 | Who is the "billing contact" in Beacon's data model — is it a distinct role, or the account owner? Can a customer have multiple billing contacts? | Engineering + PM | Week 1 — affects email targeting logic |
| OQ-3 | What is the current inbound support ticket volume specifically attributed to lockout / billing failures? | Support Lead | Week 1 — needed for baseline metric |
| OQ-4 | What is the current involuntary vs. voluntary churn breakdown? (Required for pre/post measurement) | Analytics | Week 2 — needed before launch to set baseline |
| OQ-5 | Does Beacon's existing Terms of Service need to be updated to reflect a grace period policy? | Legal | Week 2 — must resolve before launch |
| OQ-6 | Does Beacon's transactional email infrastructure have delivery monitoring and bounce handling? | RevOps | Week 2 |
| OQ-7 | Is there a maximum number of retries or a cap on retry window permitted by our payment processor agreement? | Finance / RevOps | Week 1 |

---

## 8. Rollout Plan

### Phase 0 — Confirm and instrument (Week 1, before any eng build)

- [ ] Confirm billing platform (OQ-1). If custom infra: **stop, re-score, escalate to PM.**
- [ ] Pull support ticket baseline for lockout/billing complaints (OQ-3)
- [ ] Begin churn cohort tagging by reason (involuntary vs. voluntary) — zero eng, analytics-led
- [ ] Identify billing contact data model (OQ-2)
- [ ] Legal review of ToS implications (OQ-5)

### Phase 1 — Build and internal test (Weeks 1–2)

- [ ] Configure dunning retry schedule in billing platform (M-1)
- [ ] Configure 7-day grace period / account access rules (M-3, M-4)
- [ ] Write and configure 3-email sequence (M-2, M-5) — requires copywriter or PM to draft
- [ ] Build audit log access for support team (M-6)
- [ ] QA: idempotency on retries, email delivery test, grace period enforcement, lockout screen copy
- [ ] Internal review: Finance sign-off on retry logic and audit trail; Legal sign-off on email content

### Phase 2 — Staged rollout (Week 3)

- [ ] Enable for new payment failures only (do not backfill existing failed accounts without legal/finance review)
- [ ] Monitor: email delivery rate, Day-3 recovery rate, support ticket volume
- [ ] Support team briefed on audit log; on-call eng assigned for first week of live traffic
- [ ] Alert thresholds set: if duplicate-charge event detected → auto-pause dunning and page on-call eng immediately

### Phase 3 — Full validation and iteration (Weeks 4–8)

- [ ] At Day 30: review recovery rate vs. 40% target; review support ticket delta
- [ ] At Day 60: review involuntary churn rate vs. baseline; report ARR recovered
- [ ] Decision: if recovery rate < 20% after 60 days, investigate email deliverability and billing-contact data quality before assuming the mechanism is wrong
- [ ] If S-1 (in-app banner) was deferred, evaluate whether data supports prioritizing it in the next sprint
- [ ] Feed results into Week 10 decision gate (per roadmap) alongside dunning data, A/B early signal, and top-50 survey

### Launch communications

- **Internal:** Support team briefed before launch (new audit log, new customer-facing flow)
- **External:** No proactive customer announcement needed; the feature is experienced only by customers who fail payment. Optionally add a brief ToS update note in next billing cycle communication if Legal requires it.

---

*An engineer and designer should be able to start from Phase 0 checklist items immediately. Phase 1 build does not begin until OQ-1 (billing platform) is confirmed.*

---
_Run metrics: 109.0s, 5506 in / 4695 out tokens, ~$0.0869_
