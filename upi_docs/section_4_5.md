
Welcome to the Cashfree Payments Merchant Integration Guide for UPI Lite and Interoperable PPI Wallets.

By integrating Cashfree Payments for UPI checkout (via Dynamic QR, Intent, or POS), your business automatically supports these two advanced payment features with zero additional code changes. This document outlines the operational mechanics, regulatory limits, merchant economics, and post-transaction lifecycles.

## 1. Executive Summary

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>UPI Lite</th>
      <th>Interoperable PPI Wallets</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Target Use Case</td>
      <td>High-frequency, low-value payments</td>
      <td>High-value payments using stored digital wallet funds</td>
    </tr>
    <tr>
      <td>Max Transaction Limit</td>
      <td>₹200 per payment (PIN-less)</td>
      <td>Up to customer's available wallet balance</td>
    </tr>
    <tr>
      <td>Max Stored Balance</td>
      <td>₹2,000</td>
      <td>Up to ₹2,00,000 (₹2 Lakhs) for Full-KYC</td>
    </tr>
    <tr>
      <td>Authentication</td>
      <td>1-Click (No UPI PIN required)</td>
      <td>Wallet PIN, Biometric, or 2FA (depending on issuer)</td>
    </tr>
    <tr>
      <td>Merchant Cost (MDR)</td>
      <td>0% (Standard UPI rates apply)</td>
      <td>0% for ≤ ₹2,000; 1.1% for &gt; ₹2,000 (Standard Retail)</td>
    </tr>
    <tr>
      <td>Integration Effort</td>
      <td>Natively supported out of the box</td>
      <td>Natively supported out of the box</td>
    </tr>
  </tbody>
</table>

## 2. UPI Lite: On-Device PIN-Less Payments

### 2.1 What is UPI Lite?

Designed by NPCI, UPI Lite is an on-device wallet that stores balances directly inside a secure local container (Common Library) on the customer's smartphone. By handling low-value transactions locally, UPI Lite bypasses core banking system (CBS) overhead, resulting in higher payment success rates and instantaneous checkouts.

```
[Customer Scans Cashfree QR / Clicks Intent]
                      │
                      ▼
        [Check Amount ≤ ₹200 & Wallet Bal]
                      │
            ┌─────────┴─────────┐
            │                   │
      (Success Conditions)  (Exceeds Limit / Insufficient)
            │                   │
            ▼                   ▼
    [1-Click PIN-Less Pay]  [Fallback to Standard 2FA UPI PIN]
            │                   │
            └─────────┬─────────┘
                      │
                      ▼
         [Instant Settlement Signal]
```

### 2.2 Core Business Benefits

- **Faster Checkout Speeds:** Transactions under ₹200 require no 4-digit or 6-digit UPI PIN, significantly cutting payment processing times.
- **Higher Approval Rates:** Because the bank's core servers are not queried during execution, payment failure rates due to bank downtime or network congestion are nearly eliminated.
- **Seamless Automated Fallback:** If an order total exceeds ₹200 or the customer's Lite balance is insufficient, Cashfree automatically shifts the checkout flow to standard 2-Factor Authentication (2FA) UPI without dropping the transaction session.

### 2.3 Customer Eligibility & Limits

- **Maximum Wallet Balance:** Capped at ₹2,000 max stored value.
- **Top-Up Limits:** Minimum top-up is ₹1, up to the ₹2,000 threshold (preset options: ₹500, ₹1,000, ₹2,000).
- **Single Active Account:** A customer can maintain only one active UPI Lite wallet across all Payment Service Provider (PSP) apps at a time.
- **Device Integrity Enforcement:** Activation is strictly blocked on rooted or jailbroken devices.

### 2.4 Technical & Architecture Flow (PSP Level)

1. **Registration & Key Generation:** The customer app invokes the Common Library (CL) on the device to generate a cryptographic key pair. The PSP calls `ReqListKeys` (type="GetLite") to NPCI, which returns a LITE Reference Number (LRN).
2. **Top-Up Execution:** Top-ups use `ReqPay` with Purpose Code 41 (Enablement + Add Money) or Purpose Code 71 (AutoPay replenishment). An Authentication Response Cryptogram (ARPC) updates the on-device balance.
3. **Daily Statements:** Issuing banks send a single consolidated daily SMS summary of UPI Lite debits rather than triggering an SMS per transaction, reducing SMS notification clutter.

### 2.5 Edge Cases & Background Sync

- **Timeout Handling:** If a network failure occurs after a top-up or transaction before the ARPC cryptogram reaches the device, a mandatory 3-minute cooling-off period is enforced before triggering a background sync (capped at 3 attempts/day).
- **Transaction Lock:** New UPI Lite payments are paused on the device until background synchronization completes. If all attempts fail, the app falls back to standard 2FA UPI.
- **Device Replacement:** Moving to a new phone requires explicit de-registration (Purpose Code 43) on the old device to credit residual funds back to the linked bank account before setting up a new LRN.

## 3. PPI Wallets on UPI (PhonePe, Paytm, Mobikwik, Amazon Pay)

### 3.1 Interoperability Overview

Under NPCI directives, Prepaid Payment Instruments (PPI)—such as PhonePe Wallet, Paytm Wallet, Mobikwik, and Amazon Pay—are fully interoperable across the UPI ecosystem.

Customers who hold balances in their preferred wallet can spend those funds at any merchant displaying a Cashfree UPI QR code, POS terminal, or online checkout.

> **Key Rule:** Merchants accepting UPI through Cashfree accept interoperable PPI wallets by default. No separate contract or technical integration is required for individual wallet providers.

### 3.2 Full-KYC Wallet Capability & Capacity Limits

To ensure financial regulatory compliance while supporting high Average Order Values (AOV), RBI dictates two distinct wallet tiers.

**KYC Tier Breakdown**

<table>
  <thead>
    <tr>
      <th>Wallet Parameter</th>
      <th>Min-KYC Wallet (Small PPI)</th>
      <th>Full-KYC Wallet (Upgraded PPI)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Max Balance Limit</td>
      <td>₹10,000</td>
      <td>₹2,00,000 (₹2 Lakhs)</td>
    </tr>
    <tr>
      <td>Monthly Loading Cap</td>
      <td>₹10,000 maximum per month</td>
      <td>No monthly cap</td>
    </tr>
    <tr>
      <td>UPI Network Interoperability</td>
      <td>❌ Blocked on cross-network UPI</td>
      <td>✅ Fully Enabled on Cashfree UPI Checkouts</td>
    </tr>
    <tr>
      <td>Validity</td>
      <td>Max 24 months (Requires KYC conversion)</td>
      <td>Unlimited</td>
    </tr>
  </tbody>
</table>

```
[Min-KYC User (Cap ₹10,000)]  ──► Restricted to In-App Wallet Purchases

[Full-KYC User (Cap ₹2 Lakhs)] ──► Fully Interoperable across Cashfree UPI QRs & Checkout
```

**Impact for High-AOV Merchants:** Because Full-KYC PhonePe and PPI wallet limits expand up to ₹2,00,000 (₹2 Lakhs), customers can seamlessly complete high-value transactions (electronics, ticketing, jewelery, SaaS, e-commerce) using their wallet balance over the UPI network.

### 3.3 Wallet Loading & Funding Restrictions (MCC 6540)

To prevent unauthorized credit extractions and regulatory arbitrage, loading money into a PPI wallet via UPI is governed by strict rules:

- **MCC Tagging:** All top-up transactions are tagged under MCC 6540 (POI Funding Transactions / Wallet Load).
- **Credit Restrictions:** Loading wallets using RuPay Credit Cards on UPI or Pre-Sanctioned Credit Lines is systematically blocked by the NPCI switch.
- **Permitted Sources:** Top-ups under MCC 6540 can only be funded using Savings Accounts, Current Accounts, or Overdraft (OD) Accounts via Payer-Initiated Intent flows. Dynamic QR and Collect requests are disabled for wallet loads.

### 3.4 Merchant Economics & Interchange Fee Structure

Standard UPI payments from savings accounts carry a 0% Merchant Discount Rate (MDR). However, interoperable transactions funded via PPI Wallets incur an Interchange Fee paid to the wallet issuer.

**NPCI Interchange Fee Slabs for PPI Transactions**

<table>
  <thead>
    <tr>
      <th>Category / Sector</th>
      <th>MCC Scope</th>
      <th>Order Amount</th>
      <th>Applicable Interchange Fee</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard Retail &amp; E-Commerce</td>
      <td>5411, 5311, 5651, etc.</td>
      <td>≤ ₹2,000</td>
      <td>0.0% (Free)</td>
    </tr>
    <tr>
      <td>Standard Retail &amp; E-Commerce</td>
      <td>Standard Merchant MCCs</td>
      <td>&gt; ₹2,000</td>
      <td>1.1%</td>
    </tr>
    <tr>
      <td>Fuel Stations</td>
      <td>5541, 5542</td>
      <td>Any Amount</td>
      <td>0.5%</td>
    </tr>
    <tr>
      <td>Utilities &amp; Telecom</td>
      <td>4900, 4814</td>
      <td>Any Amount</td>
      <td>0.7%</td>
    </tr>
    <tr>
      <td>Educational Services</td>
      <td>8211, 8220, 8299</td>
      <td>Any Amount</td>
      <td>0.7%</td>
    </tr>
    <tr>
      <td>Agriculture &amp; Mutual Funds</td>
      <td>0742, 6211 (select)</td>
      <td>Any Amount</td>
      <td>0.7%</td>
    </tr>
  </tbody>
</table>

**Compliance Rules for Merchants**

- **No Surcharging:** Merchants are strictly prohibited from passing interchange fees onto the end customer or applying convenience surcharges for selecting PPI Wallet checkout options.
- **Commercial Merchants Only (P2M):** Interoperable wallet payments are limited to verified commercial merchants. Peer-to-Peer (P2P) and unverified micro-merchant (P2PM) wallet transfers are blocked at the network level.

## 4. Post-Transaction Lifecycle & Operations

### 4.1 Automated Source Refunds

All refunds initiated via the Cashfree Merchant Dashboard or Refund API are dynamically processed back to the exact payment source:

- **UPI Lite Purchases:** Refunds credit back directly to the primary linked bank account.
- **PPI Wallet Purchases:** Refunds route directly back to the original PPI Wallet handle (e.g., PhonePe Wallet ID).
- **Handling Wallet Holding Overflow:** If a refund causes the customer's wallet balance to exceed their monthly statutory holding ceiling, the wallet issuer places the excess funds into a staging ledger and notifies the user to upgrade their KYC or clear existing balances per RBI directives.

### 4.2 Partial Withdrawal (UPI Lite)

Customers holding funds in a UPI Lite wallet can return partial stored balances to their primary bank account at any time using Purpose Code 46 (CREDIT flow). This action requires no UPI PIN verification because funds are returning to the verified source account.

### 4.3 Unified Dispute & Issue Resolution (UDIR)

Both UPI Lite and PPI Wallet payments are deeply integrated into NPCI's UDIR framework. Turnaround times (TAT) for chargeback resolutions, pending status validations, and auto-reversals are automated through Cashfree's dispute management pipeline.

## 5. Integration Checklist for Cashfree Merchants

- [x] **No Code Changes Required:** Existing Cashfree Payment Gateway (PG), Dynamic QR, and Intent integrations accept UPI Lite and PPI Wallets by default.
- [x] **Update Checkout Terms:** Ensure no additional surcharges are configured for customers paying via PPI Wallets.
- [x] **Accounting & Settlement Preparedness:** Ensure your financial reconciliation systems account for standard 1.1% interchange pricing on standard e-commerce orders > ₹2,000 funded via PPI Wallets.
- [x] **Refund Flow Readiness:** Standard Cashfree Refund APIs support automatic routing to both UPI Lite primary bank accounts and Full-KYC PhonePe/PPI Wallets.