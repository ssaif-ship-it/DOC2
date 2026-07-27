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
## Getting Started from Zero, Complete Merchant Onboarding Guide

### Step 1 — Sign Up on Cashfree

1. Go to [merchant.cashfree.com](https://merchant.cashfree.com) and create an account.
2. Provide basic business details (business name, type, PAN, contact info).
3. You'll land on the **Merchant Dashboard** with access to the Test (Sandbox) environment immediately.

### Step 2 — Complete KYC

In **Dashboard → Account Settings → KYC**, upload:

- PAN (Business or Individual, based on entity type)
- Bank account details (IFSC, account number, account holder name)
- Address proof and business registration documents

Cashfree performs verification, including a **penny test** (₹1–2 NEFT to your bank, which must be acknowledged).

> ✅ Once KYC is approved, the Payment Gateway is activated for production.

### Step 3 — Get API Keys

**Dashboard → Payment Gateway → Developers → API Keys**

- **Test mode:** keys are auto-generated.
- **Production mode:** click **"Generate API Keys"** and complete 2FA.

Store your keys securely:

```bash
x-client-id: <YOUR_APP_ID>
x-client-secret: <YOUR_SECRET_KEY>
```

> ⚠️ **Never expose your secret key in client-side code.**

### Step 4 — Choose Your Integration Path

| If you want… | Do this |
| :--- | :--- |
| Fastest start, minimal code | Use **Cashfree Checkout** (hosted page) — create an order via API and redirect the customer |
| Full control over UI | Use **Seamless/Custom Integration** — call the Order Pay API with specific payment methods |
| Offline/in-person only | Activate **SoftPOS** — no coding required |
| In-app UPI without redirects | Integrate the **Flash UPI SDK** in your Android app |

### Step 5 — Integrate (Online – Standard PG)

**a) Create Order API**

```http
POST /orders
Headers: x-client-id, x-client-secret
Body: {
  order_amount,
  order_currency: "INR",
  customer_details: {...},
  order_meta: { return_url: "..." }
}
```

Returns a `payment_session_id` (for Cashfree Checkout) or `order_token`.

**b) Accept Payment**

- **Cashfree Checkout:** Use `payment_session_id` to load Cashfree's hosted page. All methods (UPI Intent, Collect, Cards, NB, Wallets) are shown automatically.
- **Custom/Seamless:** Call the Order Pay API with a specific payment method:

  ```json
  // UPI Intent
  { "payment_method": { "upi": { "channel": "link" } } }

  // UPI Collect
  { "payment_method": { "upi": { "channel": "collect", "upi_id": "customer@upi" } } }
  ```

**c) Handle Response**

- Configure webhooks (**Dashboard → Developers → Webhooks**) for: Payment Success, Payment Failed, Refund events.
- Implement signature verification on incoming webhooks.
- Use the **Get Order Status API** as a fallback check.

### Step 6 — Activate Offline/SoftPOS (If Needed)

1. **Dashboard → SoftPOS →** click **"Request Activation."**
2. Once approved:
   - Add **Storefronts** (upload address proof, store images).
   - Add **Agents** (phone number + Aadhaar KYC).
   - Agents download the SoftPOS app and start collecting.
3. For Dynamic QR via API, use the **Create Terminal Transaction API** with your terminal ID.

### Step 7 — Test End-to-End

- Use Cashfree's Sandbox/Test environment to simulate payments.
- Test: success, failure, user-dropped, and refunds.
- Verify webhooks arrive and your system processes them correctly.
- Verify settlement reports in the dashboard.

### Step 8 — Go Live

1. Switch from Test to Production API keys.
2. Ensure KYC is fully approved (v3).
3. Confirm the penny test is **ACKNOWLEDGED**.
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
- [ ] Integration tested in Sandbox (all methods)
- [ ] Settlement cycle chosen and confirmed
- [ ] Refund and dispute workflows understood
- [ ] SoftPOS activated (if offline needed)
- [ ] Collection points created and verified (if offline)
- [ ] Go live — monitor transactions and settlements daily

---

## Support & Resources

| Resource | Details |
| :--- | :--- |
| **Dashboard** | [merchant.cashfree.com](https://merchant.cashfree.com) |
| **API Docs** | Cashfree Developer Documentation |
| **Postman Collections** | Available for quick API testing |
| **Sandbox** | Full test environment with simulated payments |
| **Account Manager** | Contact for custom pricing, Flash UPI, or enterprise needs |
