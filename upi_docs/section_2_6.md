# UPI Payment Products & Merchant Onboarding Guide

A complete reference for choosing the right UPI payment product and getting a Cashfree merchant account from signup to go-live.

---

## Product Comparison at a Glance

<div class="upi-product-table" style="overflow-x:auto; border:1px solid #E5E7EB; border-radius:0.5rem; box-shadow:0 1px 2px rgba(0,0,0,0.05); margin:1.5rem 0;">
<style>
.upi-product-table table { width:100%; font-size:14px; text-align:left; border-collapse:collapse; }
.upi-product-table thead th { background:#F4F0FA; color:#5A28A3; font-weight:600; padding:12px 16px; }
.upi-product-table tbody td { padding:12px 16px; border-top:1px solid #E5E7EB; color:#4B5563; }
.upi-product-table tbody tr:hover td { background:#F9FAFB; }
.upi-product-table .badge { display:inline-block; padding:2px 10px; border-radius:9999px; font-size:12px; font-weight:500; }
</style>
<table>
  <thead>
    <tr>
      <th>Product</th>
      <th>Best for</th>
      <th>Integration effort</th>
      <th>Customer action</th>
      <th>Where</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:600;color:#111827;">UPI Intent</td>
      <td>Mobile app/web checkout</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (API)</span></td>
      <td>Tap app → PIN</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">UPI Collect</td>
      <td>Desktop web, known VPA</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (API)</span></td>
      <td>Type VPA → approve in app</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Flash UPI</td>
      <td>High-volume repeat apps</td>
      <td><span class="badge" style="background:#FFFBEB;color:#B45309;">Medium (SDK)</span></td>
      <td>PIN only (no app switch)</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online (in-app)</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Static QR</td>
      <td>Physical stores, no-tech</td>
      <td><span class="badge" style="background:#F0FDF4;color:#15803D;">Zero (print QR)</span></td>
      <td>Scan → type amount → PIN</td>
      <td><span class="badge" style="background:#F3F4F6;color:#374151;">Offline</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Dynamic QR</td>
      <td>Delivery, desktop, invoices</td>
      <td><span class="badge" style="background:#FFFBEB;color:#B45309;">Medium (API)</span></td>
      <td>Scan → PIN (amount pre-filled)</td>
      <td><span class="badge" style="background:#F0FDFA;color:#0F766E;">Offline/Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">SoftPOS</td>
      <td>Field agents, delivery, retail</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (app install)</span></td>
      <td>Scan QR / Tap card / Pay link</td>
      <td><span class="badge" style="background:#F3F4F6;color:#374151;">Offline</span></td>
    </tr>
  </tbody>
</table>
</div>




# Getting Started from Zero: Complete Merchant Onboarding Guide

---

## Step 1 — Sign Up on Cashfree
* Go to [merchant.cashfree.com](https://merchant.cashfree.com) and create an account.
* Provide basic business details (business name, type, PAN, contact info).
* You'll land on the Merchant Dashboard with access to the Test (Sandbox) environment immediately.

---

## Step 2 — Complete KYC
In **Dashboard → Account Settings → KYC**, upload:
* **PAN** (Business or Individual, based on entity type)
* **Bank account details** (IFSC, account number, account holder name)
* **Address proof and business registration documents**

Cashfree performs verification, including a penny test (₹1–2 NEFT to your bank, which must be acknowledged).

> ✅ **Success:** Once KYC is approved, the Payment Gateway is activated for production.

---

## Step 3 — Get API Keys
Go to **Dashboard → Payment Gateway → Developers → API Keys**.
* **Test mode:** Keys are auto-generated.
* **Production mode:** Click **"Generate API Keys"** and complete 2FA.

Store your keys securely:
* `x-client-id: <YOUR_APP_ID>`
* `x-client-secret: <YOUR_SECRET_KEY>`

> ⚠️ **Warning:** Never expose your secret key in client-side code.

---

## Step 4 — Choose Your Integration Path

| If you want… | Do this |
| :--- | :--- |
| **Fastest start, minimal code** | Use Cashfree Checkout (hosted page) |
| **Full control over UI** | Use Seamless/Custom Integration (API) |
| **In-app UPI without redirects** | Integrate the Flash UPI SDK (Android) |
| **Offline/in-person only** | Activate SoftPOS or Static QR |

---

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Integration Guide — Step 5 & Step 6</title>
<style>
  :root {
    --cf-blue: #1259c3;
    --cf-blue-light: #eef4ff;
    --cf-text: #1a1a2e;
    --cf-muted: #5c6474;
    --cf-border: #e3e7ee;
    --cf-code-bg: #f4f6fa;
    --cf-code-text: #b3261e;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    padding: 48px 24px;
    background: #ffffff;
    color: var(--cf-text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.65;
  }

  .doc-wrap {
    max-width: 780px;
    margin: 0 auto;
  }

  .doc-eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 12px;
    font-weight: 700;
    color: var(--cf-blue);
    margin-bottom: 8px;
  }

  h1 {
    font-size: 30px;
    font-weight: 700;
    margin: 0 0 8px;
    color: var(--cf-text);
  }

  h2 {
    font-size: 22px;
    font-weight: 700;
    margin: 48px 0 8px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--cf-border);
    color: var(--cf-text);
  }

  h2 .step-num {
    color: var(--cf-blue);
  }

  p.lead {
    font-size: 16px;
    color: var(--cf-muted);
    margin: 0 0 28px;
  }

  p {
    font-size: 15.5px;
    color: var(--cf-text);
  }

  .intro-note {
    background: var(--cf-blue-light);
    border-left: 3px solid var(--cf-blue);
    padding: 14px 18px;
    border-radius: 6px;
    font-size: 15px;
    color: #26365e;
    margin: 20px 0 28px;
  }

  .path-card {
    border: 1px solid var(--cf-border);
    border-radius: 10px;
    padding: 20px 22px;
    margin: 16px 0;
    background: #fff;
    transition: box-shadow 0.15s ease;
  }

  .path-card:hover {
    box-shadow: 0 4px 16px rgba(18, 89, 195, 0.08);
  }

  .path-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 700;
    margin: 0 0 8px;
    color: var(--cf-text);
  }

  .path-badge {
    background: var(--cf-blue);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.03em;
  }

  .path-card p {
    margin: 0 0 12px;
    color: var(--cf-muted);
    font-size: 14.5px;
  }

  .path-card p:last-child {
    margin-bottom: 0;
  }

  .doc-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 14.5px;
    font-weight: 600;
    color: var(--cf-blue);
    text-decoration: none;
  }

  .doc-link:hover {
    text-decoration: underline;
  }

  .doc-link::after {
    content: "→";
    font-weight: 400;
  }

  code, .inline-code {
    background: var(--cf-code-bg);
    color: var(--cf-code-text);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 13.5px;
  }

  .flag {
    display: inline-block;
    background: #fff4e5;
    color: #9a5b00;
    font-size: 11.5px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
  }

  ul.step-list {
    margin: 0 0 12px;
    padding-left: 20px;
    color: var(--cf-muted);
    font-size: 14.5px;
  }

  ul.step-list li {
    margin-bottom: 4px;
  }

  .also-note {
    font-size: 13.5px;
    color: var(--cf-muted);
    font-style: italic;
    margin-top: -6px;
  }

  hr.divider {
    border: none;
    border-top: 1px solid var(--cf-border);
    margin: 56px 0 40px;
  }
</style>
</head>
<body>
<div class="doc-wrap">

  <div class="doc-eyebrow">Payments · Integration Guide</div>
  <h1>Set up your integration</h1>
  <p class="lead">Follow the paths below based on where you need to accept payments — mobile app, web, in-app UPI, or a fully custom backend.</p>

  <!-- STEP 5 -->
  <h2><span class="step-num">Step 5 —</span> Integrate (Online – Standard PG)</h2>

  <div class="intro-note">
    Instead of manually building payloads, we highly recommend using our official SDKs and API collections to streamline integration. Every online transaction flow follows three core principles:
    <strong>Create an Order</strong> (server-side) → <strong>Process the Payment</strong> (client-side) → <strong>Handle Webhooks</strong> (server-side).
  </div>

  <p>Choose your preferred integration path below for complete, up-to-date documentation and code samples.</p>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 1</span> Mobile App Integration (UPI Intent &amp; SDKs)</p>
    <p>Integrate our native SDKs to offer seamless UPI Intent flows, where users see a list of installed UPI apps and tap to pay directly without leaving your checkout context.</p>
    <a class="doc-link" href="https://www.cashfree.com/docs/payments/online/mobile/android">Android SDK Docs</a>
    <p class="also-note">Also available for iOS, React Native, Flutter, and Cordova.</p>
  </div>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 2</span> Web Checkout (Hosted &amp; Custom) <span class="flag">check link</span></p>
    <p>For web platforms, use our Web Integration to handle UPI Collect (entering a VPA), on-screen dynamic QR codes, or UPI Intent for mobile-web users.</p>
    <a class="doc-link" href="https://www.cashfree.com/docs/payments/overview">Web Checkout Docs</a>
  </div>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 3</span> Flash UPI <span class="flag">check link</span></p>
    <p>For a fully native, in-app UPI payment experience where the user enters their PIN directly inside your app — no app switching — integrate the Flash UPI SDK.</p>
    <a class="doc-link" href="https://www.cashfree.com/docs/payments/manage/payment-methods/upi">UPI Setup Docs</a>
  </div>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 4</span> Core API Reference &amp; Webhooks</p>
    <p>If you're building a custom backend integration, rely on our API reference to manage the <code>/orders</code> endpoint, session generation, and webhook signature verification.</p>
    <a class="doc-link" href="https://www.cashfree.com/docs/api-reference/overview">API Reference</a>
  </div>

  <!-- STEP 6 -->
  <h2><span class="step-num">Step 6 —</span> Activate Offline / QR (If Needed)</h2>

  <p>If your business operates offline — retail storefronts, field agents, or cash-on-delivery alternatives — configure your offline collection methods via the Dashboard or APIs.</p>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 1</span> Static QR</p>
    <p><strong>Setup:</strong></p>
    <ul class="step-list">
      <li>Go to <strong>Dashboard → Payment Gateway → QR Codes → Static QR</strong></li>
      <li>Generate and download the image</li>
      <li>Print it for your physical store display</li>
    </ul>
  </div>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 2</span> Dynamic QR (API)</p>
    <p>Use our Terminal APIs to push a unique QR code or payment link mapped to a specific order ID and amount.</p>
    <p>Review the Terminal &amp; Offline Payments endpoints in the Core API Reference.</p>
  </div>

  <div class="path-card">
    <p class="path-title"><span class="path-badge">Path 3</span> SoftPOS</p>
    <p><strong>Setup:</strong></p>
    <ul class="step-list">
      <li>Go to <strong>Dashboard → SoftPOS → Request Activation</strong></li>
      <li>Once approved, add Storefronts and Agents (requires phone number + KYC verification)</li>
      <li>Agents can download the Cashfree app to collect via generated QR, SMS payment links, or NFC Tap</li>
    </ul>
  </div>

  <hr class="divider">
</div>
</body>
</html>

## Step 7 — Test End-to-End
1. Use Cashfree's Sandbox/Test environment to simulate payments for your chosen method.
2. Test: success, failure, user-dropped, and refunds.
3. Verify webhooks arrive and your system processes them correctly.
4. Verify settlement reports appear in the test dashboard.

---

## Step 8 — Go Live
1. Switch from Test to Production API keys.
2. Ensure KYC is fully approved (v3).
3. Confirm the penny test is ACKNOWLEDGED.
4. Choose your settlement cycle (T+1 / T+2 / Instant).
5. Configure notifications (settlement, refund, dispute alerts).
6. Start processing real transactions.

---

## Go-Live Checklist

- [ ] Cashfree account created and email verified
- [ ] KYC documents uploaded and approved
- [ ] Bank account verified (penny test ACKNOWLEDGED)
- [ ] Production API keys generated and stored securely
- [ ] Webhook endpoints configured and tested
- [ ] Signature verification implemented
- [ ] Integration tested in Sandbox (all chosen methods)
- [ ] Settlement cycle chosen and confirmed
- [ ] Refund and dispute workflows understood
- [ ] SoftPOS activated and Collection points created and verified (if offline needed)
- [ ] Go live — monitor transactions and settlements daily

---

## Support & Resources

| Resource | Details |
| :--- | :--- |
| **Dashboard** | [merchant.cashfree.com](https://merchant.cashfree.com) |
| **API Docs** | Cashfree Developer Documentation |
| **Postman Collections** | Available for quick API testing |
| **Sandbox** | Full test environment with simulated payments |
| **Account Manager** | Contact for custom pricing, Flash UPI activation, or enterprise needs |