# UPI Payment Products & Merchant Onboarding Guide

A complete reference for choosing the right UPI payment product and getting a Cashfree merchant account from signup to go-live.

---

## Product Comparison at a Glance

| Product | Best For | Integration Effort | Customer Action | Where |
| :--- | :--- | :--- | :--- | :--- |
| **UPI Intent** | Mobile app/web checkout | Low (API) | Tap app → PIN | Online |
| **UPI Collect** | Desktop web, known VPA | Low (API) | Type VPA → approve in app | Online |
| **Flash UPI** | High-volume repeat apps | Medium (SDK) | PIN only (no app switch) | Online (in-app) |
| **Static QR** | Physical stores, no-tech | Zero (print QR) | Scan → type amount → PIN | Offline |
| **Dynamic QR** | Delivery, desktop, invoices | Medium (API) | Scan → PIN (amount pre-filled) | Offline/Online |
| **SoftPOS** | Field agents, delivery, retail | Low (app install) | Scan QR / Tap card / Pay link | Offline |

---

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
