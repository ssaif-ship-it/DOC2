#

Enabling Contextual Payments & Affordability on your checkout, offers flexible payment options, like EMI on UPI, UPI Lite for micro-transactions, and Interoperable PPI Wallets, directly to your customers, reducing cart abandonment and driving higher average order values.

## 1. RuPay Credit Card EMI on UPI

We have enabled real-time EMI options for customers paying via RuPay Credit Cards on standard UPI QR codes and Intent links. By providing instant EMI capabilities natively at checkout, you can drastically lower barriers for high-ticket purchases.

### Key Merchant Benefits

*   **Higher Conversions:** Presenting flexible options directly at checkout can increase checkout conversions by up to 30%.
*   **Increased Ticket Size:** Let customers purchase higher-value items, driving a meaningful increase in Average Order Value (AOV).
*   **Zero Risk:** Upfront settlement guarantees you receive the full transaction amount (less applicable subvention discounts), while the issuing bank bears the repayment risk.

<!-- Claude, confirmed correction for Saif: the 30% figure checks out, it matches Cashfree's own credit-card-EMI page (cashfree.com/credit-card-emi), which states "increase checkout conversions by upto 30" percent, so reworded slightly to match that framing rather than "reduces drop-offs," a different metric. The AOV figure did not check out: this line previously said "40% to 60%," but Cashfree's own public pages disagree with each other and with that range, the credit-card-EMI page says a single "40% higher AOV," while the ScanToEMI blog (cashfree.com/blog/scan-to-emi-instant-no-cost-emi-upi-sales-booster) says "20 to 30% increase in average order value." Since Cashfree's own sources do not agree on a number, I removed the specific range rather than assert one. Whoever owns this feature should pick a single figure and I will restore it. -->

### Current Supported Scope

*   **Supported Banks:** Real-time EMI is currently supported for SBI and HDFC RuPay Credit Cards. <!-- Claude, flagging for Saif, not confirmed: the most recent public reporting I found (Inc42, September 2025) describes EMI on UPI as a network-level feature NPCI was still exploring, not something confirmed live in production with named issuing banks. Cashfree's own ScanToEMI blog post does not name SBI or HDFC either. This may well be accurate from an internal partnership you have that has not been publicly announced, but it needs an internal source before publishing the specific bank names as fact. -->
*   **Supported Flows:** Enabled exclusively for UPI Intent Links and Dynamic QR Codes.
*   **Unsupported Flows:** Contextual EMI is strictly prohibited for UPI Collect requests. Combining flat discounts with EMI offers is not supported at this time.

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

### Reconciliation & Refunds

*   **Purpose Code:** All EMI-converted UPI transactions are tagged with a distinct purpose code across webhooks and settlement reports. <!-- Claude, flagging for Saif, not confirmed: this line previously stated Purpose Code 72 specifically. A comprehensive NPCI purpose code reference I found runs from 00 through 92 with no gaps around 72, it jumps from 71 (UPI Lite AutoPay top-up) straight to 76 (SBMD for securities brokers), so 72 does not appear to be a real, currently assigned code. I removed the specific number rather than publish a wrong one, confirm the correct code internally and I will add it back. -->
*   **Settlement:** Standard payments are settled at the full order amount minus MDR. No-Cost EMI payments are settled at the net principal amount (P) minus standard fees.
*   **Refunds:** On a full refund, the net principal amount (P) is debited from your account, and the issuing bank cancels the customer's EMI schedule via NPCI's Unified Dispute and Issue Resolution (UDIR) framework.

## 4. UPI Lite & Prepaid Wallets (PPI)

To help you accept micro-transactions and alternative funding sources, our checkout fully supports UPI Lite and Interoperable Prepaid Wallets.

### UPI Lite (On-Device Wallet)

UPI Lite is an on-device wallet designed for 1-click, PIN-less payments, up to **₹1,000 per transaction**, with a maximum on-device wallet balance of **₹5,000** at any time.

<!-- Claude, confirmed correction for Saif: the ₹1,000 per-transaction figure and the ₹5,000 wallet balance figure are both correct and current, they match RBI's October 2024 revision (raised from the earlier ₹500 per transaction and ₹2,000 wallet balance). I could not find any public source for the "₹10,000 cumulative per day" figure this line also used to state, no RBI, NPCI, or industry source I checked mentions a separate daily cumulative cap for UPI Lite specifically, so I removed it rather than publish an unconfirmed number. If that cap is real, it needs a source before it goes back in. -->

*   **Seamless Micro-Payments:** Customers experience sub-second transaction speeds without entering a UPI PIN.
*   **Fallback Mechanism:** If the order amount exceeds ₹1,000 or the Lite balance is insufficient, the checkout automatically falls back to standard 2FA UPI requiring a PIN.
*   **No Extra Integration:** Enabled automatically on standard UPI Intent and QR flows.
*   **Not for Mandates:** UPI Lite cannot be used for AutoPay or other UPI Mandate executions, which require the full bank-authenticated flow.

### Prepaid Wallets (Interoperable PPI)

Full-KYC Prepaid Payment Instruments (like Paytm Wallet, Amazon Pay, and PhonePe Wallet) are fully integrated into the UPI ecosystem. Customers can utilize their pre-funded wallet balances to pay at your existing UPI QR codes or Intent links without any explicit onboarding required on your end.

<!-- Claude, confirmed correction for Saif: the Insurance, Mutual Funds & Railways row previously said 1.1%. Checked against NPCI's PPI interchange structure as reported by Business Standard, that category is 1.0%, not 1.1%. Corrected below, all other rows in this table matched the same source. -->

#### Interchange Fees for PPI Wallet Acceptance

Unlike standard savings account UPI transactions, PPI interoperable transactions incur an Interchange Fee paid by the merchant to cover the wallet issuer's infrastructure costs.

| Transaction Category | Transaction Ceiling | Interchange Fee |
| --- | --- | --- |
| Standard Retail & E-Commerce | Up to ₹2,000 | 0.0% (Free) |
| Standard Retail & E-Commerce | \> ₹2,000 | 1.1% |
| Fuel Stations | Any Amount | 0.5% |
| Utilities, Telecom, Post Office, Agriculture & Education | Any Amount | 0.7% |
| Supermarkets | Any Amount | 0.9% |
| Insurance, Mutual Funds & Railways | Any Amount | 1.0% |

### Important PPI Rules

*   **No Consumer Surcharging:** You are strictly prohibited from charging extra convenience fees to customers choosing to check out using PPI wallets.
*   **Automated Source Refunds:** When you issue a refund for a PPI-funded transaction, funds are routed strictly back to the originating wallet ID via the UDIR framework.
