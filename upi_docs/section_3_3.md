If you are a Stock Broker, Mutual Fund, Online Bond Platform Provider (OBPP), or Investment Adviser or Research Analyst (IA/RA), SEBI's rules put you in a different UPI category from most other merchants. You are onboarded under a distinct category, **MCC 6211 (Security Brokers/Dealers)**, and every payment you collect must pass Third-Party Validation (TPV) first. This section walks through what TPV actually changes for you, what your customer sees, and exactly what you need to do, bank by bank, to get set up.

## 1. What TPV Means For You

TPV enforces a single rule: a payment must come from a bank account registered in the investor's own name. Cashfree shares your customer's expected bank account details with their bank, and the bank checks that the payment is actually coming from that account before it goes through. A payment from any other account fails and never reaches settlement.

This exists to make sure your customer has explicitly authorized the investment they are paying into, to stop a common fraud pattern where money moves into an investment product from an account that is not the investor's own, and to meet RBI and NPCI's compliance requirements for UPI recurring collections in this category.

<!-- Claude, flagging for Saif: dropped the earlier "additional authentication above ₹15,000" line here. That is a real NPCI rule for recurring UPI mandates in general, but I have not found it confirmed specifically for TPV mandates on Cashfree's public docs, so I did not want to state it as a TPV specific fact. Added it to the open questions list instead. -->

## 2. What Your Customer Sees

1.  Your customer selects the subscription, EMI, insurance, or mutual fund payment to set up.
2.  You trigger the UPI AutoPay request, via Intent, Collect, or Dynamic QR, passing your customer's registered bank account number and IFSC with the request.
3.  Your customer approves the mandate request in their UPI app, the same way as any AutoPay mandate. There is no separate extra prompt shown to them for TPV specifically.
4.  Behind the scenes, the bank checks that the account approving the mandate matches the one you registered. If your customer approves from a different account than the one registered, the mandate fails, and the order can remain in a pending state rather than show as failed right away, so build your reconciliation around that rather than expecting an instant decline.
5.  Once the match clears, the mandate activates, and recurring debits proceed on schedule after that, each preceded by a Pre-Debit Notification. See [4.1 AutoPay](#doc-4-1) for how that part works.

<!-- Claude, confirmed for Saif: rewrote this flow against Cashfree's own public TPV docs (cashfree.com/docs/payments/features/tpv), which describe this same account matching mechanism. That page does not mention any extra OTP or consent step for TPV specifically, only that a mismatched account fails, so I removed the earlier "additional OTP" claim, it was not something I could verify. That page also does not confirm whether this is the exact same TPV system used for the SEBI investment category specifically, since it is written as a generic feature for any merchant, not this category. See the open questions list for this. -->

## 3. Which Banks Support This Today

*   **Standard TPV (single registered account):** works over UPI with any UPI app or bank, Cashfree's public docs state that all UPI apps support this account validation.
*   **Multi-bank TPV (your customer registers up to 4 accounts, not 5):** supported on UPI, NetBanking, and bank transfers. For UPI specifically, it only works on select UPI rails and needs to be turned on for your account, contact your Cashfree account manager to enable it.
*   **NetBanking TPV** is supported across a long list of banks, over 50 at last count, including SBI, HDFC, ICICI, Axis, Kotak, and Yes Bank, alongside most other public and private banks. <!-- Claude, the full bank by bank list is at cashfree.com/docs/payments/features/tpv#netbanking-supported-banks if you need to check one specific bank. -->
*   TPV applies to both UPI Mandates and OTM (One-Time Mandate), so it covers a single premium payment the same way it covers a recurring SIP.

<!-- Claude, flagging for Saif: this section previously said standard TPV was "Supported by ICICI, YES Bank, HDFC, and Axis" and multi-bank allowed "up to five accounts, supported by ICICI and HDFC." I could not find either claim on Cashfree's public docs, rewritten to match what the public TPV feature page actually says (no bank restriction for standard UPI TPV, four accounts max for multi-bank). See the open questions list, since this public page is generic and does not confirm it is the same system used for this investment category specifically. -->

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
