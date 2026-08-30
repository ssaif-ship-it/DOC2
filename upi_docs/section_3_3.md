If you are a Stock Broker, Mutual Fund, Online Bond Platform Provider (OBPP), or Investment Adviser or Research Analyst (IA/RA), SEBI's rules put you in a different UPI category from most other merchants. You are onboarded under a distinct category, **MCC 6211 (Security Brokers/Dealers)**, and every payment you collect must pass Third-Party Validation (TPV) first. This section walks through what TPV actually changes for you, what your customer sees, and exactly what you need to do, bank by bank, to get set up.

## 1. What TPV Means For You

TPV enforces a single rule: a payment must come from a bank account registered in the investor's own name. A payment from any other account is rejected before it reaches settlement.

This exists to make sure your customer has explicitly authorized the investment they are paying into, to stop a common fraud pattern where money moves into an investment product from an account that is not the investor's own, and to meet RBI and NPCI's compliance requirements for UPI recurring collections in this category. For mandates above roughly ₹15,000, TPV also adds one more layer of authentication beyond the standard UPI PIN.

## 2. What Your Customer Sees

TPV adds exactly one extra step on top of a standard AutoPay mandate:

1.  Your customer selects the subscription, EMI, insurance, or mutual fund payment to set up.
2.  You trigger the UPI AutoPay request, via Intent, Collect, or Dynamic QR.
3.  Your customer approves the mandate request in their UPI app.
4.  The request is validated through NPCI and the TPV entity.
5.  Because this is a TPV transaction, your customer gets one additional OTP or consent prompt confirming the account is genuinely theirs.
6.  Once that clears, the mandate activates.
7.  Recurring debits proceed on schedule after that, each preceded by a Pre-Debit Notification. See [4.1 AutoPay](#doc-4-1) for how that part works.

<!-- Claude, flagging for Saif: is this flow accurate as merchant-facing, or does your integration need to handle any part of the OTP/TPV-entity verification step directly (4-5), rather than it being entirely bank-side? Written here as something that happens to the customer, not something you build for. Please confirm. -->

## 3. Which Banks Support This Today

*   **Standard TPV** checks the payment against a single registered account. Supported by ICICI, YES Bank, HDFC, and Axis.
*   **Multibank TPV** lets your customer register up to five accounts against one request. Supported by ICICI and HDFC.
*   TPV applies to both UPI Mandates and OTM (One-Time Mandate), so it covers a single premium payment the same way it covers a recurring SIP.

## 4. Your UPI Handle

In this category you get a dedicated UPI handle instead of a generic one, and Cashfree procures it on your behalf (see section 6 below for what that takes on your end). The suffix tells you which kind of payment it is for:

*   **One-time payments:** `MerchantName.cf.brk@[bank_identifier]`
*   **UPI AutoPay (recurring):** `MerchantName.cfp.brk@[bank_identifier]`

If you need to collect both one-time and recurring payments, you get both handles.

## 5. Where Your Money Settles

Settlement does not always land directly in your own account, it depends on your category.

<style>
  .onboarding-table-container {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    margin: 20px 0;
    overflow-x: auto;
  }

  .onboarding-table {
    border-collapse: collapse;
    width: 100%;
    max-width: 900px;
    background-color: #ffffff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    overflow: hidden;
  }

  .onboarding-table thead {
    background-color: #1a365d;
    color: #ffffff;
  }

  .onboarding-table th {
    text-align: left;
    padding: 16px 20px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .onboarding-table td {
    padding: 16px 20px;
    font-size: 14px;
    color: #2d3748;
    border-bottom: 1px solid #e2e8f0;
  }

  .onboarding-table tbody tr:nth-child(even) {
    background-color: #f7fafc;
  }

  .onboarding-table tbody tr:hover {
    background-color: #edf2f7;
    transition: background-color 0.2s ease;
  }

  .onboarding-table tbody tr:last-child td {
    border-bottom: none;
  }

  .intermediary-type {
    font-weight: 600;
    color: #1a202c;
  }

  /* Status Badges */
  .badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    min-width: 30px;
  }

  .badge-positive {
    background-color: #c6f6d5;
    color: #22543d;
  }

  .badge-negative {
    background-color: #fed7d7;
    color: #742a2a;
  }
</style>

<div class="onboarding-table-container">
  <table class="onboarding-table">
    <thead>
      <tr>
        <th>Category</th>
        <th>Settlement Destination</th>
        <th>TPV Required</th>
        <th>Direct Settlement (DS)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="intermediary-type">Stock Brokers</td>
        <td>Merchant's own designated bank account</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">Mutual Funds (MF)</td>
        <td>ICCL / NCCL clearing accounts</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">OBPPs</td>
        <td>ICCL / NCCL clearing accounts</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">IA / RA</td>
        <td>Cashfree Payments' Axis Escrow Account</td>
        <td><span class="badge badge-negative">No</span></td>
        <td><span class="badge badge-negative">OFF</span></td>
      </tr>
    </tbody>
  </table>
</div>

**If you are IA/RA:** TPV does not apply to you, and your funds route through Cashfree's escrow account instead of settling directly. Build this into your reconciliation and cash flow planning.

## 6. What You Need To Do, By Bank

Getting your handle procured takes a different amount of work from you depending on which bank you are on:

*   **If you are on Axis or HDFC:** nothing, from you. Cashfree procures and maps the handle on your behalf. Axis usually finishes faster since it is fully automated on our side; HDFC involves a manual step on their end and can take a bit longer.
*   **If you are on ICICI:** you will need to fill, sign, and submit the UPI Onboarding Form yourself, directly to your ICICI point of contact. If you are a Mutual Fund merchant, you also need ICCL/NCCL sign-off before you submit it.

<!-- Claude, flagging for Saif: removed the Retool/DMO-file/Banking-Ops-team detail and the isDMO flag note per your and Ayushi's comments, that is Cashfree's internal backend process, not something the merchant does. Also dropped "Terminals are created in a non-TPV state by default and must be manually updated" for the same reason. If that is something a merchant should confirm with their account manager before going live, rather than something Cashfree's ops team handles invisibly, let me know and I will add it back as a merchant-facing action item. -->
