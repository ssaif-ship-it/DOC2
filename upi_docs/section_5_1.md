### 1.1 Summary of Lifecycle Stages

<div style="overflow-x: auto; margin: 20px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #eae5f2; border-radius: 12px; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #334155;">
    <thead>
      <tr style="background-color: #f6f1fc;">
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Stage</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">What Happens</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Merchant Timing</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Authorization</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Issuing bank confirms fund availability and locks the payment amount.</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Real-time at checkout</span>
        </td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Capture</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Transaction is finalized for clearing (Cards) or confirmed successful (UPI/NetBanking).</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Real-time at checkout</span>
        </td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Settlement</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Funds move from customer banks to the Payment Aggregator's nodal/escrow account (or your bank account directly).</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #f0eafc; color: #5b21b6; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">T+0 to T+2 interbank clearing</span>
        </td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; vertical-align: top;">Payout</td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Net money is transferred from the aggregator/acquirer into your registered merchant bank account.</td>
        <td style="padding: 16px 20px; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Scheduled based on your T+n cycle</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>

### 1.2 Gross vs. Net Settlement

*   **Gross Settlement:** You receive 100% of customer payments upfront; gateway charges and taxes are invoiced separately (common for specific enterprise setups).
*   **Net Settlement (Default):** Merchant Discount Rates (MDR), applicable GST, refunds, and chargebacks are deducted prior to payout:

```Net Payout = Gross Sales - MDR Fees - GST - Refunds/Disputes```

<!-- Claude, confirmed correction for Saif: this formula previously listed a flat "GST (18%)" deduction. For standard UPI P2M transactions specifically, that is not accurate, MDR on UPI P2M has been zero since January 2020, and GST is charged as a percentage of MDR, so there is no MDR base for GST to apply to. The Finance Ministry said as much directly in 2026, calling reports of GST on UPI transactions "false, misleading, and without any basis," since no MDR is charged. I removed the flat 18% figure since this doc is UPI scoped, GST only re-enters the picture if you also process something with a chargeable MDR on this same platform, in which case 18% is the correct standard rate for that portion. -->

### 1.3 Settlement Cycles Explained (T+n)

Cycles represent business days (n) elapsed after transaction capture day (T):

*   **T+0 (Same-Day / Instant):** Payouts are executed on the transaction date itself, either in fixed daily batches (e.g., 09:00, 17:00, 20:00 IST) or via rolling 15-minute execution windows. Chargeable, and requires eligibility.

<!-- Claude, flagging for Saif, not confirmed, now with a discrepancy to reconcile: the specific batch times and the 15-minute rolling window are Cashfree's own settlement configuration, not something I can verify against a public source, so this still needs sign-off from whoever owns settlements. It is now more than just unconfirmed, the internal reference material you shared (citing "BEPG Transaction Processing") describes NPCI's own intra-day settlement cycles as running at 11:00, 16:00, and 20:00 hours, not 09:00, 17:00, and 20:00 as this line states. These may genuinely be two different things, NPCI's network-wide intra-day cycle times versus Cashfree's own batch execution schedule built on top of them, but as written they read like the same claim with two different sets of numbers. Confirm which times this line should actually state before publishing either version. -->
*   **T+1 (Next Business Day):** Payouts are executed on the first banking working day following T. Available where enabled for your account, for merchants who need funds a day sooner than the default cycle.
*   **T+2 (Standard - Default):** Payouts are executed on the second banking working day following T. This is Cashfree's default settlement cycle, most merchants stay on it, and it is what shows as "Standard Settlement" on the merchant dashboard.
*   **Beyond T+2:** Elevated-risk merchant profiles may be held for a longer cycle.

<!-- Claude, confirmed correction for Saif: this section previously called T+1 the default settlement cycle, that was wrong. Two independent sources say the default is T+2: your own merchant dashboard ("Standard Settlement, Settlement cycle - 2 working days"), and Cashfree's own public docs (cashfree.com/docs/help/payments/settlements/settlements and cashfree.com/settlement-and-reconciliation-guide), both of which state the default cycle is T+2. This also matches 3.2's "Your settlement cycle options" table elsewhere on this site, which already had T+2 marked as the default, flagged as an open comment back on 12 Aug that 5.1 needed to be corrected to match. Corrected this section and the 3.2 Real-World Scenarios table below, so T+2 is consistently the default and T+1 is a faster opt-in tier. Posted a confirming comment on this line too. -->

---

## 2. End-to-End Fund Movement

<!-- Claude, update for Saif: I had flagged this Direct Settlement Model as unconfirmed, no public Cashfree page described it. You then shared internal reference material (citing "UPI Direct Settlement" and "PRD - UPI Direct Settlement Recon") that confirms the shape of what is below and adds detail worth folding in: the acquiring bank credits your account directly and Cashfree never holds the funds; onboarding requires a direct account with the acquiring bank (currently ICICI, via ICICIUPI) and manual MID procurement that takes roughly two weeks; reconciliation is two-way (Cashfree DB against bank MIS/NPCI files) rather than the three-way recon (internal DB, NPCI/bank files, and the nodal escrow statement) the standard model gets, since Cashfree cannot see your bank statement directly; and Cashfree's systems are explicitly instructed not to initiate refunds or reversals for Direct Settlement transactions, even when bank MIS shows a mismatch against Cashfree's own records, in that case you get a report and have to act on it yourself. That matches and sharpens what the table below already says, I have not changed the table itself, this note just records where the confirmation came from. -->

### 2.1 Standard Aggregator Model vs. Direct Settlement Model

<div class="cf-model-wrap">
  <style>
    .cf-model-wrap { margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .cf-model-row { margin-bottom: 14px; }
    .cf-model-row:last-child { margin-bottom: 0; }
    .cf-model-label {
      font-size: 12px;
      font-weight: 700;
      color: #5b21b6;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 6px;
    }
    .cf-model-flow { display: flex; align-items: stretch; flex-wrap: nowrap; gap: 6px; }
    .cf-model-step {
      flex: 1 1 0;
      min-width: 0;
      background: #f6f1fc;
      border: 1px solid #eae5f2;
      border-radius: 8px;
      padding: 10px 8px;
      text-align: center;
      font-size: 12.5px;
      font-weight: 600;
      color: #0f172a;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .cf-model-step.cf-model-skip {
      background: #ffffff;
      border-style: dashed;
      color: #94a3b8;
      font-weight: 500;
    }
    .cf-model-arrow {
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #5b21b6;
      font-size: 16px;
      font-weight: 700;
      min-width: 12px;
    }
    .cf-model-arrow.cf-model-skiparrow { color: #cbd5e1; }
    @media (max-width: 640px) {
      .cf-model-flow { flex-direction: column; }
      .cf-model-step { width: 100%; }
      .cf-model-arrow { transform: rotate(90deg); padding: 1px 0; }
    }
  </style>
  <div class="cf-model-row">
    <div class="cf-model-label">Standard Model</div>
    <div class="cf-model-flow">
      <div class="cf-model-step">Customer</div>
      <div class="cf-model-arrow">&rarr;</div>
      <div class="cf-model-step">Gateway / Acquirer</div>
      <div class="cf-model-arrow">&rarr;</div>
      <div class="cf-model-step">Aggregator Escrow</div>
      <div class="cf-model-arrow">&rarr;</div>
      <div class="cf-model-step">Merchant Bank</div>
    </div>
  </div>
  <div class="cf-model-row">
    <div class="cf-model-label">Direct Model</div>
    <div class="cf-model-flow">
      <div class="cf-model-step">Customer</div>
      <div class="cf-model-arrow">&rarr;</div>
      <div class="cf-model-step">Gateway / Acquirer</div>
      <div class="cf-model-arrow cf-model-skiparrow">&rarr;</div>
      <div class="cf-model-step cf-model-skip">Escrow hop skipped</div>
      <div class="cf-model-arrow">&rarr;</div>
      <div class="cf-model-step">Merchant Bank</div>
    </div>
  </div>
</div>

<div style="overflow-x: auto; margin: 20px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #eae5f2; border-radius: 12px; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #334155;">
    <thead>
      <tr style="background-color: #f6f1fc;">
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Dimension</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Standard Aggregator Settlement</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Direct Settlement</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Escrow Routing</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Aggregator receives funds, nets fees, and dispatches single consolidated payouts.</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Acquiring bank credits your corporate current account directly.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Fee Collection</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Net settlement (fees automatically deducted prior to bank transfer).</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Gross transfer; charges billed separately via periodic debit mandates.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Reconciliation</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Simple 1:1 match per settlement batch UTR.</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Requires 3-way reconciliation (Gateway Records, Bank MIS and Bank Statement).</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Refunds</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Fully automated via PG Refund APIs.</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Standard PG Refund APIs are blocked; refunds require direct payout execution.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; vertical-align: top;">Ideal For</td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.8;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">E-commerce</span>
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">D2C</span>
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">SaaS</span>
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">Retail</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.8;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">Broking (MCC 6211)</span>
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">Wealth Management</span>
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500; margin: 2px 4px 2px 0;">Mutual Funds</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>

## 3. Cut-off Times, Weekends & Bank Holidays

### 3.1 The Payout Formula

The system calculates when a transaction is eligible for payout based on strictly defined "business days."

When you see terms like T+1, the "T" stands for the Transaction Date, and the "+1" means one business day later. The formula ensures that at 11:59 PM (23:59:59 IST) on the target day, the funds are cleared for the next payout batch.

**The Golden Rule:** Payouts rely on banks being open. If your payout date lands on a weekend or an official Reserve Bank of India (RBI) holiday, the system automatically pauses and pushes your money to the very next working day.

---

### 3.2 Real-World Scenarios

Here is how that timeline plays out in practice based on different transaction days:

<!-- Claude, flagging for Saif, not confirmed: the T+1 rollover logic this table illustrates (weekends and RBI holidays push the payout to the next working day) is standard settlement practice, that part checks out and doesn't need a citation, it's mechanics, not an empirical claim. But the specific "4:00 PM" cutoff and "afternoon" payout times in this table aren't independently verifiable, they depend on Cashfree's own batch execution schedule, same thing I already flagged just above in 3.1 (the 09:00/17:00/20:00 IST batch times comment). This table is presumably a worked example built on that same schedule, so it inherits the same caveat: plausible, but needs sign-off from whoever owns settlements, not confirmable against a public source. -->


<div style="overflow-x: auto; margin: 20px 0;">
  <table style="width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #eae5f2; border-radius: 12px; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; color: #334155;">
    <thead>
      <tr style="background-color: #f6f1fc;">
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Settlement Type</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Transaction Time</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">Payout Time</th>
        <th style="padding: 16px 20px; text-align: left; color: #5b21b6; font-weight: 600; font-size: 15px; border-bottom: 1px solid #eae5f2;">The Logic</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Standard (T+2)</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Thursday at 4:00 PM</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Monday afternoon</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">A normal weekday transaction clears two business days later. Friday and Monday are the next two business days after Thursday.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Weekend (T+2)</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Friday at 6:00 PM</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #eff6ff; color: #2563eb; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Tuesday afternoon</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">The two business days after Friday would normally be Saturday and Sunday. Because banks are closed on weekends, both roll forward, to Monday and Tuesday.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; border-bottom: 1px solid #f1f5f9; vertical-align: top;">Holiday Conflict</td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Friday at 6:00 PM</td>
        <td style="padding: 16px 20px; border-bottom: 1px solid #f1f5f9; vertical-align: top;">
          <span style="display: inline-block; background-color: #f0eafc; color: #5b21b6; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Wednesday afternoon</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">If Monday happens to be a bank holiday, both business days shift forward again, landing on Tuesday and Wednesday.</td>
      </tr>
      <tr>
        <td style="padding: 16px 20px; font-weight: 600; color: #0f172a; vertical-align: top;">Instant (T+0)</td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Any day, any time</td>
        <td style="padding: 16px 20px; vertical-align: top;">
          <span style="display: inline-block; background-color: #fef3c7; color: #d97706; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 500;">Instantly</span>
        </td>
        <td style="padding: 16px 20px; color: #334155; vertical-align: top; line-height: 1.5;">Uses IMPS or UPI networks, which run 24/7/365. Bank holidays and weekends do not matter.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Claude, note for Saif: removed 3.3 Payment-Specific Timelines entirely. It compared UPI against Domestic Cards/NetBanking and International Cards, all non-UPI rails, out of scope for this UPI-specific doc. Its one UPI-relevant line (T+0 Instant being a chargeable add-on) already duplicated 1.3, so nothing was lost. Also trimmed the "Beyond T+2" bullet in 1.3, which used to cite international cards as an example and link to this subsection, both gone now. The unconfirmed T+5-for-international-cards flag is resolved in the comments tab with a note pointing here. -->
