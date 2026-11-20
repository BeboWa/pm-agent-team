# BEACON-001: Dunning Automation + Grace Period — Execution Plan

> **Assumptions stated upfront:**
> - Team: 4 engineers (2 backend, 1 frontend, 1 fullstack/flex), 1 designer, 1 PM
> - Sprint capacity: 2-week sprints @ ~8 story points per engineer, ~6 points for designer per sprint (after ceremonies, reviews, unplanned work — roughly 70% utilization)
> - Total team capacity per sprint: ~32 eng points + ~6 design points
> - Story point estimates are rough (±50%); they assume billing platform = Stripe or Chargebee (the critical assumption from the PRD). **If custom infra is confirmed in Week 1, all estimates must be re-baselined.**
> - QA is shared across engineers (no dedicated QA role listed); QA tickets are assigned to the engineer who did not write the feature code.

---

## Backlog (Epics and Tickets)

### Epic 1: Foundation & Discovery (Phase 0 — pre-build gates)

| Ticket | Requirement | Description | Points | Owner |
|--------|------------|-------------|--------|-------|
| E1-T1 | OQ-1 | Confirm billing platform (Stripe / Chargebee / custom); document API surface for dunning config and retry hooks | 1 | Backend |
| E1-T2 | OQ-2 | Audit "billing contact" data model — distinct role vs. account owner, multi-contact support | 1 | Backend |
| E1-T3 | OQ-3 / Metrics | Pull support ticket baseline: volume attributed to lockout/billing failures | 1 | Support |
| E1-T4 | OQ-5 | Legal review: ToS implications of grace period policy | — | Legal (external) |
| E1-T5 | OQ-7 | Confirm max retry count and retry-window rules with payment processor agreement | — | Finance (external) |
| E1-T6 | OQ-6 | Confirm transactional ESP (SendGrid/Postmark/etc.), SPF/DKIM/DMARC status, bounce handling | 1 | Backend / RevOps |
| E1-T7 | §6 Metrics | Analytics: begin churn cohort tagging (involuntary vs. voluntary) — zero eng cost | — | Data |

> **Gate:** Phase 1 build does not start until E1-T1 (billing platform confirmed) is complete. All other Epic 1 items run in parallel during Week 1.

---

### Epic 2: Retry Schedule & Grace Period (Core billing logic)

| Ticket | Requirement | Description | Points | Owner |
|--------|------------|-------------|--------|-------|
| E2-T1 | M-1 | Configure automated retry schedule: Day 1, Day 3, Day 7 in billing platform | 2 | Backend |
| E2-T2 | M-3, M-4 | Enforce 7-day grace period: account stays fully accessible Day 0–7; lock only after all retries exhausted | 3 | Backend |
| E2-T3 | M-4 | Build/confirm lockout screen: clear messaging + "contact billing" CTA (not generic error) | 2 | Frontend |
| E2-T4 | Story 3 AC-4 | Validate idempotency keys on all retry calls; no double-charge scenario | 2 | Backend |
| E2-T5 | Story 3 | QA: retry schedule fires on correct days; successful mid-sequence retry halts subsequent retries; lockout triggers correctly on Day 7 exhaustion | 3 | QA (Backend) |

---

### Epic 3: Email Notification Sequence

| Ticket | Requirement | Description | Points | Owner |
|--------|------------|-------------|--------|-------|
| E3-T1 | M-2, M-5 | Write email copy: Day 0 (failure detected), Day 3 (second failure), Day 6 (final warning) — includes failure reason, suspension date, payment update link | 2 | Design / PM |
| E3-T2 | M-2, M-5 | Configure 3-email automated sequence in ESP, triggered by billing platform webhook events | 3 | Backend |
| E3-T3 | S-3 | Configure payment-confirmed email (recovery confirmation to billing contact) | 1 | Backend |
| E3-T4 | S-2 | Auto-resolve dunning sequence on successful payment: stop email sequence, no manual intervention needed | 2 | Backend |
| E3-T5 | Story 1 AC-1 | QA: Day 0 email fires within 15 min of failure event; Day 3 and Day 6 emails fire on schedule; sequence halts on recovery | 3 | QA (Backend) |
| E3-T6 | M-5 | Deliverability test: send test sequences through ESP, verify inbox placement (not spam), confirm DKIM/SPF pass | 2 | Backend / RevOps |

---

### Epic 4: Audit Log

| Ticket | Requirement | Description | Points | Owner |
|--------|------------|-------------|--------|-------|
| E4-T1 | M-6 | Backend: log all dunning events with timestamps (failure detected, retries, emails sent + delivery status, resolution/lockout) to immutable audit store | 3 | Backend |
| E4-T2 | M-6 | Support UI: expose audit log on account detail page (timestamped, read-only, filterable by event type) | 3 | Frontend |
| E4-T3 | Story 4 | QA: verify log immutability (no delete/edit), verify all event types are captured, verify delivery status is recorded | 2 | QA (Frontend) |

---

### Epic 5: In-App Banner & CS Notifications (Should-have)

| Ticket | Requirement | Description | Points | Owner |
|--------|------------|-------------|--------|-------|
| E5-T1 | S-1 | Design: in-app banner component for payment failure state (all pages, dismissible only on resolution) | 3 | Design |
| E5-T2 | S-1 | Frontend: implement in-app banner; show on all pages during grace period; auto-dismiss on payment recovery | 3 | Frontend |
| E5-T3 | S-4 | Backend: internal Slack/CRM notification when account enters dunning sequence (hook to existing notification system) | 2 | Backend |
| E5-T4 | S-1, S-2 | QA: banner appears on correct pages, dismisses on recovery, does not appear after lockout or successful payment | 2 | QA (Frontend) |

---

### Epic 6: Deferred / Icebox (Could-have — do not plan this quarter)

| Ticket | Requirement | Description | Notes |
|--------|------------|-------------|-------|
| E6-T1 | C-1 | Magic-link / token-auth payment update from email | Security/PCI review required; defer |
| E6-T2 | C-2 | Segment email copy by plan tier (Starter vs. Team) | Defer to post-launch iteration |
| E6-T3 | C-3 | Dunning-status filter field in admin dashboard | Defer; audit log covers support need for now |

---

## Dependencies and Critical Path

```
[E1-T1: Confirm billing platform] ──► EVERYTHING ELSE
         │
         ├──► [E2-T1: Retry config] ──► [E2-T2: Grace period] ──► [E2-T4: Idempotency] ──► [E2-T5: QA]
         │
         ├──► [E1-T2: Billing contact model] ──► [E3-T2: Email sequence config] ──► [E3-T5: QA]
         │                                              ▲
         │         [E3-T1: Email copy (PM/Design)] ─────┘
         │
         ├──► [E4-T1: Audit log backend] ──► [E4-T2: Support UI] ──► [E4-T3: QA]
         │
         └──► [E1-T6: ESP confirmed] ──► [E3-T6: Deliverability test] ──► LAUNCH GATE
```

**External dependencies (not controlled by eng team):**

| Dependency | Owner | Blocks | Risk if delayed |
|------------|-------|--------|----------------|
| Legal ToS review (E1-T4) | Legal | Launch gate | Cannot go live without sign-off |
| Finance: retry rules confirmation (E1-T5) | Finance | E2-T1 retry config | Wrong retry cadence shipped |
| Payment processor: idempotency key behavior | Finance / RevOps | E2-T4 | Duplicate charge exposure |
| ESP deliverability setup (SPF/DKIM/DMARC) | RevOps | E3-T6 | Emails land in spam; grace period invisible |
| Analytics: churn cohort tagging | Data | Baseline metrics only | No pre/post measurement |
| Support team briefing | CS Lead | Pre-launch | Support blind to new audit log |

**Critical path (longest dependency chain):**
> E1-T1 → E2-T1 → E2-T2 → E2-T4 → E2-T5 → Legal sign-off → Staged rollout

---

## Sprint Plan

> Assuming 2-week sprints. Sprint 1 begins Week 1. Team: 2 backend engineers, 1 frontend engineer, 1 fullstack engineer, 1 designer.
> Capacity per sprint: ~32 eng points + ~6 design points (at 70% utilization).

---

### Sprint 1 (Weeks 1–2): Foundation + Core Billing Logic

**Sprint goal:** Confirm all pre-build gates; have retry schedule, grace period, and audit log backend wired and testable internally.

| Ticket | Owner | Points |
|--------|-------|--------|
| E1-T1 Confirm billing platform | Backend | 1 |
| E1-T2 Billing contact data model | Backend | 1 |
| E1-T6 Confirm ESP + deliverability | Backend | 1 |
| E2-T1 Configure retry schedule | Backend | 2 |
| E2-T2 Grace period enforcement | Backend | 3 |
| E2-T4 Idempotency validation | Backend | 2 |
| E4-T1 Audit log backend | Backend | 3 |
| E3-T1 Email copy drafting | Design / PM | 2 |
| E5-T1 Banner component design | Design | 3 |
| E3-T2 Email sequence config (start) | Backend | 3 |
| E2-T3 Lockout screen | Frontend | 2 |

**Sprint 1 eng total: ~20 points** (conservative given discovery work and external gates consuming time)
**Design total: ~5 points**

**Exit criteria:** Billing platform confirmed; retry + grace period logic deployed to staging; audit log writing events; email copy drafted and in legal review.

---

### Sprint 2 (Weeks 3–4): Email Sequence, In-App Banner, QA, Staged Rollout

**Sprint goal:** Complete email sequence, in-app banner, full QA pass, support team briefed, staged rollout live for new failures.

| Ticket | Owner | Points |
|--------|-------|--------|
| E3-T2 Email sequence config (complete) | Backend | — (carry from S1) |
| E3-T3 Payment-confirmed email | Backend | 1 |
| E3-T4 Auto-resolve on payment | Backend | 2 |
| E3-T6 Deliverability test | Backend | 2 |
| E4-T2 Audit log support UI | Frontend | 3 |
| E5-T2 In-app banner frontend | Frontend | 3 |
| E5-T3 CS Slack/CRM notification | Backend (flex) | 2 |
| E2-T5 QA: retry schedule | QA (Backend) | 3 |
| E3-T5 QA: email sequence | QA (Backend) | 3 |
| E4-T3 QA: audit log | QA (Frontend) | 2 |
| E5-T4 QA: banner | QA (Frontend) | 2 |
| Support team briefing | PM / CS Lead | — |

**Sprint 2 eng total: ~25 points**

**Exit criteria:** All Must + Should requirements QA-passed on staging; deliverability test passed; legal/finance sign-offs received; support team briefed; staged rollout enabled for new payment failures only.

---

### Post-Sprint 2: Validation (Weeks 5–8, no new build)

- Week 5: Monitor email delivery rate, Day-3 recovery rate, duplicate-charge alerts
- Day 30: Review recovery rate vs. 40% target; support ticket delta
- Day 60: Involuntary churn rate vs. baseline; ARR recovered report
- Decision gate: if recovery < 20% → investigate deliverability + billing contact data quality before assuming product fix needed
- Backlog grooming: evaluate C-1 (magic link), C-2 (tier segmentation) based on data

---

## Risks and Mitigations

| # | Risk | Likelihood | Severity | Early Warning Sign | Mitigation |
|---|------|-----------|----------|--------------------|------------|
| R-1 | **Custom billing infrastructure confirmed** (not Stripe/Chargebee) | Unknown | 🔴 High — effort triples; timeline shifts to Next quarter | E1-T1 returns anything other than a known SaaS billing platform | **Hard stop at end of Week 1.** If custom infra confirmed: re-score effort to 2–3 person-months, escalate to PM, do not begin E2 work. |
| R-2 | **Warning emails land in spam** | Medium | 🔴 High — grace period is invisible; recovery rate near zero | Email open rate < 25% in first week of staged rollout | Confirm SPF/DKIM/DMARC before launch (E1-T6, E3-T6). Use reputable ESP. Set open-rate monitoring alert. |
| R-3 | **Stale/wrong billing contact email** | Medium | 🟡 Medium — email delivered but to wrong person | High delivery rate but low open rate; support tickets still reference "no warning received" | Implement in-app banner (S-1) as independent redundant channel. Alert account admin separately if different from billing contact. |
| R-4 | **Retry logic triggers duplicate charge** | Low | 🔴 High — customer and legal/finance impact; potential chargeback wave | Any duplicate-charge event in staging QA or production monitoring | Idempotency key validation required before ship (E2-T4). QA test case required. Auto-pause dunning + page on-call eng if duplicate detected in production. |
| R-5 | **Legal/Finance sign-off delayed past Sprint 2** | Medium | 🟡 Medium — blocks launch gate | No response by Day 7 of Sprint 1 | PM escalates to legal/finance leads by Day 3 of Sprint 1. Identify named approvers and SLA upfront. ToS changes are low-complexity; flag as such in the ask. |
| R-6 | **Billing contact data model is more complex than expected** (OQ-2) | Medium | 🟡 Medium — email targeting logic must be re-architected | E1-T2 reveals no distinct billing contact role in data model | Identify in Week 1. Fallback: email account owner role. Add follow-on ticket to collect billing contact separately if needed. |

---

## Stakeholder Status Update (Draft)

> **For:** Executive stakeholders
> **Re:** BEACON-001 Dunning Automation — Status as of Sprint 1 kickoff

---

**What we're doing:** Turning on automated payment retry + a 7-day grace period to stop involuntary churn. Currently, customers who miss a payment are locked out immediately with no warning — costing ~$456K ARR/year. Industry tools recover 40–70% of these accounts; we're targeting ≥40%.

**Timeline:** 2 sprints (4 weeks) to staged rollout, assuming Beacon runs on Stripe or Chargebee. **Week 1 priority: confirm billing platform.** If we're on custom infra, timeline moves to next quarter and we'll escalate immediately.

**Biggest risk:** Email deliverability and stale billing contact data. We have mitigations in plan (deliverability testing, in-app banner as backup channel).

**External dependencies to unblock now:** Legal (ToS review — low complexity, need named owner + 1-week SLA) and Finance (retry rules sign-off). PM will ping both this week.

**What "done" looks like at Day 60:** Recovery rate ≥40% of accounts entering dunning, ≥$90K ARR recovered, billing support tickets down ≥50%.

---
_Run metrics: 86.4s, 5119 in / 4216 out tokens, ~$0.0786_
