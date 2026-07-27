This guide outlines the rules, workflows, regulatory timelines, and reconciliation mechanics for returning customer funds—either via merchant-initiated Refunds or system-triggered Reversals.

### 1. Key Concepts & Definitions

It is essential to distinguish between refunds, reversals, and chargebacks to manage cash flow and support operations effectively.

| Term | Triggered By | Timing & Scope | Operational Focus |
| :--- | :--- | :--- | :--- |
| **Refund** | Merchant (Dashboard or API) | Post-capture (Up to 180 days from transaction date). | Used for order cancellations, product returns, goodwill credits, or SLA breaches. |
| **Reversal** | System / Network (NPCI or Bank) | Pre-settlement / Immediate post-debit. | "Undoes" failed/stuck debits, authorization timeouts, or unlinked VPA transfers. |
| **Chargeback** | Issuing Bank / NPCI (Customer Dispute) | Post-settlement (30 to 90+ days post-purchase). | Customer-initiated legal dispute; carries administrative fees and risk exposure. |

**Core Rules for Refund Eligibility**
*   **Transaction Status:** Only payments in `SUCCESS` / `Captured` state can be refunded. Pending, failed, or already reversed transactions cannot be refunded.
*   **Time Window:** Standard refunds are allowed up to 180 days from the transaction date. Complaint-driven UPI UDIR refunds are supported up to 90 days.
*   **Refundable Balance:** Any new refund must satisfy:

$$\text{Refund Amount} \le \text{Captured Amount} - \sum \text{Previous Partial Refunds}$$

### 2. Payment Method Differences & Regulatory SLAs

Refund processing speeds and technical capabilities vary significantly depending on the payment rail used.

| Payment Method | Mechanism | Typical Credit Window | Regulatory TAT & Compliance |
| :--- | :--- | :--- | :--- |
| **UPI** | Real-time API / Auto-Reversal / UDIR | Instant to T+1 Business Day | RBI mandates failed debit reversals within T+5 calendar days. Delay penalty: ₹100/day charged to acquiring bank/merchant. |
| **Credit/Debit Cards** | ISO 8583 0400 Reversals / Scheme Refunds | 5–7 Business Days | Scheme rules (Visa/Mastercard/RuPay) set an outer limit of 7–10 days. |
| **Net Banking** | Bank Claim Files / MIS Adjustments | 3–5 Business Days | Non-automated; relies on bank-side periodic claim file processing. |
| **Prepaid Wallets (PPI)** | Sponsor Bank API | Instant to T+1 Business Day | Governed by NPCI/RBI PPI-on-UPI operating guidelines. |
| **EMI / BNPL** | Issuer Credit Line Adjustment | 5–7 Business Days | Refund cancels principal; customer must contact issuer to cancel bank EMI interest schedules. |

### 3. Refunds vs. Reversals

#### 3.1 Merchant-Initiated Refunds (Full vs. Partial)
*   **Full Refund:** Refunds 100% of the captured transaction amount.
*   **Partial Refund:** Refunds a portion of the original sale. Multiple partial refunds are permitted until the total captured balance reaches zero.
*   **Multi-Payment Orders:** On orders paid via multiple transactions, refunds must be executed at the transaction level (`payment_id`) rather than the order level to ensure clear ledger allocation.

#### 3.2 System-Driven Auto-Reversals
Reversals occur automatically when funds leave the customer's account but cannot be fulfilled:
*   **UPI Timeouts ("Deemed Success"):** Debited funds that fail terminal confirmation are auto-reversed back to the remitter bank via NPCI switch signals.
*   **Direct VPA Transfers:** Payments sent directly to a merchant VPA without a valid checkout session/Order ID are tagged as `UNRECONCILED_AUTO_REFUND` and auto-reversed.
*   **Card Auth Timeouts:** Authorization holds that drop before capture are released via ISO 8583 0400 messages.
*   **Direct Settlement Exception:** If you operate on a Direct Settlement model (where acquirers credit your bank account directly), standard Payment Gateway refund APIs are blocked. Refunds must be executed as explicit outbound Payout transfers from your current account or refund wallet.

### 4. Refund Status Lifecycle

Gateways track refunds across a defined lifecycle. You can monitor these statuses via Dashboard or Webhooks:

```text
[INITIATED] ---> [IN_PROGRESS / PENDING] ---> [SUCCESS / REFUNDED]
                       |
                       +---> [ON_HOLD]  (Low merchant balance / verification pending)
                       +---> [MANUAL]   (Exhausted auto-retries; escalated to ops)
                       +---> [FAILED / CANCELLED]