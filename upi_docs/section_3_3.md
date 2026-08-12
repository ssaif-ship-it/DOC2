Stock Brokers, Mutual Funds, Online Bond Platform Providers (OBPPs), and Investment Advisers/Research Analysts (IA/RAs) are onboarded under a distinct SEBI-regulated category, **MCC 6211 (Security Brokers/Dealers)**. The defining requirement for this category is Third-Party Validation (TPV) on every payment collected.

## 1. Why TPV Applies

TPV enforces a single rule: an investor's payment must originate from a bank account registered in their own name. A payment from any other account is rejected before it reaches settlement.

This requirement exists to:

*   Ensure investors are aware of, and have explicitly authorized, every recurring payment linked to their investments.
*   Prevent a common fraud pattern: payment into an investment product from an account that does not belong to the investor.
*   Meet RBI and NPCI compliance requirements for UPI-based recurring collections in this category.
*   Add a further authentication layer, beyond the standard UPI PIN, for mandates above approximately ₹15,000.

## 2. The Customer Experience

TPV adds one additional step to mandate setup, compared to a standard AutoPay mandate:

1.  The customer selects the subscription, EMI, insurance, or mutual fund payment to set up.
2.  The merchant triggers the UPI AutoPay request, via Intent, Collect, or Dynamic QR.
3.  The customer approves the mandate request in their UPI app.
4.  The request is validated through NPCI and the TPV entity.
5.  Because this is a TPV transaction, the customer receives one additional OTP or consent prompt confirming the account is genuinely theirs.
6.  On successful authentication, the mandate activates.
7.  Recurring debits then proceed on schedule, each preceded by a Pre-Debit Notification. See [4.1 AutoPay](#doc-4-1) for how recurring debits and notifications work.

<!-- Claude, flagging for Saif: is this flow accurate as merchant-facing, or does the merchant's integration need to handle any part of the OTP/TPV-entity verification step directly (4-5), rather than it being entirely bank-side? Written here as something that happens to the customer, not something the merchant builds for. Please confirm. -->

## 3. Standard vs. Multibank TPV

*   **Standard TPV** validates against a single registered account. Supported by ICICI, YES Bank, HDFC, and Axis.
*   **Multibank TPV** allows registration of up to five accounts against one request. Supported by ICICI and HDFC.
*   TPV applies to both UPI Mandates and OTM (One-Time Mandate), covering single premiums and recurring SIPs alike.

## 4. UPI Handle Format

Merchants in this category are issued a dedicated UPI handle rather than a generic one; Cashfree procures this on the merchant's behalf (see Section 6). The suffix identifies the payment type:

*   **One-time payments:** `MerchantName.cf.brk@[bank_identifier]`
*   **UPI AutoPay (recurring):** `MerchantName.cfp.brk@[bank_identifier]`

Merchants requiring both one-time and recurring collections are issued both handles.

## 5. Settlement Routing

Settlement does not always route directly to the merchant's own account; this depends on category.

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

**Note:** For IA/RA merchants, TPV does not apply, and funds route through Cashfree's escrow account rather than settling directly. This should be factored into reconciliation and cash flow planning.

## 6. Handle Procurement Process

Procurement effort depends on the acquiring bank:

*   **Axis and HDFC:** No action required from the merchant. Cashfree procures and maps the handle. Axis is typically faster, since it is handled through an internal API; HDFC is a manual process and can take longer.
*   **ICICI:** The merchant must fill, sign, and submit the UPI Onboarding Form directly to their ICICI point of contact. Mutual Fund merchants additionally require ICCL/NCCL sign-off before submission.

<!-- Claude, flagging for Saif: removed the Retool/DMO-file/Banking-Ops-team detail and the isDMO flag note per your and Ayushi's comments, that is Cashfree's internal backend process, not something the merchant does. Also dropped "Terminals are created in a non-TPV state by default and must be manually updated" for the same reason. If that is something a merchant should confirm with their account manager before going live, rather than something Cashfree's ops team handles invisibly, let me know and I will add it back as a merchant-facing action item. -->
