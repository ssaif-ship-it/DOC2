This guide outlines the rules, workflows, regulatory timelines, and reconciliation mechanics for returning customer funds—either via merchant-initiated Refunds or system-triggered Reversals.

### 1. Key Concepts & Definitions

It is essential to distinguish between refunds, reversals, and chargebacks to manage cash flow and support operations effectively.

<div style="overflow-x: auto; margin: 20px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #eae5f2; border-radius: 12px; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #334155;">
    <thead>
      <tr style="background-color: #f6f1fc;">
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Term</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Triggered By</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Timing &amp; Scope</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Operational Focus</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Refund</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Merchant (Dashboard or API)</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Post-capture (Up to 180 days from transaction date).</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Used for order cancellations, product returns, goodwill credits, or SLA breaches.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Reversal</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #f0eafc; color: #5b21b6; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">System / Network (NPCI or Bank)</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Pre-settlement / Immediate post-debit.</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">"Undoes" failed/stuck debits, authorization timeouts, or unlinked VPA transfers.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; vertical-align: top;">Chargeback</td>
        <td style="padding: 16px 20px; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef2f2; color: #dc2626; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Issuing Bank / NPCI (Customer Dispute)</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Post-settlement (30 to 90+ days post-purchase).</td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Customer-initiated legal dispute; carries administrative fees and risk exposure.</td>
      </tr>
    </tbody>
  </table>
</div>


**Core Rules for Refund Eligibility**
*   **Transaction Status:** Only payments in `SUCCESS` / `Captured` state can be refunded. Pending, failed, or already reversed transactions cannot be refunded.
*   **Time Window:** Standard refunds are allowed up to 180 days from the transaction date. Complaint-driven UPI UDIR refunds are supported up to 90 days.
*   **Refundable Balance:** Any new refund must satisfy:

> **Refund Amount** ≤ **Captured Amount** - **∑ (Previous Partial Refunds)**### 2. Payment Method Differences & Regulatory SLAs

Refund processing speeds and technical capabilities vary significantly depending on the payment rail used.

<div style="overflow-x: auto; margin: 20px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #eae5f2; border-radius: 12px; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #334155;">
    <thead>
      <tr style="background-color: #f6f1fc;">
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Payment Method</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Mechanism</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Typical Credit Window</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Regulatory TAT &amp; Compliance</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">UPI</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Real-time API / Auto-Reversal / UDIR</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Instant to T+1 Business Day</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">RBI mandates failed debit reversals within T+5 calendar days. Delay penalty: ₹100/day charged to acquiring bank/merchant.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Credit/Debit Cards</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">ISO 8583 0400 Reversals / Scheme Refunds</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">5–7 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Scheme rules (Visa/Mastercard/RuPay) set an outer limit of 7–10 days.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Net Banking</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Bank Claim Files / MIS Adjustments</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #f0eafc; color: #5b21b6; border: 1px solid #ddd6fe; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">3–5 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Non-automated; relies on bank-side periodic claim file processing.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Prepaid Wallets (PPI)</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Sponsor Bank API</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Instant to T+1 Business Day</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Governed by NPCI/RBI PPI-on-UPI operating guidelines.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; vertical-align: top;">EMI / BNPL</td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Issuer Credit Line Adjustment</td>
        <td style="padding: 16px 20px; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">5–7 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Refund cancels principal; customer must contact issuer to cancel bank EMI interest schedules.</td>
      </tr>
    </tbody>
  </table>
</div>
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