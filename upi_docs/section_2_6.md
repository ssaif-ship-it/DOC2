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

## Step 5 — Integrate (Online – Standard PG)

### a) Create Order API (Applies to all online methods)
Create an order to generate a session ID.

* **Endpoint:** `POST /orders`
* **Headers:** `x-client-id`, `x-client-secret`, `x-api-version: 2023-08-01`
* **Body:**

```json
{
  "order_amount": 500.00,
  "order_currency": "INR",
  "customer_details": {
    "customer_id": "cust_001",
    "customer_phone": "9999999999"
  },
  "order_meta": {
    "return_url": "https://yoursite.com/payment-result?order_id={order_id}"
  }
}
```

* **Returns:** `payment_session_id` (and `order_id`).

---

### b) Accept Payment (Choose your specific method below)

#### Path 1: Cashfree Checkout (Hosted)
Use the `payment_session_id` to load Cashfree's hosted page. All enabled methods (UPI Intent, Collect, Cards, Wallets) are shown automatically.

#### Path 2: UPI Intent (Custom UI)
Call `POST /orders/sessions` to get a deep-link:

```json
{
  "payment_session_id": "<id>",
  "payment_method": {
    "upi": {
      "channel": "link"
    }
  }
}
```
* **Action:** Extract the `upi://` URL from `data.payload.default` and launch it on the user's device (e.g., via Android Intent).

#### Path 3: UPI Collect (Custom UI)
Call `POST /orders/sessions` targeting the user's specific UPI ID:

```json
{
  "payment_session_id": "<id>",
  "payment_method": {
    "upi": {
      "channel": "collect",
      "upi_id": "customer@okaxis"
    }
  }
}
```
* **Action:** Show a "waiting for approval" spinner (5-minute timeout window).

#### Path 4: Flash UPI (Android SDK)
1. Request activation via Account Manager to get a dedicated handle.
2. Add dependencies: `com.cashfree.pg:api:x.x.x` and `com.cashfree.pg:upi:x.x.x`.
3. Initialize and trigger:

```java
CFSession cfSession = new CFSession.CFSessionBuilder()
        .setEnvironment(CFSession.Environment.PRODUCTION)
        .setPaymentSessionId(paymentSessionId)
        .setOrderId(orderId)
        .build();

CFUPIIntentCheckoutPayment cfUPIPayment = new CFUPIIntentCheckoutPayment.CFUPIIntentCheckoutPaymentBuilder()
        .setSession(cfSession)
        .build();

CFPaymentGatewayService.getInstance().doPayment(activity, cfUPIPayment);
```

---

### c) Handle Response (Applies to all online methods)
1. Configure Webhooks in **Dashboard → Developers → Webhooks** (Payment Success, Payment Failed, Refund events).
2. Implement signature verification on incoming webhooks.
3. Use `GET /orders/{order_id}` as a fallback to check status (especially critical for polling UPI Collect).

---

## Step 6 — Activate Offline/QR (If Needed)
Choose your offline flow based on your operational setup:

### Path 1: Static QR
* **Setup:** Go to **Dashboard → Payment Gateway → QR Codes → Static QR**. Generate and download the image. Print for display.
* **Tracking:** Reconcile via `GET /settlements/transactions?start_date=...&end_date=...` matching amount + timestamp + payer VPA.

#### Path 2: Dynamic QR (API)
* **Setup:** Create a terminal one-time via `POST /terminal`:

```json
{
  "terminal_id": "store_counter_1",
  "terminal_name": "Main Counter",
  "terminal_type": "QRCODE",
  "terminal_phone_no": "9999999999"
}
```

* **Trigger:** Generate a unique QR per order via `POST /terminal/transactions`:

```json
{
  "cf_terminal_id": "store_counter_1",
  "order_id": "order_20240101_001",
  "order_amount": 750.00,
  "order_currency": "INR",
  "payment_method": "QR_CODE",
  "customer_details": {
    "customer_id": "cust_001",
    "customer_phone": "9999999999"
  }
}
```

* **Action:** Display the returned base64 image or URL. Handle expiry and webhooks.

### Path 3: SoftPOS
* **Setup:** Go to **Dashboard → SoftPOS → Request Activation**.
* Once approved, add **Storefronts** (upload address proof, store images).
* Add **Agents** (requires phone number + KYC verification).
* **Action:** Agents download the app and collect via generated QR, SMS payment links, or NFC Tap.
* *(Optional)* Push a dynamic amount straight to the agent's app via API: `POST /terminal/transactions` using `"payment_method": "UPI_QR"`.

---

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