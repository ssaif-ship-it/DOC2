
This guide provides a step-by-step walkthrough for merchants integrating Cashfree UPI AutoPay (alongside eNACH and Card Standing Instructions). It covers account activation, webhook configuration, subscription lifecycle execution, sandbox verification, and direct links to comprehensive developer documentation.

**Developer documentation quick links:**

- [Cashfree Developer Studio](#) — central documentation hub
- [Subscriptions API Reference](#) — full request/response schemas and error contracts
- [Cashfree Postman Collections](#) — interactive API testing collections

## 1. Onboarding Prerequisites

Before initiating subscription integrations, verify that your account meets the following baseline requirements:

| Requirement | Description | Status / Action | Reference |
| :--- | :--- | :--- | :--- |
| **Cashfree Account** | Active account on merchant.cashfree.com | Mandatory | [Sign Up / Login](#) |
| **KYC Verification** | KYC v3 completed and approved | Mandatory | [KYC Compliance Guide](#) |
| **PG Activation** | Payment Gateway live status enabled | Mandatory | [PG Activation Steps](#) |
| **Bank Verification** | Penny-test credit status marked `ACKNOWLEDGED` | Mandatory | [Bank Verification Docs](#) |
| **Subscriptions Product** | Explicit product activation in Dashboard | Request via Dashboard / Account Manager | [Dashboard Products](#) |

> **Note — VPA provisioning:** Upon activating Subscriptions, Cashfree automatically provisions a dedicated merchant VPA (e.g., `yourmerchant@cfnsdl`) with the subscription attribute enabled on the UPI switch.

## 2. Step-by-Step Integration Journey

```text
[ 1. Activate Subscriptions ] --> [ 2. API Keys & Webhooks ] --> [ 3. Create Plan ]
                                                                         |
                                                                         v
[ 6. Reconcile & Manage ]   <-- [ 5. Execute Charges (PDN) ] <-- [ 4. Authorize Mandate ]
```

### Step 1 — Activate Subscriptions Product

1. Log in to the Cashfree Merchant Dashboard.
2. Navigate to **Products > Subscriptions** and click **Request Activation**.
3. Internal provisioning configures your `SBCProfile`, webhook triggers, and VPA mandate attributes on the UPI switch.

### Step 2 — Retrieve API Keys & Configure Webhooks

- Retrieve production and sandbox credentials under **Developers > API Keys** (`x-client-id`, `x-client-secret`, `x-api-version`). Refer to the [Authentication Guide](#).
- Register your endpoint under **Developers > Webhooks** and subscribe to subscription lifecycle events:
  - `SUBSCRIPTION_STATUS_CHANGE`
  - `SUBSCRIPTION_AUTH_SUCCESS` / `SUBSCRIPTION_AUTH_FAILURE`
  - `SUBSCRIPTION_PAYMENT_SUCCESS` / `SUBSCRIPTION_PAYMENT_FAILURE`
- Implement HMAC-SHA256 signature verification on all incoming webhooks using the [Signature Verification Specs](#).

### Step 3 — Define a Plan

Create a plan defining the recurring frequency and ceiling limit (`PERIODIC` for automated schedules or `ON_DEMAND` for usage-based billing).

- **Dashboard flow:** Subscriptions > Plans > Create Plan
- **API endpoint:** `POST /pg/plans`

See request schemas and parameters in the [Plans API Reference](#).

### Step 4 — Create & Authorize Subscription

Tie a customer to a plan and generate the mandate authorization link.

- **API endpoint:** `POST /pg/subscriptions`
- **Authorization link:** Redirect the user or invoke the SDK using the returned `authorization_link`.

**Flow options:**

| Method | Customer Experience |
| :--- | :--- |
| **UPI AutoPay** | Customer approves mandate via UPI PIN inside their app (Intent, QR, or Collect) |
| **eNACH** | Redirects to NPCI eMandate portal for NetBanking/Debit Card approval |
| **Card SI** | Tokenization and OTP validation at SI Hub |

See authorization request schemas in the [Create Subscription API Docs](#).

### Step 5 — Execute Recurring Charges

Once the mandate status transitions to `ACTIVE`, recurring charges can be processed:

- **`PERIODIC` plans:** Cashfree automatically schedules and triggers debits on due dates.
- **`ON_DEMAND` plans:** Trigger charges manually via `POST /pg/subscriptions/pay`.

See payload specifications in the [Subscription Charge API Reference](#).

> **Mandatory rule — Pre-Debit Notification (PDN):** Cashfree automatically delivers an SMS/push PDN to the customer 24 to 48 hours prior to execution. Debits ≤ ₹15,000 execute automatically without PIN entry.

> **Tip:** Need custom control over PDN timing? Explore the [Merchant-Controlled PDN & Execution APIs](#).

### Step 6 — Manage, Monitor & Reconcile

Control active mandates via Dashboard or API (`POST /pg/subscriptions/{subscription_id}/manage`):

- **Supported actions:** `CANCEL` (revokes mandate), `PAUSE` (suspends debits), `ACTIVATE` (resumes), `CHANGE_PLAN`.

See the [Manage Subscription API Reference](#).

**Mandate updates:** Modify execution amounts or expiry dates without customer re-authorization via the [Mandate Update API](#).

## 3. Integration Approaches & SDKs

| Approach | Best For | Technical Effort | Documentation |
| :--- | :--- | :--- | :--- |
| **Cashfree Hosted Checkout** | Fastest setup; hosted mandate flow | Low | [Hosted Checkout Integration](#) |
| **Element SDK** | Native mobile app UI with Cashfree processing | Medium | [Subscription Element SDK Docs](#) |
| **Seamless API** | Full white-label control over UI and steps | High | [Subscriptions API Specs](#) |
| **Dashboard / Links (No-Code)** | Manual billing, sales teams, testing | Zero | [Subscription Payment Links Guide](#) |

## 4. Sandbox Testing & Go-Live Checklist

Before transitioning to production, complete end-to-end testing in the Cashfree Sandbox environment.

### Sandbox Testing Resources

- **Environment URL:** `https://sandbox.cashfree.com/pg`
- [Sandbox Overview & Credentials](#) — Sandbox Getting Started Guide
- [Test Cards & Simulator Handles](#) — Subscriptions Test Scenarios & Test VPAs
- [Postman Workspace](#) — Download Cashfree Subscriptions Postman Collection

### Sandbox Test Matrix

- [ ] Mandate creation and simulated PIN approval ([Test Handles Guide](#))
- [ ] Mandate cancellation / user decline path
- [ ] First cycle charge execution and webhook verification
- [ ] Auto-retry trigger on simulated `INSUFFICIENT_FUNDS`
- [ ] Signature verification validation using [Webhook Tools](#)

### Go-Live Verification

- [ ] KYC v3 approved and penny-test marked `ACKNOWLEDGED`
- [ ] Subscriptions product enabled in Production Dashboard
- [ ] Production API keys (`x-client-id`, `x-client-secret`) updated
- [ ] Webhook URLs updated to live SSL endpoint
- [ ] Error handling mapped per [Standard & AutoPay Error Codes Reference](#)

## 5. API Quick Reference

| Endpoint | Method | Purpose | Reference |
| :--- | :--- | :--- | :--- |
| `/pg/plans` | `POST` | Define billing schedules and amounts | [API Docs](#) |
| `/pg/subscriptions` | `POST` | Initialize subscription and generate mandate link | [API Docs](#) |
| `/pg/subscriptions/{id}` | `GET` | Fetch subscription status and details | [API Docs](#) |
| `/pg/subscriptions/{id}/manage` | `POST` | Pause, resume, or cancel subscription | [API Docs](#) |
| `/pg/subscriptions/pay` | `POST` | Trigger an on-demand recurring charge | [API Docs](#) |
| `/pg/subscriptions/{id}/payments` | `GET` | Retrieve payment execution history | [API Docs](#) |

For complete API schemas, HTTP header requirements, response status codes, and error payloads, visit the [Cashfree Subscriptions API Portal](#).