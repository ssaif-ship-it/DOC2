# Affordability & Contextual Payments on UPI

Enabling Contextual Payments & Affordability on your checkout, offers flexible payment options, like EMI on UPI, UPI Lite for micro-transactions, and Interoperable PPI Wallets, directly to your customers, reducing cart abandonment and driving higher average order values.

## 1. RuPay Credit Card EMI on UPI

We have enabled real-time EMI options for customers paying via RuPay Credit Cards on standard UPI QR codes and Intent links. By providing instant EMI capabilities natively at checkout, you can drastically lower barriers for high-ticket purchases.

### Key Merchant Benefits

*   **Higher Conversions:** Presenting flexible options directly at checkout reduces customer drop-offs by up to 30%.
*   **Increased Ticket Size:** Let customers purchase higher-value items, driving a 40% to 60% increase in Average Order Value (AOV).
*   **Zero Risk:** Upfront settlement guarantees you receive the full transaction amount (less applicable subvention discounts), while the issuing bank bears the repayment risk.

<!-- Claude, flagging for Saif, not confirmed: could not find any independent benchmark supporting "up to 30%" drop-off reduction or "40% to 60%" AOV increase specifically for EMI-at-checkout. Industry blog content on EMI/BNPL and AOV shows a wide, inconsistently sourced spread (one source cites 10-15% abandonment reduction, another describes purchase likelihood rising from 17% to 26%, neither matching these figures). These read as internal marketing numbers; if there's a Cashfree-internal study behind them, worth citing it, otherwise consider softening to something like "can meaningfully reduce drop-offs and increase order values" rather than specific percentages that can't be sourced. -->

### Current Supported Scope

*   **Supported Banks:** Real-time EMI is currently supported for SBI and HDFC RuPay Credit Cards.
*   **Supported Flows:** Enabled exclusively for UPI Intent Links and Dynamic QR Codes.
*   **Unsupported Flows:** Contextual EMI is strictly prohibited for UPI Collect requests. Combining flat discounts with EMI offers is not supported at this time.

<!-- Claude, flagging for Saif, not confirmed: "Supported Banks: SBI and HDFC only" reads as an early Phase 1 rollout constraint with no date attached. RuPay Credit Card on UPI itself (the base rail this EMI feature sits on top of) is live across 15+ issuing banks including ICICI, Axis, and Kotak, not just SBI and HDFC, and the wider market for EMI-at-checkout on UPI has moved fast, with NBFC-backed issuers like Kiwi launching competing instant-EMI-on-UPI products in October 2025. I could not confirm whether Cashfree's own SBI/HDFC-only constraint is still current or has since expanded, since that is an internal rollout detail, not something published externally. Worth confirming with product before this goes out with no caveat, a merchant reading "currently supported" today may reasonably expect it to include their customer's bank. -->

### Category Restrictions on RuPay Credit Card on UPI

Before EMI can apply, the base RuPay Credit Card on UPI method itself has to be available to the customer. NPCI excludes the following categories from accepting RuPay Credit Card payments via UPI at all, regardless of MCC:

*   Person-to-person and person-to-person-merchant transfers (P2P, P2PM)
*   Digital account opening
*   Lending platforms
*   Cash withdrawal, at a merchant or at an ATM
*   eRUPI
*   IPO
*   Foreign inward remittances
*   Mutual funds
*   Any other category the issuing bank or RBI separately restricts

This list is defined by category, not by MCC number. If your business falls into one of these categories, RuPay Credit Card will not appear as a UPI payment option for your customers, and the EMI feature above is not reachable either.

## 2. EMI Subvention & Affordability Engine

You can configure both No-Cost EMI and Low-Cost EMI structures via the Merchant Dashboard or API.

In a No-Cost EMI model, the customer pays only the product sticker price, split equally over the selected months. You, as the merchant, absorb the interest by offering an upfront discount equivalent to the total interest charged by the bank.

### Mathematical Amortization Model

The monthly installment (EMI) paid by the customer is calculated using the standard amortized equation:

```
EMI = [P * R * (1 + R)^N] / [(1 + R)^N - 1]
```

Where:

*   A = Order Amount / Product Sticker Price (total paid by customer)
*   P = Adjusted Base Principal (settled upfront to merchant)
*   R = Monthly Interest Rate charged by issuing bank (Annual Rate / 12 / 100)
*   N = Repayment Tenure in months
*   EMI = Monthly Installment Amount, where EMI = A / N for No-Cost EMI

To determine the net Principal amount (P) settled to you:

```
P = [EMI * ((1 + R)^N - 1)] / [R * (1 + R)^N]
```

### Standard Calculation Example (3-Month No-Cost EMI at 16% p.a.)

| Parameter | Value | Description |
| --- | --- | --- |
| Order Amount (A) | ₹10,000 | Total amount paid by customer over N months |
| Tenure (N) | 3 Months | Chosen repayment duration |
| Bank Interest Rate | 16% p.a. | Bank's credit card interest rate |
| Monthly EMI | ₹3,333 | Fixed monthly amount paid by customer |
| Adjusted Principal (P) | ₹9,739 | Calculated base amount |
| Merchant Subvention | ₹261 | Upfront discount absorbed by merchant |
| Upfront Settlement | ₹9,739 | Amount settled to merchant |

For Low-Cost EMI, you specify a capped interest subvention percentage, and the customer pays the remaining balance interest.

## 3. Integration & Post-Payment Lifecycle

### Dashboard Configuration

Log in to your Merchant Dashboard, navigate to **Offers & Affordability > Create Offer**, and select **RuPay Credit Card EMI**. Set your tenure rules and subvention type. Once saved, rule configurations are instantly replicated to the payment engine.

### API Integration

When creating an order, request a contextual Intent link or Dynamic QR by specifying the `upi_cc_emi` payment method. The API attaches the required contextual metadata (`ctxtCode: "03"`) automatically.

```json
{
  "order_id": "order_99887766",
  "order_amount": 10000.00,
  "order_currency": "INR",
  "payment_method": {
    "upi": {
      "channel": "intent",
      "ctxtCode": "03",
      "prodCode": "SKU-44321"
    }
  }
}
```

<!-- Claude, flagging for Saif, not confirmed: ctxtCode "03" and the prodCode field could not be found in any published NPCI or integrator documentation I could access, this looks like an internal Cashfree implementation detail rather than a public NPCI spec value. Since this is a live copy-pasteable API example a merchant could lift directly into their integration, worth a quick internal check that "03" is still the correct, current value before publishing, a wrong context code here would silently break contextual EMI at checkout for anyone who copies it as-is. -->

### Reconciliation & Refunds

*   **Purpose Code:** All EMI-converted UPI transactions are tagged with Purpose Code 72 across webhooks and settlement reports.
*   **Settlement:** Standard payments are settled at the full order amount minus MDR. No-Cost EMI payments are settled at the net principal amount (P) minus standard fees.
*   **Refunds:** On a full refund, the net principal amount (P) is debited from your account, and the issuing bank cancels the customer's EMI schedule via NPCI's Unified Dispute and Issue Resolution (UDIR) framework.

<!-- Claude, flagging for Saif, likely wrong: checked "Purpose Code 72" against every published UPI purpose code table I could find (NPCI's own material and integrator docs like Juspay's, which list codes up to 71 and then jump straight to 76, 77, 82, 87, 92). Code 72 does not appear anywhere tied to EMI or anything else, this needs a real internal source before publishing, a merchant filtering webhooks or settlement reports by this code would get nothing back if it's wrong. Separately, "via NPCI's Unified Dispute and Issue Resolution (UDIR) framework" for a routine EMI cancellation on a normal refund reads like a mismatch, UDIR is NPCI's customer-raised grievance and dispute mechanism (used when something goes wrong, like a wrongly debited transaction), not the mechanism for a standard merchant-initiated refund reversing a mandate. Worth confirming whether this is really routed through UDIR or just standard reversal processing. Same UDIR phrasing appears again further down in the PPI refunds section, flagged separately there. -->

## 4. UPI Lite & Prepaid Wallets (PPI)

To help you accept micro-transactions and alternative funding sources, our checkout fully supports UPI Lite and Interoperable Prepaid Wallets.

### UPI Lite (On-Device Wallet)

UPI Lite is an on-device wallet designed for 1-click, PIN-less payments, up to **₹1,000 per transaction**, **₹10,000 cumulative per day**, with a maximum on-device wallet balance of **₹5,000** at any time.

*   **Seamless Micro-Payments:** Customers experience sub-second transaction speeds without entering a UPI PIN.
*   **Fallback Mechanism:** If the order amount exceeds ₹1,000, the daily cumulative cap is reached, or the Lite balance is insufficient, the checkout automatically falls back to standard 2FA UPI requiring a PIN.
*   **No Extra Integration:** Enabled automatically on standard UPI Intent and QR flows.
*   **Not for Mandates:** UPI Lite cannot be used for AutoPay or other UPI Mandate executions, which require the full bank-authenticated flow.

### Prepaid Wallets (Interoperable PPI)

Full-KYC Prepaid Payment Instruments (like Paytm Wallet, Amazon Pay, and PhonePe Wallet) are fully integrated into the UPI ecosystem. Customers can utilize their pre-funded wallet balances to pay at your existing UPI QR codes or Intent links without any explicit onboarding required on your end.

#### Interchange Fees for PPI Wallet Acceptance

Unlike standard savings account UPI transactions, PPI interoperable transactions incur an Interchange Fee paid by the merchant to cover the wallet issuer's infrastructure costs.

| Transaction Category | Transaction Ceiling | Interchange Fee |
| --- | --- | --- |
| Standard Retail & E-Commerce | Up to ₹2,000 | 0.0% (Free) |
| Standard Retail & E-Commerce | > ₹2,000 | 1.1% |
| Fuel Stations | Any Amount | 0.5% |
| Utilities, Telecom, Post Office, Agriculture & Education | Any Amount | 0.7% |
| Supermarkets | Any Amount | 0.9% |
| Insurance, Mutual Funds & Railways | Any Amount | 1.1% |

<!-- Claude, confirmed correction for Saif: the table previously listed "Educational Services" and "Agriculture & Mutual Funds" as separate 0.7% rows, and had no Supermarkets row at all. Per NPCI's April 2023 PPI interchange circular (still current per Razorpay's Feb 2026 UPI charges page, razorpay.com/learn/upi-transaction-charges), the real structure is: Fuel 0.5%; Post Office, Telecom, Utilities, Agriculture and Education together at 0.7%; Supermarkets at 0.9% (was missing entirely); and Insurance, Mutual Funds and Railways together at 1.1%, not 0.7%. Mutual Funds was misplaced in the old table, it belongs in the top bracket with Insurance and Railways, not with Agriculture. Also dropped the stray escaped "\>" so it renders as a normal ">" character. -->

### Important PPI Rules

*   **No Consumer Surcharging:** You are strictly prohibited from charging extra convenience fees to customers choosing to check out using PPI wallets.
*   **Automated Source Refunds:** When you issue a refund for a PPI-funded transaction, funds are routed strictly back to the originating wallet ID via the UDIR framework.

<!-- Claude, flagging for Saif, not confirmed: same UDIR concern as the EMI refunds subsection above, UDIR is NPCI's dispute and grievance mechanism, not the standard path for a routine merchant-initiated refund. Worth confirming this is actually routed through UDIR rather than ordinary refund/reversal processing, "strictly" reads like a firm technical claim and I could not verify it either way. -->
