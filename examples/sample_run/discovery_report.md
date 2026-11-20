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
