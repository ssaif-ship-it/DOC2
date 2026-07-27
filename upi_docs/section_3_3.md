The UPI ecosystem supports a wide range of funding sources—including Savings/Current Accounts, RuPay Credit Cards, Prepaid Wallets (PPI), and Pre-Sanctioned Credit Lines.

However, because alternative instruments involve Interchange Fees, Merchant Discount Rates (MDR), and specific credit risk guidelines, NPCI and regulatory bodies enforce strict controls on which business categories (MCCs) can accept specific payment methods and which checkout initiation flows (Intent, Dynamic QR, Collect, AutoPay) they are permitted to use.

### 1. Payment Instruments & Funding Sources Overview

**A. Savings & Current Bank Accounts**
*   **Default Acceptance:** Supported across 100% of all MCCs and initiation flows.
*   **Pricing:** Zero MDR for standard P2M transactions under current regulatory directives.

**B. RuPay Credit Cards on UPI**
*   **Default Acceptance:** Permitted for standard retail P2M (Person-to-Merchant) checkouts.
*   **Blocked Categories:** P2P, P2PM (unverified small merchants), Financial Institutions (6012), Capital Markets (6211), Wallet Top-ups (6540), Rent (6513), and Digital Gaming (5816).
*   **Pricing & MDR:** Standard credit card MDR applies according to card network slabs.

**C. Prepaid Payment Instruments (PPI / Wallets)**
*   **Default Acceptance:** Interoperable across standard merchant UPI QR codes and Intent checkouts (e.g., Paytm Wallet, Mobikwik, Amazon Pay).
*   **Interchange Slabs:**
    *   Standard Retail (> ₹2,000): 1.1% interchange fee.
    *   Subsidized Categories (0.5% - 0.7%): Fuel (5541/5542), Utilities (4900), Agriculture, and Educational Services.
    *   Transactions ≤ ₹2,000: Zero interchange fee for retail merchants.

**D. Pre-Sanctioned Credit Lines on UPI**
*   **Default Acceptance:** Permitted for standard retail e-commerce and point-of-sale checkouts.
*   **Pricing & MDR:** Attracts merchant MDR similar to credit cards (typically 1.3% to 2.0%).

### 2. Master MCC Compatibility Matrix

The table below outlines instrument support and allowed checkout initiation flows across primary industry categories:

| Business Category / Industry | Sample MCCs | Bank Acc | RuPay CC | Wallets (PPI) | Credit Lines | Permitted Initiation Flows & Restrictions |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Standard Retail & E-Commerce | 5411, 5311, 5651 | ✅ | ✅ | ✅ | ✅ | Intent, Dynamic QR, AutoPay |
| Restaurants & Dining | 5812, 5814 | ✅ | ✅ | ✅ | ✅ | Intent, Dynamic QR |
| Travel, Airlines & Hotels | 3000-3299, 7011, 4722 | ✅ | ✅ | ✅ | ✅ | Intent, Dynamic QR, OTM/SBMD |
| Utilities & Telecom | 4900, 4814 | ✅ | ✅ | ✅ (0.7% Fee) | ✅ | Intent, Dynamic QR, AutoPay |
| Fuel Stations | 5541, 5542 | ✅ | ✅ | ✅ (0.5% Fee) | ✅ | Dynamic QR, Static QR |
| Education & Schools | 8211, 8220, 8299 | ✅ | ✅ | ✅ (0.7% Fee) | ✅ | Intent, Dynamic QR, Collect |
| Hospitals & Healthcare | 8011, 8062, 8099 | ✅ | ✅ | ✅ | ✅ | Intent, Dynamic QR |
| Capital Markets & Broking | 6211 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent, Dynamic QR, Collect (TPV Mandated; Credit/Wallet Blocked) |
| Financial Services / NBFC | 6012 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent, Dynamic QR, Collect (TPV Mandated; Credit/Wallet Blocked) |
| Digital Gaming & Casinos | 5816, 7995 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent Only (Collect & QR Flows Strictly Blocked) |
| Wallet Loading | 6540 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent Only (Collect & QR Flows Strictly Blocked) |
| Rent Payments | 6513 | ✅ | ❌ Blocked | ✅ | ❌ Blocked | Intent, Dynamic QR (Collect Blocked) |
| Credit Card Bill Payments | 5413 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent, Dynamic QR (Collect Strictly Blocked) |
| Digital Gold Purchases | 5412 | ✅ | ❌ Blocked | ❌ Blocked | ❌ Blocked | Intent, Dynamic QR (Collect Strictly Blocked) |
| Tax & Government Services | 9311, 9399 | ✅ | ✅ | ✅ | ✅ | Intent, Dynamic QR |
| Unverified Small Merchants | P2PM | ✅ | ❌ Blocked | ✅ | ❌ Blocked | QR Scan, Intent (Collect capped at ₹2,000) |

### 3. Category Guardrails & Routing Restrictions

**A. Flow Blocks & Sunset Enforcement**
To mitigate spam and fraud, NPCI systematically blocks Collect ("pull") requests for high-risk categories:
*   **Strict Collect Blocks:** Digital Gaming (5816), Wallet Loads (6540), Rent (6513), Digital Gold (5412), and Credit Card Bill Payments (5413) are strictly blocked for Collect requests. Attempting to trigger a Collect call for these MCCs will result in an immediate technical rejection (Collect Blocked for MCC).
*   **QR & Collect Blocks:** Gaming (5816) and Wallet Loading (6540) are restricted exclusively to Payer-Initiated Intent flows.

**B. Mandatory Third-Party Verification (TPV)**
For Capital Markets (6211) and Financial Services (6012):
*   Transactions must originate strictly from bank accounts pre-verified against the customer's trading/investment account.
*   Credit Cards, Wallets, and Credit Lines are completely blocked to comply with SEBI and RBI regulations prohibiting leveraged funds in securities trading.

**C. Compliance & Auditing**
*   **MCC Misclassification Auditing:** Merchants must not route restricted transactions (such as gaming deposits or stock investments) under standard retail MCCs (5411). NPCI automated pattern detection monitors routing behaviors and suspends terminals violating classification rules.
*   **Surcharging Prohibited:** Merchants are prohibited from adding a surcharge to pass on the MDR of RuPay Credit Cards or Credit Lines to end consumers during standard UPI checkout.