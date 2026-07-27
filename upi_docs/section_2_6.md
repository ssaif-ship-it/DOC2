---
title: "Merchant Onboarding Guide"
description: "Sign up, complete KYC, choose a UPI payment product, and go live on Cashfree — a step-by-step guide for merchants and their integration teams."
id: doc-merchant-onboarding
---

# Merchant Onboarding Guide

Everything you need to start accepting UPI payments on Cashfree — from creating your account to processing your first live transaction.

**Who this guide is for:** business owners and operators setting up a Cashfree account, working alongside a developer for the integration steps. Sections marked **For Developers** go into API-level detail; you can hand those off to your technical team.

## Prerequisites

Before you start, have the following ready:

- PAN (business or individual, depending on your entity type)
- Business registration documents and address proof
- A bank account for settlements (IFSC, account number, account holder name)
- Access to your website or app codebase, if integrating online payments

## Product Comparison at a Glance

| Product | Best For | Integration Effort | Customer Action | Where |
| :--- | :--- | :--- | :--- | :--- |
| **UPI Intent** | Mobile app/web checkout | Low (API) | Tap app → PIN | Online |
| **UPI Collect** | Desktop web, known VPA | Low (API) | Type VPA → approve in app | Online |
| **Flash UPI** | High-volume repeat apps | Medium (SDK) | PIN only (no app switch) | Online (in-app) |
| **Static QR** | Physical stores, no-tech | Zero (print QR) | Scan → type amount → PIN | Offline |
| **Dynamic QR** | Delivery, desktop, invoices | Medium (API) | Scan → PIN (amount pre-filled) | Offline/Online |
| **SoftPOS** | Field agents, delivery, retail | Low (app install) | Scan QR / Tap card / Pay link | Offline |

Not sure which product fits your business? See [Choosing a UPI Payment Product](#) for a more detailed breakdown.

## Step 1 — Sign Up on Cashfree

1. Go to [merchant.cashfree.com](https://merchant.cashfree.com) and create an account.
2. Provide your basic business details (business name, type, PAN, contact info).
3. You'll land on the **Merchant Dashboard** with immediate access to the Test (Sandbox) environment.

## Step 2 — Complete KYC

Go to **Dashboard → Account Settings → KYC** and upload:

- PAN (business or individual, based on entity type)
- Bank account details (IFSC, account number, account holder name)
- Address proof and business registration documents

Cashfree verifies your bank account with a **penny test** — a ₹1–2 NEFT transfer that you'll need to acknowledge in the dashboard.

> **Note:** Once KYC is approved, your Payment Gateway is activated for production.

## Step 3 — Get Your API Keys

*For Developers*

Go to **Dashboard → Payment Gateway → Developers → API Keys**.

- **Test mode:** keys are generated automatically.
- **Production mode:** click **Generate API Keys** and complete two-factor authentication.

Store your keys securely as environment variables:

```bash
x-client-id: <YOUR_APP_ID>
x-client-secret: <YOUR_SECRET_KEY>
```

> **Warning:** Never expose your secret key in client-side code.

## Step 4 — Choose Your Integration Path

| If you want… | Do this |
| :--- | :--- |
| Fastest start, minimal code | Use **Cashfree Checkout** (hosted page) — create an order via API and redirect the customer |
| Full control over UI | Use **Seamless/Custom Integration** — call the Order Pay API with a specific payment method |
| Offline/in-person only | Activate **SoftPOS** — no coding required |
| In-app UPI without redirects | Integrate the **Flash UPI SDK** into your Android app |

## Step 5 — Integrate (Online Payments)

*For Developers*

**Create an order**

```http
POST /orders
Headers: x-client-id, x-client-secret
```

```json
{
  "order_amount": 0,
  "order_currency": "INR",
  "customer_details": { "...": "..." },
  "order_meta": { "return_url": "..." }
}
```

The response returns a `payment_session_id` (for Cashfree Checkout) or `order_token` (for custom integrations).

**Accept payment**

- **Cashfree Checkout:** load Cashfree's hosted page with `payment_session_id`. All methods (UPI Intent, Collect, Cards, Net Banking, Wallets) appear automatically.
- **Custom/Seamless:** call the Order Pay API with a specific payment method:

  ```json
  // UPI Intent
  { "payment_method": { "upi": { "channel": "link" } } }

  // UPI Collect
  { "payment_method": { "upi": { "channel": "collect", "upi_id": "customer@upi" } } }
  ```

**Handle the response**

- Configure webhooks (**Dashboard → Developers → Webhooks**) for Payment Success, Payment Failed, and Refund events.
- Implement signature verification on incoming webhooks.
- Use the **Get Order Status API** as a fallback check.

See the full [API Reference](#) for request/response schemas and error codes.

## Step 6 — Activate Offline Payments (SoftPOS)

1. Go to **Dashboard → SoftPOS** and click **Request Activation**.
2. Once approved:
   - Add **Storefronts** (upload address proof and store images).
   - Add **Agents** (phone number and Aadhaar KYC).
   - Agents download the SoftPOS app and can start collecting payments.
3. For Dynamic QR via API, use the **Create Terminal Transaction API** with your terminal ID. *(For Developers)*

## Step 7 — Test End-to-End

- Use Cashfree's Sandbox environment to simulate payments.
- Test success, failure, user-dropped, and refund scenarios.
- Confirm webhooks arrive and your system processes them correctly.
- Check that settlement reports appear correctly in the dashboard.

## Step 8 — Go Live

1. Switch from Test to Production API keys.
2. Confirm KYC is fully approved.
3. Confirm your penny test shows as **Acknowledged**.
4. Choose your settlement cycle (T+1, T+2, or Instant).
5. Set up notifications for settlements, refunds, and disputes.
6. Start processing live transactions.

## Go-Live Checklist

- [ ] Cashfree account created and email verified
- [ ] KYC documents uploaded and approved
- [ ] Bank account verified (penny test acknowledged)
- [ ] Production API keys generated and stored securely
- [ ] Webhook endpoints configured and tested
- [ ] Signature verification implemented
- [ ] Integration tested in Sandbox (all methods)
- [ ] Settlement cycle chosen and confirmed
- [ ] Refund and dispute workflows understood
- [ ] SoftPOS activated (if offline payments needed)
- [ ] Collection points created and verified (if offline)
- [ ] Live — monitoring transactions and settlements daily

## Support & Resources

| Resource | Details |
| :--- | :--- |
| **Dashboard** | [merchant.cashfree.com](https://merchant.cashfree.com) |
| **API Docs** | See the Cashfree Developer Documentation |
| **Postman Collections** | Available for quick API testing |
| **Sandbox** | Full test environment with simulated payments |
| **Account Manager** | Contact for custom pricing, Flash UPI, or enterprise needs |
