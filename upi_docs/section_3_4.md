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
## Step 7  Test End-to-End
1. Use Cashfree's Sandbox/Test environment to simulate payments for your chosen method.
2. Test: success, failure, user-dropped, and refunds.
3. Verify webhooks arrive and your system processes them correctly.
4. Verify settlement reports appear in the test dashboard.

---

## Step 8   Go Live
1. Switch from Test to Production API keys.
2. Ensure KYC is fully approved (v3).
3. Confirm the penny test is ACKNOWLEDGED.
4. Choose your settlement cycle (T+1 / T+2 / Instant).
5. Configure notifications (settlement, refund, dispute alerts).
6. Start processing real transactions.

---

## Go Live Checklist

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