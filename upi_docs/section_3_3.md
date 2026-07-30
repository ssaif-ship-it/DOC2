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

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>UPI Merchant Category & Instrument Eligibility Matrix</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f7f7f8;
    color: #1a1a1a;
    padding: 32px;
  }
  h1 {
    font-size: 20px;
    margin-bottom: 16px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    background: #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    font-size: 13.5px;
  }
  th, td {
    border: 1px solid #e0e0e0;
    padding: 10px 12px;
    text-align: left;
    vertical-align: top;
  }
  th {
    background: #1a1a1a;
    color: #fff;
    font-weight: 600;
    white-space: nowrap;
  }
  td.center {
    text-align: center;
  }
  tr:nth-child(even) {
    background: #fafafa;
  }
  tr:hover {
    background: #f0f4ff;
  }
  code {
    background: #eef0f3;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 12.5px;
    white-space: nowrap;
  }
  .yes {
    color: #1a7f37;
    font-weight: 600;
  }
  .no {
    color: #c62828;
    font-weight: 600;
  }
  .fee {
    color: #b26a00;
    font-weight: 500;
    font-size: 12px;
  }
</style>
</head>
<body>

<h1>UPI Merchant Category & Instrument Eligibility Matrix</h1>

<table>
  <thead>
    <tr>
      <th>Business Category / Industry</th>
      <th>Sample MCCs</th>
      <th>Bank Acc</th>
      <th>RuPay CC</th>
      <th>Wallets (PPI)</th>
      <th>Credit Lines</th>
      <th>Permitted Initiation Flows & Restrictions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Standard Retail & E-Commerce</td>
      <td><code>5411</code>, <code>5311</code>, <code>5651</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR, AutoPay</td>
    </tr>
    <tr>
      <td>Restaurants & Dining</td>
      <td><code>5812</code>, <code>5814</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR</td>
    </tr>
    <tr>
      <td>Travel, Airlines & Hotels</td>
      <td><code>3000–3299</code>, <code>7011</code>, <code>4722</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR, OTM/SBMD</td>
    </tr>
    <tr>
      <td>Utilities & Telecom</td>
      <td><code>4900</code>, <code>4814</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅ <span class="fee">(0.7% fee)</span></td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR, AutoPay</td>
    </tr>
    <tr>
      <td>Fuel Stations</td>
      <td><code>5541</code>, <code>5542</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅ <span class="fee">(0.5% fee)</span></td>
      <td class="center yes">✅</td>
      <td>Dynamic QR, Static QR</td>
    </tr>
    <tr>
      <td>Education & Schools</td>
      <td><code>8211</code>, <code>8220</code>, <code>8299</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅ <span class="fee">(0.7% fee)</span></td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR, Collect</td>
    </tr>
    <tr>
      <td>Hospitals & Healthcare</td>
      <td><code>8011</code>, <code>8062</code>, <code>8099</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR</td>
    </tr>
    <tr>
      <td>Capital Markets & Broking</td>
      <td><code>6211</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent, Dynamic QR, Collect — TPV mandated; credit/wallet blocked</td>
    </tr>
    <tr>
      <td>Financial Services / NBFC</td>
      <td><code>6012</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent, Dynamic QR, Collect — TPV mandated; credit/wallet blocked</td>
    </tr>
    <tr>
      <td>Digital Gaming & Casinos</td>
      <td><code>5816</code>, <code>7995</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent only — Collect & QR flows strictly blocked</td>
    </tr>
    <tr>
      <td>Wallet Loading</td>
      <td><code>6540</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent only — Collect & QR flows strictly blocked</td>
    </tr>
    <tr>
      <td>Rent Payments</td>
      <td><code>6513</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent, Dynamic QR — Collect blocked</td>
    </tr>
    <tr>
      <td>Credit Card Bill Payments</td>
      <td><code>5413</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent, Dynamic QR — Collect strictly blocked</td>
    </tr>
    <tr>
      <td>Digital Gold Purchases</td>
      <td><code>5412</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td class="center no">❌ Blocked</td>
      <td>Intent, Dynamic QR — Collect strictly blocked</td>
    </tr>
    <tr>
      <td>Tax & Government Services</td>
      <td><code>9311</code>, <code>9399</code></td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td class="center yes">✅</td>
      <td>Intent, Dynamic QR</td>
    </tr>
    <tr>
      <td>Unverified Small Merchants</td>
      <td><code>P2PM</code></td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td class="center yes">✅</td>
      <td class="center no">❌ Blocked</td>
      <td>QR Scan, Intent — Collect capped at ₹2,000</td>
    </tr>
  </tbody>
</table>

</body>
</html>

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