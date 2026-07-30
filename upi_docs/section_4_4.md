

### About EMI on UPI
EMI on UPI is an NPCI-backed capability known as "Contextual Payments." It enables merchants to offer No-Cost and Low-Cost EMI directly on the UPI rail, specifically tailored for RuPay Credit Cards on UPI (with Credit Line on UPI planned for Phase 2).

This feature is highly significant because over 50% of RuPay credit cards issued today are cardless. Customers access their credit lines exclusively through UPI rather than physical cards, meaning they previously had no way to avail of EMI options. EMI on UPI bridges this gap.

---

## Use Cases and Business Value
* **Higher Conversions on Large Ticket Sizes:** Tap into a massive base of eligible users to drive conversions for orders typically above ₹3,000.
* **Purely Additive GMV:** This feature brings in entirely new users and does not cannibalize existing card-based EMI transactions.
* **Broad Merchant Base:** With nearly 3,500 merchants possessing RuPay CC users, hundreds are instantly eligible to boost revenue with potential initial GMV impacts of ₹126M+.

---

## Eligibility Check and Constraints (Phase 1)
Before integrating, please ensure your use case aligns with the Phase 1 capabilities:
* **Supported Banks:** Only SBI and HDFC RuPay Credit Cards are live in Phase 1.
* **Supported Flows:** Available strictly for Intent and QR Code flows. Collect requests are not supported.
* **Offer Combinations:** Discount + EMI combos are **NOT** supported in Phase 1 (Standard and No-Cost EMI only).
* **Deferred Features:** Low-cost EMI and Credit Line on UPI are deferred to Phase 2.

---

## EMI Types Supported

| Type | Code | Description |
| :--- | :--- | :--- |
| **Standard EMI** | `STDEMI` | Interest-bearing; the customer pays the principal amount plus interest. |
| **No-Cost EMI** | `NOCEMI` | The merchant absorbs the interest; the customer pays only the principal. |
| **Low-Cost EMI** | `LOCEMI` | Merchant partially subsidizes the interest (Deferred to Phase 2). |

---

## Payment Modes and Verification
EMI options are presented to the user via a context code embedded directly in the UPI QR or Intent link.

### Mode 1: User-Selected EMI (Open Mode)
1. The merchant generates a QR/intent link with a generic context code.
2. The customer scans the QR with their UPI app linked to a RuPay CC.
3. Both Cashfree and the Issuer Bank parallel-process the request to fetch eligible plans.
4. The customer selects their preferred plan (tenure, bank, type) in the UPI app and enters their PIN.
5. Standard UPI settlement occurs, and the EMI is booked at the issuing bank.

### Mode 2: Merchant Pre-Selected EMI (Locked Mode)
1. The merchant embeds a fully specified EMI plan (tenure, amount, rate) into the QR code.
2. The customer scans and sees a read-only locked plan.
3. The customer confirms with their UPI PIN.
4. If required meta tags are missing during authorization, the transaction is strictly declined.

---

## User Flow with Cashfree
1. **Checkout Page:** The user arrives at checkout and sees messaging indicating that EMI is supported for RuPay Credit Cards (SBI & HDFC).
2. **Scan/Click:** The user clicks the UPI intent link or scans the QR code.
3. **App Redirection:** The user is redirected to their UPI TPAP app.
4. **Plan Selection:** Switch checks the amount and fetches options. The user can either make a standard payment via a savings account or choose the eligible RuPay Credit Card to convert the transaction to EMI.
5. **Completion:** The user enters their UPI PIN to authorize the payment.

---

## Merchant Flow with Cashfree

### Dashboard Journey (No-Code Setup)
1. Log into the Cashfree Dashboard.
2. Navigate to the **Offers** section and create a No-Cost EMI offer (Type: RuPay Credit Card EMI).
3. Select Issuing Banks (**SBI** and **HDFC**).
4. Enable the RuPay flag to make the merchant eligible for Contextual EMI.
5. Once enabled, all generated intent links and QR codes will automatically carry the context code.

### API Integration Journey
For seamless merchants or API integrators, follow these steps:
1. **Create Offer:** Use the Cashfree Offers API to generate the EMI offer.
2. **Order Pay API:** Pass the newly created payment method `upi_cc_emi`.
   * For User-Selected EMI: pass `offer_id`.
   * For Merchant Pre-Selected EMI: pass `offer_id`, `emi.tenure`, and `emi.bank_name`.
3. **Checkout UI Update:** Render EMI plans via the Cashfree Offers API and display a note: *"HDFC and SBI support no-cost EMI via RuPay UPI"*.
4. **Webhook Handling:** Parse the new `emi_details` object in the payment success webhook. You will need to handle fields such as `emi_booking_id`, `status`, `tenure`, and `type`.
5. **Reconciliation:** Map the EMI transaction type in settlement reports. The backend will tag EMI transactions with Purpose Code `72`.

---

## API Webhook & Reconciliation Notes
After successful payment authorization, expect the following payload details:

```json
{
  "event": "payment_success",
  "data": {
    "payment": {
      "emi_details": {
        "emi_booking_id": "string",
        "status": "EMISTATUS",
        "tenure": "integer",
        "type": "string"
      }
    }
  }
}