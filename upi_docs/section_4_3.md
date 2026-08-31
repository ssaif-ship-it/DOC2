This guide walks you through integrating Cashfree Subscriptions, covering UPI AutoPay, eNACH, and Card Standing Instructions, from activating the product to your first live recurring charge. At each step, we call out what you are actually deciding, what it means for your customer, and what it means for you operationally, not just the API call to make.

## 1. Before You Start: Prerequisites

| Requirement | Description | Status / Action |
| :-- | :-- | :-- |
| **Cashfree Account** | Active account on merchant.cashfree.com | Mandatory, [sign up or log in](https://merchant.cashfree.com/merchants/signup) |
| **KYC Verification** | KYC v3 completed and approved | Mandatory, see the [KYC Compliance Guide](https://www.cashfree.com/docs/help/account/account-activation#required-documents) |
| **PG Activation** | Payment Gateway live status enabled | Mandatory, see [PG Activation Steps](https://www.cashfree.com/docs/help/account/account-activation) |
| **Subscriptions Product** | Explicit product activation in Dashboard | Request via Dashboard or your account manager |

<!-- REMOVED per Saif's comment on the live doc (2026-08-12): dropped the "Bank Verification / penny-test ACKNOWLEDGED" row. Confirm this was because it's not actually a Subscriptions-specific gate (e.g. it's just general PG activation and doesn't belong in this checklist), so nothing else needs adjusting elsewhere in this file. -->

> **Note on VPA provisioning:** Once Subscriptions is activated, Cashfree automatically provisions a dedicated merchant VPA (e.g., `yourmerchant@cfnsdl`) with the subscription attribute enabled on the UPI switch.

## 2. The Two Ways to Integrate

Before writing any code, decide how much of the mandate creation experience you want to build yourself. This is the choice that shapes everything else in this guide.

<div style="display:flex;flex-wrap:wrap;gap:16px;margin:16px 0;">
  <div style="flex:1;min-width:220px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:14px 16px;">
    <div style="font-weight:600;margin-bottom:6px;">Hosted Checkout</div>
    <div style="font-size:14px;color:#334155;">Cashfree hosts the mandate approval page. You redirect your customer there, Cashfree collects their VPA/bank details and manages the authorization screen, then redirects back to you.</div>
  </div>
  <div style="flex:1;min-width:220px;background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:14px 16px;">
    <div style="font-weight:600;margin-bottom:6px;">Seamless (API-only)</div>
    <div style="font-size:14px;color:#334155;">You build the entire mandate creation UI yourself and call Cashfree's APIs directly. Your customer never leaves your app or site, but you own the interface, the validation, and the PCI/UPI handling on your end.</div>
  </div>
</div>

| | Customer sees | You have to build |
| :-- | :-- | :-- |
| **Hosted Checkout** | Briefly redirected to a Cashfree-branded approval page, then back to you | Almost nothing, call the API, redirect using the returned link |
| **Seamless** | Never leaves your app, approves the mandate inside your own UI | The full mandate creation interface, plus your own handling of UPI/bank details |

If you are not sure which to pick: Hosted Checkout gets you live fastest and is what most merchants start with. Seamless is worth the extra build only if a visible redirect to Cashfree would actually hurt your conversion or brand experience.

Two lighter-weight options sit alongside these: the **Element SDK** gives you a native mobile UI while Cashfree still processes everything behind it, a middle ground, less work than full Seamless, more native feel than a redirect, and **Dashboard/Payment Links** let you create and send a subscription with no code at all, useful for sales-led billing or quick testing rather than a real integration.

## 3. Building the Integration, Step by Step

<div style="display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:16px 0;font-size:13px;">
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">1. Activate</div>
  <div style="color:#94a3b8;">&rarr;</div>
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">2. Keys &amp; Webhooks</div>
  <div style="color:#94a3b8;">&rarr;</div>
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">3. Create a Plan</div>
  <div style="color:#94a3b8;">&rarr;</div>
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">4. Authorize Mandate</div>
  <div style="color:#94a3b8;">&rarr;</div>
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">5. Execute Charges</div>
  <div style="color:#94a3b8;">&rarr;</div>
  <div style="background:#f0f4f8;border:1px solid #cbd5e1;border-radius:6px;padding:6px 12px;">6. Reconcile</div>
</div>

### Step 1: Activate Subscriptions

Log in to the Merchant Dashboard, go to **Products > Subscriptions**, and click **Request Activation**. This provisions your `SBCProfile`, webhook triggers, and VPA mandate attributes on the UPI switch. There is no customer-facing effect at this step, it is account setup, but it can involve a manual review, so start it before you plan a go-live date.

### Step 2: Get API Keys and Set Up Webhooks

Retrieve your production and sandbox credentials under **Developers > API Keys** (`x-client-id`, `x-client-secret`, `x-api-version`), see the [Authentication Guide](https://www.cashfree.com/docs/api-reference/authentication). Then register your webhook endpoint under **Developers > Webhooks** and subscribe to:

*   `SUBSCRIPTION_STATUS_CHANGE`
*   `SUBSCRIPTION_AUTH_SUCCESS` / `SUBSCRIPTION_AUTH_FAILURE`
*   `SUBSCRIPTION_PAYMENT_SUCCESS` / `SUBSCRIPTION_PAYMENT_FAILURE`

Why this matters for your customer: webhooks are how your own app finds out a mandate was approved or a charge failed. If these are not wired up correctly, your customer could see a stale status in your app, still "pending" after they have approved, or still "active" after a payment failed, even though Cashfree processed it correctly on its end. Verify incoming webhooks with HMAC-SHA256 using the [Signature Verification Specs](https://www.cashfree.com/docs/payments/online/webhooks/signature-verification).

<!-- FLAG FOR SAIF: from your test account notes, confirm whether you actually had to implement this signature verification by hand, or whether an SDK/dashboard setting handled it for you. If it's handled for you, this section should say so and skip straight to "which events to subscribe to." -->

### Step 3: Create a Plan

A plan defines the billing rules a customer will be authorizing. You are making two decisions here, both already covered in detail in [4.1 AutoPay](#doc-4-1):

*   **Periodic or On-Demand**, whether Cashfree auto-triggers debits on a schedule, or you trigger each charge yourself.
*   **Exact or Max amount**, whether the customer is authorizing one fixed number every cycle, or a ceiling you can charge up to.

What this means for your customer: Exact is predictable, they know exactly what leaves their account every cycle. Max gives you flexibility, useful for variable bills, but your customer is authorizing a range, not a number, which some customers find less reassuring at approval time.

Create the plan via **Dashboard: Subscriptions > Plans > Create Plan**, or `POST /pg/plans`, see the [Plans API Reference](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/plans/create).

### Step 4: Create and Authorize the Subscription

Tie a customer to the plan with `POST /pg/subscriptions`, see the [Create Subscription API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/mandate/create). This returns an `authorization_link`, what you do with it depends on the integration approach from Step 2 above, redirect for Hosted Checkout, or feed it into your own UI for Seamless.

You are also choosing a payment method here, which changes what your customer actually experiences:

| Method | What your customer does |
| :-- | :-- |
| **UPI AutoPay** | Approves the mandate with their UPI PIN, inside their own UPI app (Intent, QR, or Collect) |
| **eNACH** | Gets redirected to their bank's NetBanking or Debit Card portal to approve |
| **Card SI** | Enters an OTP to tokenize their card at the SI Hub |

UPI AutoPay tends to complete fastest since most customers already have a UPI app open and ready. eNACH's bank redirect is an extra hop, and some customers drop off there simply because they do not recognize the bank's page. Offering more than one method widens who can pay you, but means you are supporting more than one approval experience.

### Step 5: Execute Recurring Charges

Once the mandate is `ACTIVE`, Periodic plans debit automatically on schedule, On-Demand plans need you to call `POST /pg/subscriptions/pay` yourself. Every execution follows the Pre-Debit Notification, retry, and denial rules already covered in [4.1 AutoPay, sections 5 and 6](#doc-4-1), that is where the actual mechanics live, this step is just where you trigger it.

If you need finer control over notification timing than the default, see the [Merchant-Controlled PDN & Execution APIs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/payment/create-controlled-notification).

**On changing an amount mid-mandate:** Cashfree does not offer a direct API to edit an active mandate's amount or expiry in place. To bill a customer a different amount going forward, create a new plan with the revised amount and apply it via the `CHANGE_PLAN` action described in Step 6.

### Step 6: Manage, Monitor, and Reconcile

Control active mandates via Dashboard or `POST /pg/subscriptions/{subscription_id}/manage`, see the [Manage Subscription API Reference](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/mandate/manage).

| Action | Effect on your customer | When to use it |
| :-- | :-- | :-- |
| **PAUSE** | Debits stop, but the mandate itself stays alive, nothing for them to re-approve later | Customer requests a temporary break, or you are troubleshooting |
| **ACTIVATE** | Resumes debits on the existing mandate | Ending a pause |
| **CANCEL** | Mandate is revoked outright, they would need to approve a brand new one to resume | Customer is done, or the relationship is ending |
| **CHANGE_PLAN** | They keep paying, but under new plan terms | You need to change the amount, frequency, or ceiling |

## 4. Sandbox Testing & Go-Live Checklist

Test end to end in Cashfree's Sandbox (`https://sandbox.cashfree.com/pg`) before going live:

*   [ ] Mandate creation and simulated PIN approval, see [Sandbox Environment Resources](https://www.cashfree.com/docs/payments/online/resources/sandbox-environment)
*   [ ] Mandate cancellation and the user-decline path
*   [ ] First cycle charge execution and webhook verification
*   [ ] A simulated `INSUFFICIENT_FUNDS` failure, confirm your app reacts correctly per the retry rules in [4.1](#doc-4-1)
*   [ ] Signature verification, using the [Webhook Tools](https://www.cashfree.com/devstudio/preview/pg/tools/webhookVerification)

Before flipping to production:

*   [ ] KYC v3 approved
*   [ ] Subscriptions product enabled in the Production Dashboard
*   [ ] Production API keys updated
*   [ ] Webhook URLs updated to your live SSL endpoint
*   [ ] Error handling mapped against [5.3 Standard & AutoPay Error Codes](#doc-5-3)

## 5. API Quick Reference

For when you already know the flow and just need the endpoint:

| Endpoint | Method | Purpose | Reference |
| :-- | :-- | :-- | :-- |
| `/pg/plans` | `POST` | Define billing schedules and amounts | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/plans/create) |
| `/pg/subscriptions` | `POST` | Initialize subscription and generate mandate link | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/mandate/create) |
| `/pg/subscriptions/{id}` | `GET` | Fetch subscription status and details | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/mandate/fetch) |
| `/pg/subscriptions/{id}/manage` | `POST` | Pause, resume, or cancel subscription | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/mandate/manage) |
| `/pg/subscriptions/pay` | `POST` | Trigger an on-demand recurring charge | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/raise-a-charge-or-create-an-auth) |
| `/pg/subscriptions/{id}/payments` | `GET` | Retrieve payment execution history | [API Docs](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/payment/fetch-payments-for-mandate) |

<!-- FLAG FOR SAIF: your PG/Online Store test notes say Subscriptions actually runs on a legacy /api/v2 API in practice, while every endpoint above is the newer /pg one from Cashfree's "latest" docs. Confirm which one your test account is actually provisioned on before this table goes live, if it's the legacy one, this whole table and several links above need to point at /api/v2 endpoints instead. -->

Full schemas, headers, status codes, and error payloads are in the [Cashfree Subscriptions API Portal](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/overview), and the [Postman Collection](https://www.cashfree.com/docs/api-reference/payments/latest/subscription/subscription-postman-collection) if you would rather explore hands-on.
