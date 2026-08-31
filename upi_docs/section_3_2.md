## Find Your Merchant Category

Before you look at payment options, place yourself in one of these four categories. It decides which rows in the comparison below actually apply to you, and which ones you can skip.

| You are | This means | What matters to you |
| :-- | :-- | :-- |
| **Online only** | You sell through a website, an app, or both, with no physical counter. | UPI Intent for mobile checkout, Dynamic QR for desktop |
| **Offline only** | You sell from a physical storefront or counter, with no website or app of your own. | Static QR for a fixed counter, SoftPOS if your staff move around |
| **Online and offline** | You run a website or app, and you also take payments in person. | A mix, UPI Intent and Dynamic QR online, Static QR or SoftPOS in person |
| **Field or mobile collection** | Your staff or agents collect payment away from a fixed location, delivery, home visits, on site services. | SoftPOS |

Once you know which row describes you, the comparison below tells you exactly which product to build first, and which ones you can ignore for now.

---

## Product Comparison at a Glance

Pick the product that matches how your customers pay you. You are not locked in, most merchants run two or three of these side by side, and you can add another later without redoing your integration.

| Product | Best for | Integration effort | Customer action | What to know before you pick it |
| :-- | :-- | :-- | :-- | :-- |
| **[UPI Intent](#doc-2-1)** | Mobile app and mobile web checkout | Low (API or SDK) | Tap their UPI app, enter PIN | Highest success rates of the online flows. Behaviour differs on iOS, see 2.1. |
| **[UPI Collect](#doc-2-2)** | Narrow. Only the exempt categories below | Low (API) | Type VPA, approve in their app | **Restricted.** Manual VPA entry for P2M is under sunset. See the note in Step 5 before building on this. |
| **[Static QR](#doc-2-3)** | Counter payments, low tech stores | Low (activation, then print) | Scan, type amount, enter PIN | Not zero effort. Needs activation, and it cannot be reconciled per order. |
| **[Dynamic QR](#doc-2-3)** | Delivery, desktop checkout, invoices | Medium (API) | Scan, enter PIN (amount pre-filled) | The recommended replacement for Collect on desktop web. |
| **[SoftPOS](#doc-2-4)** | Field agents, delivery staff, retail | Low (app install) | Scan QR, tap card, or pay by link | Needs activation, agent registration and agent KYC. Tap to pay needs an NFC capable Android phone. |

**If you only read one row.** Selling online, on mobile: UPI Intent. Selling online, on desktop: Dynamic QR. Selling in person: Static QR for a fixed counter, SoftPOS if staff move around.

---

# Getting Started from Zero: Complete Merchant Onboarding Guide

This guide takes you from no account to live transactions. It is eight steps, and four of them are decisions rather than tasks.

| Step | What happens | What you decide |
| :-- | :-- | :-- |
| 1. Sign up | You get a dashboard and sandbox access immediately | Nothing, just complete it |
| 2. Complete KYC | Cashfree verifies your business and bank account | Nothing to choose, but this is what gates production |
| 3. Get API keys | You collect your test and production credentials | Nothing, just complete it |
| 4. Choose your integration path | You commit to how your checkout is built | Hosted checkout, custom API, or mobile SDK. Hardest of these to reverse. |
| 5. Integrate online | You build and test against sandbox | Which UPI flows you enable |
| 6. Set up offline acceptance | Optional, skip if you sell online only | Static QR or SoftPOS |
| 7. Test end to end | You prove success, failure and refund paths work | Nothing, just complete it |
| 8. Go live | You switch keys and start taking real money | Your settlement cycle |

You can work through Steps 3 to 7 in sandbox while Step 2 is still pending. Nothing about KYC blocks you from building.

---

<style>
.cf-acc-wrap{margin:20px 0 28px;}
.cf-acc-item{border:1px solid #E5E7EB;border-radius:10px;margin-bottom:10px;overflow:hidden;background:#FFFFFF;}
.cf-acc-item > summary{list-style:none;cursor:pointer;padding:14px 18px;display:flex;align-items:center;gap:10px;font-size:15px;background:#F9FAFB;position:relative;}
.cf-acc-item > summary::-webkit-details-marker{display:none;}
.cf-acc-item > summary::after{content:"";position:absolute;right:18px;top:50%;width:8px;height:8px;border-right:2px solid #6B7280;border-bottom:2px solid #6B7280;transform:translateY(-65%) rotate(-45deg);transition:transform .15s ease;}
.cf-acc-item[open] > summary::after{transform:translateY(-35%) rotate(45deg);}
.cf-acc-item[open] > summary{background:#F4F0FA;border-bottom:1px solid #E5E7EB;}
.cf-acc-item > summary .cf-acc-tag{font-size:11px;font-weight:700;color:#5A28A3;background:#F4F0FA;padding:3px 9px;border-radius:999px;flex-shrink:0;}
.cf-acc-item[open] > summary .cf-acc-tag{background:#FFFFFF;}
.cf-acc-item > summary .cf-acc-title{font-weight:600;color:#111827;padding-right:20px;}
.cf-acc-body{padding:18px 18px 22px;}
.cf-acc-body > *:first-child{margin-top:0;}
.cf-acc-body > *:last-child{margin-bottom:0;}
</style>

<div class="cf-acc-wrap">

<details class="cf-acc-item" open>
<summary><span class="cf-acc-tag">Step 1</span><span class="cf-acc-title">Sign Up on Cashfree</span></summary>

*   Go to [merchant.cashfree.com](https://merchant.cashfree.com) and create an account.
*   Provide basic business details (business name, type, PAN, contact info).
*   You land on the Merchant Dashboard with access to the Test (Sandbox) environment immediately.

**Where this leaves you.** You can generate test API keys, build a full integration and run simulated payments today. You cannot accept a real payment until Step 2 clears.

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 2</span><span class="cf-acc-title">Complete KYC</span></summary>

In **Dashboard > Account Settings > KYC**, upload:

*   **PAN** (Business or Individual, depending on your entity type)
*   **Bank account details** (IFSC, account number, account holder name)
*   **Address proof and business registration documents**

Cashfree then runs a penny test, a Re 1 NEFT credit to the bank account you gave. You confirm receipt by replying to the bank account confirmation email Cashfree sends you. This is an email reply, not a button in the dashboard.

### Your options while KYC is pending

| Situation | What you can do |
| :-- | :-- |
| You want to start building now | Yes. Use your Test keys from Step 3 and build the whole integration in sandbox. Nothing here is wasted work. |
| You need to go live on a fixed date | Submit KYC first, before you write any code. Verification is the long pole, not the integration. |
| Your documents were rejected | The dashboard shows which document failed and why. Re-upload the corrected one, the rest of your submission is retained. |
| Your entity type changed after signup | Raise this with support before re-uploading. Changing entity type after approval is slower than getting it right the first time. |

**How this affects you later.** Your MCC (Merchant Category Code) is assigned from what you declare here, your website, and your product listing. You do not choose your own MCC. Your MCC then determines your per transaction limits, which UPI flows you are permitted to use, and whether you need TPV. If you sell across more than one business line, flag it now, because a wrong MCC surfaces later as unexplained declines. See [3.1 Standards and Onboarding](#doc-3-1) and [3.4 MCC Limits and Caps](#doc-3-4).

### How to check where your KYC stands

Your status is shown against your account and moves through these values:

| Status | What it means | What to do |
| :-- | :-- | :-- |
| **KYC pending** | You have not submitted yet | Upload the documents above |
| **Under review** | Submitted, Cashfree is verifying | Nothing, wait. Keep building in sandbox. |
| **Resubmit KYC** | Something was rejected | The reason is shown against the failed document. Re-upload just that one. |
| **Completed** | Approved | You can generate production keys |
| **Blocked** | Products cannot be activated for this business | Contact support, this is not fixable by re-uploading |

> **Success:** Once your KYC status reads Completed, the Payment Gateway is activated for production.

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 3</span><span class="cf-acc-title">Get API Keys</span></summary>

Go to **Dashboard > Payment Gateway > Developers > API Keys**.

*   **Test mode:** keys are auto-generated, available immediately.
*   **Production mode:** click **Generate API Keys** and complete 2FA. Available once KYC is approved.

Store your keys securely:

*   `x-client-id: <YOUR_APP_ID>`
*   `x-client-secret: <YOUR_SECRET_KEY>`

> **Warning:** Never expose your secret key in client-side code. Every call that uses it belongs on your server.

**Where this leaves you.** You have two independent key pairs. Test keys only ever hit sandbox, production keys only ever hit live. Keeping them in separate environment configs from day one avoids the most common go-live incident, which is shipping test keys to production.

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 4</span><span class="cf-acc-title">Choose Your Integration Path</span></summary>

This is the decision that is most expensive to reverse, so it is worth ten minutes now.

| If this is you | Take this path | Trade-offs |
| :-- | :-- | :-- |
| You want the fastest possible start and minimal code | **Cashfree Checkout (hosted page)**. Cashfree renders the payment page, you redirect to it. | Control over checkout look and feel. The customer briefly leaves your domain. |
| You want full control over the checkout UI | **Seamless / Custom Integration (API)**. You build the UI, you call the APIs. | More build time, and you own webhook handling, retries and error messaging. |
| You have a mobile app and want UPI inside it | **Mobile SDK**, available for Android, iOS, React Native, Flutter and Cordova. | Little. This is the standard choice for app-first merchants. |
| You sell in person, online is not relevant | **SoftPOS or Static QR**. Skip Step 5 and go to Step 6. | Per order reconciliation on Static QR, see Step 6. |

**Can you change your mind later?** Moving from hosted checkout to custom is a full front end rebuild, though your order creation and webhook code carries over. Adding a mobile SDK alongside an existing web integration is additive and low risk. Adding offline acceptance later is entirely separate and does not touch your online integration.

**Not sure?** Start with hosted checkout. It gets you live fastest, and the server-side work you do for it (order creation, webhook handling, signature verification) is exactly the work a custom integration needs later.

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 5</span><span class="cf-acc-title">Integrate Online (Standard PG)</span></summary>

Every online transaction flow, whichever path you chose, is the same three moves:

**Create an Order** (server side) → **Process the Payment** (client side) → **Handle the Webhook** (server side).

### The two calls you will make

Merchants most often stall here, because it looks like one call and it is two.

1.  `POST /orders` creates the order and returns a **`payment_session_id`**. It does **not** return a UPI deep link.
2.  Order Pay, with `payment_method.upi.channel` set, returns the thing you actually render: `"link"` for an Intent deep link, `"qrcode"` for a QR payload, `"collect"` with a `upi_id` for a Collect request.

Base URLs:

*   Sandbox: `https://sandbox.cashfree.com/pg`
*   Production: `https://api.cashfree.com/pg`

Every request needs these four headers:

```
x-client-id:      <YOUR_APP_ID>
x-client-secret:  <YOUR_SECRET_KEY>
x-api-version:    2026-01-01
Content-Type:     application/json
```

A request without `x-api-version` fails, and this is the single most common first-call error. Check the [API reference](https://www.cashfree.com/docs/api-reference/overview) for the current version before you build, since it is dated and does change.

### Handling the result

Treat the **server to server webhook as the only source of truth** for payment status. The browser redirect back to your return URL is not a reliable success signal, because the customer may close the tab, lose signal, or return before the bank has responded.

Verify every webhook before you act on it. The signature is HMAC SHA256 over the timestamp concatenated with the raw payload, base64 encoded, delivered in the `x-webhook-signature` header alongside `x-webhook-timestamp`. See [signature verification](https://www.cashfree.com/docs/payments/online/webhooks/signature-verification). If you skip this, your webhook endpoint accepts anything anyone posts to it.

### Which UPI flows to enable

**Intent.** Enable this. It is the default for mobile app and mobile web, and it carries the best success rates. See [2.1 UPI Intent](#doc-2-1).

**Dynamic QR.** Enable this if you have desktop web customers, or you send invoices or payment links. See [2.3 QR Solutions](#doc-2-3).

**Collect.** Read this before you build on it.

> **Restricted flow.** Manual VPA entry Collect for P2M is under sunset. Unless your category is exempt, do not build on it, and migrate if you already have. Use Dynamic QR for desktop web instead. For the scope, the exemptions and the migration path, see [2.2 UPI Collect](#doc-2-2).

### Reference documentation

*   [Android SDK](https://www.cashfree.com/docs/payments/online/mobile/android), also available for iOS, React Native, Flutter and Cordova
*   [Web Checkout](https://www.cashfree.com/docs/payments/overview)
*   [API Reference](https://www.cashfree.com/docs/api-reference/overview)

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 6</span><span class="cf-acc-title">Set Up Offline Acceptance (Optional)</span></summary>

Skip this step entirely if you sell online only.

### Your options

| | **Static QR** | **SoftPOS** |
| :-- | :-- | :-- |
| Best for | A fixed counter, one till, low volume | Staff who move, delivery, field collection, multiple counters |
| What the customer does | Scans, types the amount themselves, enters PIN | Scans a QR you generate, taps a card, or pays a link you send |
| Amount | Customer types it, so it can be wrong | You enter it, so it is always right |
| Reconciliation | **Weak.** You cannot tie a payment to a specific order. You rely on SMS alerts or manual ledger checks. | Per transaction, per agent, per collection point |
| Setup | Request activation, then print the standee | Request activation, install the app, register each agent, complete agent KYC |
| Hardware | None | An Android phone. NFC required if you want tap to pay. |

**Choose Static QR if** you need to start taking payments tomorrow and you can live without order level reconciliation.

**Choose SoftPOS if** you need to know which agent collected what, or you need to reconcile against orders or invoices, or your staff collect payment away from a fixed counter.

**How this affects you later.** Static QR's reconciliation gap is not something you can fix downstream. If you expect to need order level matching within a few months, start on SoftPOS rather than migrating later.

To activate either, go to **Dashboard > SoftPOS > Request Activation**, or contact your account manager. See [2.4 SoftPOS and Offline Products](#doc-2-4).

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 7</span><span class="cf-acc-title">Test End to End</span></summary>

Test in sandbox before you switch keys. Sandbox uses the same APIs, the same webhooks and the same error codes as production.

1.  Point your integration at `https://sandbox.cashfree.com/pg` with your Test keys.
2.  Run each scenario below and confirm your system does the right thing for each.
3.  Verify webhooks arrive, that signature verification passes, and that your order status updates.
4.  Verify settlement reports appear in the test dashboard.

### Test VPAs

Use these handles in place of a real UPI ID to force a specific outcome.

| Test VPA | Outcome | What you should check |
| :-- | :-- | :-- |
| `testsuccess@gocash` | Payment succeeds | Order marked paid, success webhook received and verified, customer sees confirmation |
| `testinsufficientfunds@gocash` | Fails, insufficient funds | Customer sees a message telling them to use another account, not a raw error code |
| `testinvalidpin@gocash` | Fails, incorrect PIN | Customer is offered a retry, since this one is fixable by them |
| `testexpired@gocash` | Collect request expires | Order is not left hanging in pending forever |
| `testuserdropped@gocash` | Customer abandons the payment mid flow | Order stays in a clear pending or failed state, and does not sit there unresolved |

Also test a **refund**. User drops (the row above) are the largest single category of real world failures, and a checkout that leaves them in limbo generates support tickets from day one.

**How this affects you later.** Wrong error handling fails silently. A merchant who maps every failure to "payment failed, try again" will retry declines that must not be retried and will not retry the ones that would have succeeded. See [5.3 Standard Error Codes](#doc-5-3), which also covers how raw codes get translated into customer-facing messages.

</details>

<details class="cf-acc-item">
<summary><span class="cf-acc-tag">Step 8</span><span class="cf-acc-title">Go Live</span></summary>

1.  **Switch from Test to Production API keys** in your environment config. Confirm no test key remains anywhere in your production build.
2.  **Confirm KYC is approved.** Check the status in **Dashboard > Account Settings > KYC**.
3.  **Confirm the penny test.** Reply to the bank account confirmation email from Cashfree. Your settlements cannot reach you until this is done.
4.  **Choose your settlement cycle.** See the options below.
5.  **Configure webhook notifications.** Subscribe to the events by their literal names: `PAYMENT_SUCCESS_WEBHOOK`, `PAYMENT_FAILED_WEBHOOK`, `REFUND_STATUS_WEBHOOK`. Prose descriptions in a dashboard list will not match what your code needs to switch on.
6.  **Run one real transaction of your own** before you open the flow to customers.

### Your settlement cycle options

| Option | When the money reaches you | Cost | Pick this if |
| :-- | :-- | :-- | :-- |
| **Standard (T+2)** | Two business days after the transaction | Included | **This is the default.** Most merchants stay here. |
| T+1 | Next business day | Included, where enabled for your account | You need funds a day sooner |
| Instant Settlement | Roughly 15 minutes | Chargeable add-on | Your cash flow needs same day funds |
| On-Demand Settlement | Instantly, including holidays | Chargeable | You need funds outside the normal cycle, when you ask for them |

Business days exclude weekends and bank holidays. A transaction on Friday 3 June settles Monday 6 June on T+1, or Tuesday 7 June on T+2.

**How this affects you later.** Your first settlement may be held longer than your stated cycle while your account is new. Instant and On-Demand both carry a fee, so check your pricing before you switch to either. See [5.1 Settlements](#doc-5-1).

</details>

</div>

---

## Go Live Checklist

*   [ ] Cashfree account created and email verified
*   [ ] KYC documents uploaded and approved
*   [ ] Bank account verified and penny test confirmed by email
*   [ ] Production API keys generated and stored securely, no test keys in the production build
*   [ ] Integration tested in sandbox across every method you enabled
*   [ ] Success, insufficient funds, invalid PIN, expiry, user dropped and refund all tested
*   [ ] Webhook endpoints configured and receiving
*   [ ] Webhook signature verification implemented and passing
*   [ ] Settlement cycle chosen, and the Instant fee understood if you chose Instant
*   [ ] Refund and dispute workflows understood
*   [ ] SoftPOS activated, collection points created and agents KYC verified, if you sell offline
*   [ ] One real transaction completed by you
*   [ ] Monitoring in place, check transactions and settlements daily for the first two weeks

---

## Support & Resources

| Resource | Details |
| :-- | :-- |
| **Dashboard** | [merchant.cashfree.com](https://merchant.cashfree.com) |
| **API Docs** | [www.cashfree.com/docs](https://www.cashfree.com/docs) |
| **API Reference** | [www.cashfree.com/docs/api-reference/overview](https://www.cashfree.com/docs/api-reference/overview) |
| **Sandbox** | [Sandbox environment guide](https://www.cashfree.com/docs/payments/online/resources/sandbox-environment). Full test environment with simulated payments. |
| **Postman Collections** | Available for quick API testing. *Link to be added.* |
| **Account Manager** | Contact for custom pricing, enterprise volumes, or product activation |
