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

# Set up your integration

Follow the paths below based on where you need to accept payments — mobile app, web, in-app UPI, or a fully custom backend.

---

## Step 5 — Integrate (Online – Standard PG)

> Instead of manually building payloads, we highly recommend using our official SDKs and API collections to streamline integration. Every online transaction flow follows three core principles: **Create an Order** (server-side) → **Process the Payment** (client-side) → **Handle Webhooks** (server-side).

Choose your preferred integration path below for complete, up-to-date documentation and code samples.

### Path 1: Mobile App Integration

Native SDKs for Android, iOS, React Native, Flutter, and Cordova.

### Intent
Users see a list of installed UPI apps and tap to pay directly, without leaving your checkout context.

- [Android SDK Docs](https://www.cashfree.com/docs/payments/online/mobile/android)
- *Also available for iOS, React Native, Flutter, and Cordova.*

### Path 2: Web Checkout (Hosted & Custom) 

Handles multiple UPI methods depending on device — desktop or mobile web.

### Collect
User manually enters their VPA (UPI ID) on the checkout page.

### QR
A dynamic QR code is rendered on-screen for the user to scan and pay.

### Intent
On mobile-web, the user is redirected to their preferred UPI app to complete payment.

- [Web Checkout Docs](https://www.cashfree.com/docs/payments/overview)

### Path 3: Flash UPI 

Fully native, in-app UPI experience — no switching to a separate app.

### PIN
The user enters their UPI PIN directly inside your app to authorize the payment.

- [UPI Setup Docs](https://www.cashfree.com/docs/payments/manage/payment-methods/upi)

### Path 4: Core API Reference & Webhooks

For a fully custom backend integration.

### Custom
Manage the `/orders` endpoint, session generation, and webhook signature verification directly.

- [API Reference](https://www.cashfree.com/docs/api-reference/overview)

---

## Step 6 — Activate Offline / QR (If Needed)

If your business operates offline — retail storefronts, field agents, or cash-on-delivery alternatives — configure your offline collection methods via the Dashboard or APIs.

### Path 1: Static QR

#### Setup
1. Go to **Dashboard → Payment Gateway → QR Codes → Static QR**
2. Generate and download the image
3. Print it for your physical store display

### Path 2: Dynamic QR (API)

### QR
Use our Terminal APIs to push a unique QR code or payment link mapped to a specific order ID and amount.

*Review the Terminal & Offline Payments endpoints in the Core API Reference.*

### Path 3: SoftPOS

#### Setup
1. Go to **Dashboard → SoftPOS → Request Activation**
2. Once approved, add Storefronts and Agents (requires phone number + KYC verification)
3. Agents can download the Cashfree app to collect via generated QR, SMS payment links, or NFC Tap

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