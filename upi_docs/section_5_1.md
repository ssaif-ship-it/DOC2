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
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Funds move from customer banks to the Payment Aggregator’s nodal/escrow account (or your bank account directly).</td>
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
*   **Net Settlement (Default):** Merchant Discount Rates (MDR), GST (18%), refunds, and chargebacks are deducted prior to payout:

```Net Payout = Gross Sales - MDR Fees - GST - Refunds/Disputes```

### 1.3 Settlement Cycles Explained (T+n)

Cycles represent business days (n) elapsed after transaction capture day (T):

*   **T+0 (Same-Day / Instant):** Payouts are executed on the transaction date itself, either in fixed daily batches (e.g., 09:00, 17:00, 20:00 IST) or via rolling 15-minute execution windows.
*   **T+1 (Next Business Day - Default):** Payouts are executed on the first banking working day following T.
*   **T+2 / Extended:** Applied for international card transactions, specific alternative payment methods, or elevated risk categories.

---

## 2. End-to-End Fund Movement

### 2.1 Standard Aggregator Model vs. Direct Settlement Model

> **Standard Model:**  [Customer] ---> [Gateway/Acquirer] ---> [Aggregator Escrow] ---> [Merchant Bank]
> **Direct Model:**    [Customer] ---> [Gateway/Acquirer] -------------------------> [Merchant Bank]

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
        <td style="padding: 16px 20px; color: #334155; border-bottom: 1px solid #f1f5f9; vertical-align: top; line-height: 1.5;">Requires 3-way reconciliation (Gateway Records ↔ Bank MIS ↔ Bank Statement).</td>
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

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Modern Settlement Table</title>
<style>
  /* Reset and base font */
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 40px;
    background-color: #ffffff;
    display: flex;
    justify-content: center;
  }

  /* Main container matching the rounded, bordered look */
  .styled-table-container {
    width: 100%;
    max-width: 1050px;
    border: 1px solid #F1F5F9;
    border-radius: 12px;
    overflow: hidden; 
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }

  /* Purple header styling matching the new image */
  th {
    background-color: #F8F4FE; /* Light purple background */
    color: #6B21A8; /* Vibrant purple text */
    font-weight: 600;
    font-size: 16px;
    padding: 20px 24px;
    border-bottom: 1px solid #F1F5F9;
  }

  /* Row styling */
  td {
    padding: 24px;
    border-bottom: 1px solid #F8FAFC;
    color: #475569;
    font-size: 15px;
    line-height: 1.6;
    vertical-align: middle;
  }

  tr:last-child td {
    border-bottom: none;
  }

  /* Bold left column for emphasis */
  td:first-child {
    font-weight: 600;
    color: #0F172A;
    font-size: 16px;
  }

  /* Pill Badges */
  .pill {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 9999px; /* Fully rounded corners */
    font-weight: 500;
    font-size: 14px;
    white-space: nowrap;
  }

  /* Colors exactly matching the new reference image */
  .pill-blue {
    background-color: #EFF6FF;
    color: #2563EB;
  }

  .pill-orange {
    background-color: #FEF3C7;
    color: #D97706;
  }
</style>
</head>
<body>

<div class="styled-table-container">
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Settlement Type</th>
        <th style="width: 20%;">Transaction Time</th>
        <th style="width: 40%;">The Logic</th>
        <th style="width: 20%;">Payout Time</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Standard (T+1)</td>
        <td>Thursday at 4:00 PM</td>
        <td>A normal weekday transaction clears on the next consecutive business day.</td>
        <td><span class="pill pill-blue">Friday afternoon</span></td>
      </tr>
      <tr>
        <td>Weekend (T+1)</td>
        <td>Friday at 6:00 PM</td>
        <td>The "+1" day lands on Saturday. Because banks are closed on weekends, it rolls to Monday.</td>
        <td><span class="pill pill-blue">Monday afternoon</span></td>
      </tr>
      <tr>
        <td>Holiday Conflict</td>
        <td>Friday at 6:00 PM</td>
        <td>If Monday happens to be a bank holiday, the payout rolls forward again to Tuesday.</td>
        <td><span class="pill pill-orange">Tuesday afternoon</span></td>
      </tr>
      <tr>
        <td>Instant (T+0)</td>
        <td>Any day, any time</td>
        <td>Uses IMPS or UPI networks, which run 24/7/365. Bank holidays and weekends do not matter.</td>
        <td><span class="pill pill-orange">Instantly</span></td>
      </tr>
    </tbody>
  </table>
</div>

</body>
</html>
---

### 3.3 Payment-Specific Timelines 

You are not forced to pick a single payout schedule for your entire business. The system allows you to configure different settlement speeds based on the type of payment your customer used.

This is usually done to balance cash flow with fraud prevention:

*   **UPI Transactions:** Can be set to T+0 (Instant). Because UPI is highly secure and runs 24/7, you can get this money immediately.
*   **Domestic Cards & NetBanking:** Set to T+1 (Next working day). This is standard for normal Indian banking channels.
*   **International Cards:** Set to T+5 (5 days later). Cross-border payments carry a much higher risk of fraud and chargebacks, so the gateway holds the funds longer to ensure the transaction is legitimate before passing it to you.