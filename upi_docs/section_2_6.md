# Affordability & Contextual Payments on UPI

Welcome to the comprehensive guide for enabling Contextual Payments & Affordability on your checkout. This suite empowers you to offer flexible payment options—like EMI on UPI, UPI Lite for micro-transactions, and Interoperable PPI Wallets—directly to your customers, reducing cart abandonment and driving higher average order values.

## 1. RuPay Credit Card EMI on UPI

We have enabled real-time EMI options for customers paying via RuPay Credit Cards on standard UPI QR codes and Intent links. By providing instant EMI capabilities natively at checkout, you can drastically lower barriers for high-ticket purchases.

### Key Merchant Benefits

- **Higher Conversions:** Presenting flexible options directly at checkout reduces customer drop-offs by up to 30%.
- **Increased Ticket Size:** Empower customers to purchase higher-value items, driving a 40% to 60% increase in Average Order Value (AOV).
- **Zero Risk:** Upfront settlement guarantees you receive the full transaction amount (less applicable subvention discounts), while the issuing bank bears the repayment risk.

### Current Supported Scope

- **Supported Banks:** Real-time EMI is currently supported for SBI and HDFC RuPay Credit Cards.
- **Supported Flows:** Enabled exclusively for UPI Intent Links and Dynamic QR Codes.
- **Unsupported Flows:** Contextual EMI is strictly prohibited for UPI Collect requests. Combining flat discounts with EMI offers is not supported at this time.

## 2. EMI Subvention & Affordability Engine

You can configure both No-Cost EMI and Low-Cost EMI structures via the Merchant Dashboard or API.

In a No-Cost EMI model, the customer pays only the product sticker price, split equally over the selected months. You, as the merchant, absorb the interest by offering an upfront discount equivalent to the total interest charged by the bank.

### Mathematical Amortization Model

The monthly installment ($EMI$) paid by the customer is calculated using the standard amortized equation:

$$
EMI = \frac{P \times R \times (1+R)^N}{(1+R)^N - 1}
$$

Where:

- $A$ = Order Amount / Product Sticker Price (total paid by customer)
- $P$ = Adjusted Base Principal (settled upfront to merchant)
- $R$ = Monthly Interest Rate charged by issuing bank (Annual Rate / 12 / 100)
- $N$ = Repayment Tenure in months
- $EMI$ = Monthly Installment Amount, where $EMI = \frac{A}{N}$ for No-Cost EMI

To determine the net Principal amount ($P$) settled to you:

$$
P = \frac{EMI \times [(1+R)^N - 1]}{R \times (1+R)^N}
$$

### Standard Calculation Example (3-Month No-Cost EMI at 16% p.a.)

| Parameter | Value | Description |
|---|---|---|
| Order Amount ($A$) | ₹10,000 | Total amount paid by customer over $N$ months |
| Tenure ($N$) | 3 Months | Chosen repayment duration |
| Bank Interest Rate | 16% p.a. | Bank's credit card interest rate |
| Monthly EMI | ₹3,333 | Fixed monthly amount paid by customer |
| Adjusted Principal ($P$) | ₹9,739 | Calculated base amount |
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

- **Purpose Code:** All EMI-converted UPI transactions are tagged with Purpose Code 72 across webhooks and settlement reports.
- **Settlement:** Standard payments are settled at the full order amount minus MDR. No-Cost EMI payments are settled at the net principal amount ($P$) minus standard fees.
- **Refunds:** On a full refund, the net principal amount ($P$) is debited from your account, and the issuing bank cancels the customer's EMI schedule via NPCI's Unified Dispute and Issue Resolution (UDIR) framework.

## 4. UPI Lite & Prepaid Wallets (PPI)

To help you seamlessly accept micro-transactions and alternative funding sources, our checkout fully supports UPI Lite and Interoperable Prepaid Wallets.

### UPI Lite (On-Device Wallet)

UPI Lite is an on-device wallet designed for 1-click, PIN-less payments for amounts up to ₹200.

- **Seamless Micro-Payments:** Customers experience sub-second transaction speeds without entering a UPI PIN.
- **Fallback Mechanism:** If the order amount exceeds ₹200 or the Lite balance is insufficient, the checkout automatically falls back to standard 2FA UPI requiring a PIN.
- **No Extra Integration:** Enabled automatically on standard UPI Intent and QR flows.

### Prepaid Wallets (Interoperable PPI)

Full-KYC Prepaid Payment Instruments (like Paytm Wallet, Amazon Pay, and PhonePe Wallet) are fully integrated into the UPI ecosystem. Customers can utilize their pre-funded wallet balances to pay at your existing UPI QR codes or Intent links without any explicit onboarding required on your end.

#### Interchange Fees for PPI Wallet Acceptance

Unlike standard savings account UPI transactions, PPI interoperable transactions incur an Interchange Fee paid by the merchant to cover the wallet issuer's infrastructure costs.

| Transaction Category | Transaction Ceiling | Interchange Fee |
|---|---|---|
| Standard Retail & E-Commerce | ≤ ₹2,000 | 0.0% (Free) |
| Standard Retail & E-Commerce | > ₹2,000 | 1.1% |
| Fuel Stations | Any Amount | 0.5% |
| Utilities & Telecom | Any Amount | 0.7% |
| Educational Services | Any Amount | 0.7% |
| Agriculture & Mutual Funds | Any Amount | 0.7% |

### Important PPI Rules

- **No Consumer Surcharging:** You are strictly prohibited from charging extra convenience fees to customers choosing to check out using PPI wallets.
- **Automated Source Refunds:** When you issue a refund for a PPI-funded transaction, funds are routed strictly back to the originating wallet ID via the UDIR framework.