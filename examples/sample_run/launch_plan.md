# Launch Package: BEACON-001 — Dunning Automation + Grace Period

---

## Positioning

### What It Is
Automated payment recovery with a 7-day grace period: when a payment fails, Beacon now retries automatically, warns the billing contact immediately, and keeps the account fully accessible for 7 days while the issue is resolved.

### Why It Matters (Internal Frame)
This is Beacon's highest-certainty revenue action. An estimated $456K ARR is leaking annually from payment failures that result in immediate, silent lockouts — not from customer dissatisfaction. Industry dunning recovery rates run 40–70%; even at a conservative 20%, this effort recovers ~$90K ARR in the first two quarters. It is a configuration change on existing billing infrastructure costing ~0.5 person-months.

### Launch Tier Recommendation: **Announced Feature — Internal + Billing-Adjacent**

**Justification:**
- No proactive all-customer announcement needed; the feature only activates for customers who experience a payment failure.
- Requires mandatory internal briefing (support team, CS, RevOps) before go-live.
- Requires legal/finance sign-off on ToS and retry logic before launch.
- A brief ToS or billing-policy notice should be included in the next billing cycle communication if Legal requires it (flag below).
- This is not a quiet rollout — support must be fully prepared before the first dunning email goes out.

---

## Messaging by Audience

### Customers (Billing Contacts) — DRAFT

> **Subject: Payment issue on your Beacon account — here's what to do**
>
> Hi [Name],
>
> We weren't able to process your Beacon subscription payment on [DATE]. Don't worry — your account and all your team's work remain fully accessible for the next 7 days.
>
> **What's happening:** [Failure reason from payment processor, e.g., "Your card was declined."]
>
> **What to do:** Update your payment method here → [LINK]
>
> **Important dates:**
> - We'll retry your payment automatically on Day 1, Day 3, and Day 7.
> - If the issue isn't resolved by [DATE + 7 days], your account will be suspended.
>
> Questions? Reply to this email or visit [support link].
>
> — The Beacon Team

*(Follow-up emails send on Day 3 and Day 6 with updated countdown. Confirmation email sends on successful recovery.)*

---

### Customers — Lockout Screen (Post Grace Period) — DRAFT

> **Your Beacon account has been suspended due to a billing issue.**
>
> To restore access, please update your payment method: [LINK]
>
> Need help? Contact us at [billing support email].

*(Not a generic error page — must include specific instructions per M-4.)*

---

### Customers — In-App Banner (During Grace Period, S-1) — DRAFT

> ⚠️ **Action needed:** We couldn't process your payment. Your account is accessible until [DATE]. [Update payment method →]

---

### Customers — Successful Recovery Confirmation — DRAFT

> **Subject: Payment confirmed — you're all set**
>
> Hi [Name],
>
> Your Beacon payment was successfully processed. Your account is fully active and no further action is needed.
>
> — The Beacon Team

---

### Sales Team

**What changed:** Beacon now gives customers a 7-day grace period and three automated payment retry attempts before any lockout occurs. This is a retention improvement, not a pricing or plan change.

**Key objection handlers:**

| Objection | Response |
|---|---|
| "Will customers abuse the grace period to use Beacon for free?" | The grace period is 7 days — industry standard. Retries run on Days 1, 3, and 7. Accounts that don't resolve payment are locked at Day 7. This is not a free extension of service. |
| "What if a prospect asks about billing reliability?" | Beacon now has automated dunning with a 7-day grace period, three retry attempts, proactive email warnings, and full audit logging. This is best-practice billing infrastructure. |
| "Does this change pricing or contract terms?" | No. This feature does not change plan pricing, proration, or contract terms. [Flag: Legal review of ToS is in progress — confirm before making any ToS-related statements to customers.] |

---

### Customer Support Team

**What changed and what you need to know:**

1. **Customer experience:** Customers with a failed payment now receive up to three warning emails (Day 0, Day 3, Day 6) and retain full access for 7 days. Lockout only occurs if all retries fail and the customer does not update their payment method by Day 7.

2. **Audit log:** Every dunning event is logged with timestamps — failure detected, retries attempted, emails sent (with delivery status), and resolution or lockout. Access the log at [LOCATION — to be confirmed before launch]. Use this to respond to "I never got a warning" claims.

3. **How to handle common tickets:**

| Customer says | What to do |
|---|---|
| "I was locked out without warning" | Pull audit log. Confirm email send/delivery timestamps. If email was sent and delivered, share the timeline. If email bounced, escalate to RevOps to verify billing contact email on file. |
| "I updated my payment but I'm still locked out" | Check audit log for payment confirmation event. If payment confirmed but access not restored, escalate to engineering (auto-resolve per S-2 should trigger immediately). |
| "I'm seeing a banner but I didn't fail payment" | Escalate to engineering — banner should only display during active dunning sequence. |
| "I want my account back after Day 7 lockout" | Confirm payment method is updated and charge succeeds. Manual reactivation process: [TO BE DOCUMENTED BY REVOPS BEFORE LAUNCH]. |

4. **What hasn't changed:** Voluntary cancellations, enterprise billing, and pricing are not affected by this feature.

5. **Training required:** Complete the support team briefing before go-live. Do not go live until this briefing is confirmed.

---

### Executive / Finance Audience

**Business case summary:**

- **Problem:** 40% of Beacon's churned logos (~40 customers/quarter) are lost to payment failure, not dissatisfaction. This represents $456K ARR at risk annually — a pure billing ops failure, not a product or market problem.
- **Solution cost:** ~0.5 person-months (assumes Stripe/Chargebee — must be verified Week 1).
- **Projected return:** Industry recovery rates are 40–70%. At a conservative 20%, projected ARR recovery is ~$90K in the first two quarters. At 40% (conservative floor of industry benchmark), recovery reaches ~$180K.
- **Supporting metrics:** Reduction in billing-related support tickets (target: ≥50% within 30 days) and payment failure recovery rate (target: ≥40% of accounts entering dunning sequence recovering within 7 days).
- **Strategic fit:** This is Bet 1 of the "Stop the Bleed" strategy. It is the fastest, lowest-risk, highest-confidence action on the roadmap. NRR of 80% means every recovered customer has compounding retention value.
- **Key dependency:** Effort estimate assumes Beacon runs on Stripe Billing, Chargebee, or equivalent. If custom billing infrastructure is confirmed, effort triples and timeline shifts. **Verify billing platform in Week 1 before committing budget or timeline.**

---

## Release Notes (Draft)

> **DRAFT — Requires legal and product review before publication**

### Billing: Automated Payment Recovery + 7-Day Grace Period

**What's new**

If a payment fails on your Beacon account, you'll now receive an immediate email notification with the reason for the failure and a direct link to update your payment method. Your account remains fully accessible for 7 days while you resolve the issue.

**How it works**

- **Day 0:** Payment fails. You receive an email with failure details and a link to update your payment method.
- **Day 1, Day 3, Day 7:** Beacon automatically retries the payment.
- **Day 3 and Day 6:** If the issue is unresolved, you receive follow-up reminder emails.
- **If resolved:** Your account continues uninterrupted. You'll receive a payment confirmation email.
- **If unresolved after 7 days:** Your account is suspended until payment is updated. You'll see clear instructions on the suspension screen.

**Who is affected**

Starter and Team tier customers. This feature activates only when a payment failure occurs.

**Nothing changes if your payment succeeds.** This feature runs silently in the background.

*Available: [DATE]*

---

## Launch Plan and Checklist

### Phase 0 — Confirm and Instrument (Week 1) — **BLOCKS ALL BUILD WORK**

| # | Action | Owner | Blocking? |
|---|---|---|---|
| 0-1 | **Confirm billing platform (Stripe, Chargebee, or custom)** | Engineering Lead | ✅ Yes — if custom infra, stop and re-score |
| 0-2 | Identify billing contact data model (distinct role vs. account owner; multiple contacts?) | Engineering + PM | ✅ Yes — affects email targeting |
| 0-3 | Pull support ticket baseline for lockout/billing complaints | Support Lead | No — but needed for metric baseline |
| 0-4 | Begin churn cohort tagging: involuntary vs. voluntary | Analytics | No — run in parallel |
| 0-5 | Confirm payment method update page exists and link is functional | Engineering | ✅ Yes — required for email copy |
| 0-6 | Confirm payment processor agreement permits 3-retry schedule and 7-day window (OQ-7) | Finance / RevOps | ✅ Yes |
| 0-7 | Legal review: ToS update required for grace period policy? (OQ-5) | Legal | ✅ Yes — must resolve before launch |
| 0-8 | Confirm transactional email infrastructure (ESP, SPF/DKIM/DMARC, delivery monitoring) | RevOps | ✅ Yes |

---

### Phase 1 — Build and Internal Test (Weeks 1–2)

| # | Action | Owner | Notes |
|---|---|---|---|
| 1-1 | Configure dunning retry schedule: Day 1, Day 3, Day 7 (M-1) | Engineering | Requires 0-1 confirmed |
| 1-2 | Configure 7-day grace period / account access rules (M-3, M-4) | Engineering | |
| 1-3 | Write 3-email sequence + confirmation email (M-2, M-5) | PM / Copywriter | See DRAFT above; legal review required |
| 1-4 | Configure email sequence in ESP | RevOps | Requires 1-3 complete |
| 1-5 | Build audit log access for support team (M-6) | Engineering | |
| 1-6 | Build in-app banner (S-1) | Engineering | High value — include if timeline holds |
| 1-7 | Configure auto-resolve on payment success (S-2) | Engineering | |
| 1-8 | Configure CS/account owner Slack or CRM notification on dunning entry (S-4) | RevOps | |
| 1-9 | Confirmation email on recovery (S-3) | RevOps | |
| **QA** | Idempotency validation on retries (no double-charge) | Engineering | ⚠️ P0 — must pass before any go-live |
| **QA** | Email delivery end-to-end test | RevOps | |
| **QA** | Grace period enforcement test (access remains through Day 7) | Engineering | |
| **QA** | Lockout screen copy test (must not be generic error) | Engineering + PM | |
| **QA** | Auto-resolve triggers correctly on payment success | Engineering | |
| **Sign-off** | Finance: retry logic and audit trail review | Finance | Required before launch |
| **Sign-off** | Legal: email content and ToS review | Legal | Required before launch |

---

### Phase 2 — Staged Rollout (Week 3)

| # | Action | Owner | Notes |
|---|---|---|---|
| 2-1 | Support team briefing: audit log, new customer-facing flow, ticket handling guide | Support Lead | **Must complete before go-live** |
| 2-2 | CS team briefing: dunning notification flow, proactive outreach process for high-value accounts | CS Lead | |
| 2-3 | Enable for **new payment failures only** — do not backfill existing failed accounts | Engineering | ⚠️ Legal/finance must review before any backfill decision |
| 2-4 | Set alert threshold: duplicate-charge event → auto-pause dunning + page on-call engineering immediately | Engineering | ⚠️ P0 — must be active on go-live day |
| 2-5 | Monitor: email delivery rate, Day-3 recovery rate, support ticket volume | RevOps + Analytics | Daily for first week |
| 2-6 | On-call engineering assigned for first week of live traffic | Engineering Lead | |
| 2-7 | If ToS update required: include notice in next billing cycle communication | Legal + Marketing | Coordinate timing |

---

### Phase 3 — Validation and Iteration (Weeks 4–8)

| # | Checkpoint | Metric | Action if Below Target |
|---|---|---|---|
| Day 30 | Billing support ticket volume | Target: ≥50% reduction in lockout-related tickets | Investigate audit log usage; re-brief support team |
| Day 30 | Email open rate | Flag if <25% (deliverability issue) | Investigate ESP deliverability, SPF/DKIM, billing contact email quality |
| Day 60 | Payment failure recovery rate | Target: ≥40% of dunning accounts recover | Investigate email deliverability and billing contact data quality before assuming mechanism is wrong |
| Day 60 | Involuntary churn rate | Target: ≥40% reduction in logos lost to payment failure | Cross-check against churn cohort tagging |
| Day 60 | ARR recovered | Target: ≥$90K on track (2-quarter projection) | Report to executive team with recovery rate data |
| Day 60 | In-app banner (S-1) | Was it deferred? | Evaluate data — if recovery rate is below target, prioritize in next sprint |

---

## Sales and Support Enablement

### Billing, Pricing, and Payment Change Protocols

> ⚠️ **This section requires Legal and Finance review before finalization.**

| Item | Detail | Status |
|---|---|---|
| **Customer notice period** | No proactive announcement needed for customers not in a dunning sequence. Customers entering dunning are notified at moment of failure (Day 0 email). | Confirm with Legal |
| **ToS / billing agreement update** | Legal must confirm whether the 7-day grace period creates a contractual service obligation. If yes, update ToS before launch and include a brief notice in the next billing cycle communication. | ⚠️ Open — OQ-5 |
| **Grandfathering / migration** | No plan changes, pricing changes, or proration changes. No grandfathering decisions required. | N/A |
| **Invoice and receipt changes** | No changes to invoice format or receipt content from this feature. Failed payment attempts and successful recovery will be logged in the audit trail (internal). Confirm with Finance whether retry attempt records should appear on customer-facing receipts. | ⚠️ Flag for Finance |
| **Support readiness** | Support team must complete briefing and have audit log access confirmed before go-live. Manual reactivation process (post-Day-7 lockout) must be documented by RevOps before launch. | ⚠️ Required pre-launch |
| **Duplicate charge protection** | Idempotency keys on retry calls must be validated in QA before launch. Any duplicate-charge event post-launch triggers auto-pause of dunning and immediate engineering escalation. | ⚠️ P0 QA item |
| **PCI-DSS scope (C-1, if built)** | Magic-link payment update flow requires short-lived single-use tokens. Card data must not pass through Beacon's servers. HTTPS required. Confirm PCI scope with Security before building. | ⚠️ Flag for Security — C-1 only |

---

### Support Quick-Reference Card

**Feature name:** Dunning Automation + Grace Period (BEACON-001)
**Live date:** [DATE]
**Who is affected:** Starter and Team tier customers with payment failures

| Scenario | What the customer sees | What support does |
|---|---|---|
| Payment fails, within grace period | Warning email + in-app banner (if S-1 shipped) | Pull audit log; confirm email sent; share resolution link |
| Customer claims no warning received | — | Pull audit log; check email delivery status; if bounced, check billing contact email on file; escalate to RevOps if stale |
| Customer updated payment, still seeing banner | Banner should auto-dismiss | Check audit log for payment confirmation; if confirmed but banner persists, escalate to engineering |
| Account locked after Day 7 | Lockout screen with instructions | Confirm payment method updated; confirm charge succeeded; follow manual reactivation process [LINK — to be created by RevOps] |
| Suspected duplicate charge | — | **Escalate immediately to engineering.** Do not attempt manual resolution. |

**Audit log location:** [TO BE CONFIRMED BEFORE LAUNCH]
**Escalation path for billing errors:** [TO BE CONFIRMED BEFORE LAUNCH]

---

## Launch Risks

| Risk | Likelihood | Severity | Mitigation | Owner |
|---|---|---|---|---|
| **Custom billing infrastructure confirmed** (not Stripe/Chargebee) | Unknown | 🔴 Critical — effort triples, timeline shifts to Next phase | Verify billing platform in Week 1 before any design or engineering work begins. If confirmed, stop, re-score, and escalate to PM and leadership. | Engineering Lead — Week 1 |
| **Dunning emails land in spam** | Medium | 🔴 High — grace period is invisible to customer; recovery rate collapses | Confirm ESP with SPF/DKIM/DMARC configured. Test deliverability before launch. Monitor open rate post-launch; flag if <25%. | RevOps |
| **Billing contact email on file is stale or wrong** | Medium | 🟡 Medium — email sent but not received by decision-maker | In-app banner (S-1) provides redundant channel. Consider notifying account admin separately if different from billing contact. Add to QA checklist. | Engineering + RevOps |
| **Retry logic triggers duplicate charge** | Low | 🔴 Critical — customer and legal/financial impact | Validate idempotency keys on all retry calls in QA before launch. Set auto-pause alert for any duplicate-charge event post-launch. | Engineering |
| **ToS or billing agreement not updated before launch** | Medium | 🟡 Medium — legal and customer trust exposure | Legal review is a hard gate. Do not launch until OQ-5 is resolved and any required ToS update is live or in next billing cycle notice. | Legal |
| **Support team not briefed before go-live** | Low (preventable) | 🟡 Medium — first dunning emails create confused inbound tickets | Support briefing is a hard pre-launch gate. Audit log access must be confirmed and manual reactivation process documented. | Support Lead |
| **Grace period creates bad debt exposure on high-value accounts** | Low | 🟡 Low for most accounts | Finance should set a monitoring threshold (e.g., flag any account with >$5K MRR entering dunning) and confirm whether manual intervention is needed for those accounts. | Finance |
| **Churn cohort baseline not established before launch** | Medium | 🟡 Medium — post-launch measurement is unreliable | Begin churn cohort tagging (involuntary vs. voluntary) in Week 1 in parallel. Zero engineering cost. Without a baseline, the 60-day success metrics cannot be evaluated. | Analytics |
| **Payment method update page is broken or link is wrong** | Low (preventable) | 🟡 Medium — customer cannot self-resolve; support volume spikes | Confirm link destination and test end-to-end before email copy is finalized. Include in QA checklist. | Engineering |

---

> **All customer-facing copy in this document is marked DRAFT and must be reviewed by a human editor and legal counsel before use.**
>
> **Legal and Finance review gates identified above are hard stops — do not proceed to staged rollout without sign-off on (1) ToS implications, (2) retry logic audit trail, and (3) email content approval.**

---
_Run metrics: 116.0s, 9823 in / 5007 out tokens, ~$0.1046_
