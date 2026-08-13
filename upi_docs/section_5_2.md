This guide outlines the rules, workflows, regulatory timelines, and reconciliation mechanics for returning customer funds, either via merchant-initiated Refunds or system-triggered Reversals.

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

<!-- Claude, flagging for Saif, not confirmed: couldn't trace either figure to a citable source. No RBI or NPCI document sets a single 180-day refund-initiation deadline that I could find, Razorpay/PayU/Cashfree's own public docs only state refund processing time, not an initiation window, so 180 days may be specific to Cashfree's own policy rather than an industry standard, worth confirming with whoever owns this rule. Same for the 90-day UDIR figure: NPCI's UDIR framework sets TATs for resolution speed (e.g. 3 days for P2M auto-chargeback conversion), not a single codified filing deadline, the actual in-app dispute window varies by bank/app (commonly 30 to 90 days). Left both numbers as-is and posted a comment on this line, since I don't have a confirmed replacement for either. -->
*   **Refundable Balance:** Any new refund must satisfy:

> **Refund Amount** must be less than or equal to **Captured Amount** minus the **total of all previous partial refunds**.

### 2. Payment Method Differences & Regulatory SLAs

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
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">For merchant (P2M) UPI payments specifically, RBI mandates failed debit reversals within T+5 calendar days. Delay penalty: ₹100/day charged to acquiring bank/merchant. (A separate RBI line item sets P2P transfers at T+1, not T+5, don't reuse this figure outside a merchant-payment context.)</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Credit/Debit Cards</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">ISO 8583 0400 Reversals / Scheme Refunds</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">5 to 7 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Treat 7 to 10 days as a safe outer bound; some networks apply slower rails further out.</td>
      </tr>
      <!-- Claude, flagging for Saif, not confirmed: softened this cell. Couldn't find a published Visa, Mastercard, or RuPay/NPCI document that states a specific "7 to 10 day outer limit" as scheme policy, that read as paraphrase presented as a citation. The 5 to 7 business day figure in the pill above is broadly consistent with what other Indian gateways publish, so left that alone. Posted a comment on this row too. -->
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Net Banking</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Bank Claim Files / MIS Adjustments</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #f0eafc; color: #5b21b6; border: 1px solid #ddd6fe; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">3 to 5 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Non-automated; relies on bank-side periodic claim file processing.</td>
      </tr>
      <!-- Claude, flagging for Saif, not confirmed: the Net Banking (3 to 5 days) and EMI/BNPL (5 to 7 days) credit windows below have no independent public source either way, they read as operational/gateway-observed figures rather than a codified rule. Plausible, but only your own ops or settlements team can confirm they're current. Posted a comment on this row too. -->
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
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">5 to 7 Business Days</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Refund cancels principal; customer must contact issuer to cancel bank EMI interest schedules.</td>
      </tr>
    </tbody>
  </table>
</div>

## 3. Refunds vs. Reversals

### 3.1 Merchant-Initiated Refunds (Full vs. Partial)

*   **Full Refund:** Refunds 100% of the captured transaction amount.
*   **Partial Refund:** Refunds a portion of the original sale. Multiple partial refunds are permitted until the total captured balance reaches zero.
*   **Multi-Payment Orders:** On orders paid via multiple transactions, refunds must be executed at the transaction level (`payment_id`) rather than the order level to ensure clear ledger allocation.

### 3.2 System-Driven Auto-Reversals

Reversals occur automatically when funds leave the customer's account but cannot be fulfilled:

*   **UPI Timeouts ("Deemed Success"):** Debited funds that fail terminal confirmation are auto-reversed back to the remitter bank via NPCI switch signals.
*   **Direct VPA Transfers:** Payments sent directly to a merchant VPA without a valid checkout session/Order ID are tagged as `UNRECONCILED_AUTO_REFUND` and auto-reversed.
*   **Card Auth Timeouts:** Authorization holds that drop before capture are released via ISO 8583 0400 messages.
*   **Direct Settlement Exception:** If you operate on a Direct Settlement model (where acquirers credit your bank account directly), standard Payment Gateway refund APIs are blocked. Refunds must be executed as explicit outbound Payout transfers from your current account or refund wallet.

## 4. Refund Status Lifecycle

Gateways track refunds across a defined lifecycle. You can monitor these statuses via Dashboard or Webhooks:

<div class="cf-rf-wrap">
  <style>
    .cf-rf-wrap { margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .cf-rf-main { display: flex; align-items: stretch; flex-wrap: nowrap; gap: 6px; }
    .cf-rf-node {
      flex: 1 1 0;
      min-width: 0;
      border-radius: 8px;
      padding: 10px 10px;
      text-align: center;
    }
    .cf-rf-main .cf-rf-node { display: flex; align-items: center; justify-content: center; font-size: 12.5px; font-weight: 600; }
    .cf-rf-blue { background: #eff6ff; border: 1px solid #bfdbfe; color: #2563eb; }
    .cf-rf-green { background: #ecfdf5; border: 1px solid #a7f3d0; color: #059669; }
    .cf-rf-amber { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }
    .cf-rf-red { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; }
    .cf-rf-arrow {
      flex: 0 0 auto; display: flex; align-items: center; justify-content: center;
      color: #94a3b8; font-size: 16px; font-weight: 700; min-width: 12px;
    }
    .cf-rf-connector { display: flex; justify-content: center; margin: 6px 0; color: #94a3b8; font-size: 16px; }
    .cf-rf-branch-label {
      text-align: center; font-size: 11px; font-weight: 700; color: #94a3b8;
      text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 8px;
    }
    .cf-rf-branches { display: flex; flex-wrap: wrap; gap: 8px; }
    .cf-rf-branches .cf-rf-node { flex: 1 1 150px; }
    .cf-rf-title { font-size: 12.5px; font-weight: 700; }
    .cf-rf-caption { margin-top: 4px; font-size: 11px; font-weight: 500; opacity: 0.85; line-height: 1.4; }
    @media (max-width: 640px) {
      .cf-rf-main { flex-direction: column; }
      .cf-rf-main .cf-rf-arrow { transform: rotate(90deg); padding: 1px 0; }
      .cf-rf-branches { flex-direction: column; }
    }
  </style>
  <div class="cf-rf-main">
    <div class="cf-rf-node cf-rf-blue">INITIATED</div>
    <div class="cf-rf-arrow">&rarr;</div>
    <div class="cf-rf-node cf-rf-blue">IN_PROGRESS / PENDING</div>
  </div>
  <div class="cf-rf-connector">&darr;</div>
  <div class="cf-rf-branch-label">Branches to one of four outcomes</div>
  <div class="cf-rf-branches">
    <div class="cf-rf-node cf-rf-green">
      <div class="cf-rf-title">SUCCESS / REFUNDED</div>
    </div>
    <div class="cf-rf-node cf-rf-amber">
      <div class="cf-rf-title">ON_HOLD</div>
      <div class="cf-rf-caption">Low merchant balance or verification pending</div>
    </div>
    <div class="cf-rf-node cf-rf-amber">
      <div class="cf-rf-title">MANUAL</div>
      <div class="cf-rf-caption">Exhausted auto-retries, escalated to ops</div>
    </div>
    <div class="cf-rf-node cf-rf-red">
      <div class="cf-rf-title">FAILED / CANCELLED</div>
    </div>
  </div>
</div>
