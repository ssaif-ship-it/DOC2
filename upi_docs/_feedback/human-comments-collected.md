# Human review comments — collected offline

Source: `upi_docs/_feedback/comments.json` in the DOC2 repo, exported and filtered on 2026-08-28.

This pulls out everything actually **written by a person** (Saif, Ayushi) across every section: every human-authored comment thread in full, plus any human reply left inside a thread even when the original comment was posted by Claude. Claude-authored top-level comments with no human reply are left out of the body below and only counted in the summary, so this stays a record of human judgment, not AI output reviewing itself.

## 1.1 About UPI  (doc-1-1)

**On:** “secure 4- or 6-digit UPI PIN.”
> Or biometric
— **Ayushi**, 2026-08-20, *resolved* (resolved by Saif)


## 2.1 UPI Intent  (doc-2-1)

**On:** “When the user taps "Pay with UPI," your app/website triggers a specific link (starting with upi://pay?...). The phone's operating system instantly detects this and opens a bottom sheet showing all the…”
> Can we add the flow as well?
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “Warning: Never trust the frontend app-switch return alone to verify a payment. Always wait for the backend Webhook confirmation from Cashfree.”
> Can we add more information on intent link -- like how this is in android and ios , for seamless -- what all deeplinks are returned
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)


## 2.2 UPI Collect  (doc-2-2)

**On:** “nd mobile web transactions a”
> Add ios here as well
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “Android (Ef”
> and desktop both -- for both UPI and UPI Autopay
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “(TPV)”
> We can remove this
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “(AutoPay, OTM): Recurring payments rely on the Collect architecture for execution, modification and revoke. When a subscription is due, the merchant's server triggers a pre-authorized Collect request …”
> We can make ths clear , that mandate creation -- UPI collect is not allowe
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “Desktop-to-Mobile Flows: When a user is checking out on a desktop computer and chooses to type in their UPI ID rather than sca”
> This needs to be removed
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “While this was once a standard integration, it inherently introduces friction (users must wait for network notifications and manually switch apps) and yields lower success rates compar”
> Lets add a collect flow video
— **Ayushi**, 2026-08-26, *resolved* (resolved by Saif)


## 2.3 QR Solutions  (doc-2-3)

**On:** “Small offline retail storefronts, generic donation pages, or low-tech payment collection.”
> Where the qr cannot  be loaded dynamically
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “Limitations: Because the amount is variable and the QR does not contain a unique order ID, automated server-to-server reconciliation is very difficult. You rely on SMS notifications or manual ledger c…”
> Only available for offline merchat , where they dont haee a website and app and payments are collcted in close proximity
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)

**On:** “standard UP”
> dynamic
— **Ayushi**, 2026-08-26, *resolved* (resolved by Claude)


## 2.5 Affordability & Contextual Payments  (doc-2-5)

**On:** “Interchange Fees for PPI Wallet Acceptance”
> Do we need to include this?
— **Saif**, 2026-08-13, *open*


## 3.2 Merchant Onboarding Guide  (doc-3-2)

**On:** “Online”
> This table need to be reworked
— **Ayushi**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “In-app UPI without redirects	Integrate the Flash UPI SDK (Android)”
> Needs to be removed
— **Ayushi**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “User manually enters their VPA (UPI ID) on the checkout page.”
> Add note about collect sunset
— **Ayushi**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “Path 3: Flash UPI Fully native, in-app UPI experience, with no switching to a separate app.”
> To be removed
— **Ayushi**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “Ensure KYC is fully approved (v3).”
> How will user ensure this?
— **Ayushi**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “Switch from Test to Production API keys. Ensure KYC is fully approved (v3). Confirm the penny test is ACKNOWLEDGED. Choose your settlement cycle (T+1 / T+2 / Instant). Configure notifications (settlem…”
> Reality
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)


## 3.3 Investment Category Onboarding  (doc-3-3)

**On:** “To comply with SEBI guidelines, onboarding investment category merchants such as Stock Brokers, Mutual Funds, Online Bond Platform Providers (OBPPs), and Investment Advisers/Research Analysts (IA/RAs)…”
> give propepr structure and then explain the stuff in order
— **Saif**, 2026-08-11, *open*

**On:** “Axis Bank (API-Based): The most streamlined route. Handles are procured via internal API integration. The Banking Ops team uploads the specified DMO format file in Retool.  Note: Terminals are created…”
> This is internal , and merchant facing
— **Ayushi**, 2026-08-11, *resolved* (resolved by Claude)

**On:** “Bank-Specific Procurement Workflows The process for acquiring and mapping the Valid Handle varies depending on the chosen acquiring bank:  Axis Bank (API-Based): The most streamlined route. Handles ar…”
> whole needs to be changed whatever is not merchant facing
— **Saif**, 2026-08-12, *open*

**On:** “Axis and HDFC: No action required from the merchant. Cashfree procures and maps the handle. Axis is typically faster, since it is handled through an internal API; HDFC is a manual process and can take…”
> Naming Banks and giving bank specific steps, should we do it ?
— **Saif**, 2026-08-13, *open*


## 3.4 MCC Limits and Caps  (doc-3-4)

**On:** “Volume Cap: Standard Default merchants (₹100k tier) are subject to a maximum 20 transactions daily per rolling 24 hours.”
> easy explain
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “Bank-Level Overrides: Remitter banks reserve authority to apply lower internal spending limits (e.g., ₹50,000 daily) regardless of category cap allowance.”
> remove
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “24-Hour Security Cap: Profile updates (new registration, device binding, or UPI PIN reset) cap transactions at ₹5,000 total for the first 24 hours. Volume Cap: Standard Default merchants (₹100k tier) …”
> refine
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)


## 4.1 AutoPay  (doc-4-1)

**On:** “within 5 minutes of mandate creation)”
> Confirmation needed, not Stated by NPCI
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “Instant: If the very first debit happens instantly (within 5 minutes of mandate creation), no additional PIN is required, as the creation PIN suffices. Deferred: If the first execution is deferred to …”
> 1 rupeee limit
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “If an execution fails (e.g., insufficient funds), you are allowed a maximum of 9 re-initiation attempts (10 attempts total) for that specific SeqNum.”
> verify 3
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “the lending institution directly.”
> 2 type apis
— **Saif**, 2026-08-11, *resolved* (resolved by Saif)

**On:** “For MAX mandates specifically: the moment your customer approves the mandate in their UPI app, a ₹1 debit is triggered right away as a verification check, before any of your real recurring debits begi…”
> cofirm
— **Saif**, 2026-08-12, *open*

**On:** “Customer-side and temporary: low balance, a brief network issue at the customer's bank, an inactive-but-not-closed account	Retry it, Periodic only. The subscription moves to ON HOLD, and you call the …”
> verify
— **Saif**, 2026-08-12, *resolved* (resolved by Saif)


## 4.3 AutoPay Onboarding Guide  (doc-4-3)

**On:** “Bank Verification	Penny-test credit status marked ACKNOWLEDGED	Mandatory	Bank Verification Docs”
> Remove
— **Saif**, 2026-08-12, *resolved* (resolved by Saif)

**On:** “[ 1. Activate Subscriptions ] --> [ 2. API Keys & Webhooks ] --> [ 3. Create Plan ]”
> better looking wireframe
— **Saif**, 2026-08-12, *resolved* (resolved by Saif)

**On:** “This guide provides a step-by-step walkthrough for merchants integrating Cashfree UPI AutoPay (alongside eNACH and Card Standing Instructions). It covers account activation, webhook configuration, sub…”
> to do the following changes 
proper disperse of links
tell user proper step by step and what options they will get at each step verify that
like the the 2 apis we offer etc
— **Saif**, 2026-08-12, *resolved* (resolved by Saif)


## 5.1 Settlements  (doc-5-1)

**On:** “Standard (T+2)	Thursday at 4:00 PM”
> T+1
— **saif**, 2026-08-13, *open*

**On:** “3.3 Payment-Specific Timelines You are not forced to pick a single payout schedule for your entire business. The system allows you to configure different settlement speeds based on the type of payment…”
> remove
— **Saif**, 2026-08-13, *open*

**On:** “Here is how that timeline plays out in practice based on different transaction days:”
> Asked to show the source for the Real-World Scenarios table below (Standard/Weekend/Holiday Conflict/Instant rows).
— **Saif**, 2026-08-13, *open*


## 5.2 Refunds & Reversals  (doc-5-2)

**On:** “Refund	Merchant (Dashboard or API)	Post-capture (Up to 180 days from transaction date).	Used for order cancellations, product returns, goodwill credits, or SLA breaches.”
> confirm
— **Saif**, 2026-08-13, *open*


## 5.4 Smart Routing & Uptime  (doc-5-4)

**On:** “~92%.”
> Confirm
— **Saif**, 2026-08-13, *open*

**On:** “User Drops (~13%): Customer-initiated actions, such as closing the app, abandoning the payment page, or allowing the payment collect request to time out. Technical Failures (~7%): Infrastructure-level…”
> correct data 
or should we even keep it there?
— **Saif**, 2026-08-13, *open*


## Coverage summary

| Section | Total comments | With human input |
|---|---|---|
| 1.1 About UPI | 1 | 1 |
| 2.1 UPI Intent | 2 | 2 |
| 2.2 UPI Collect | 6 | 6 |
| 2.3 QR Solutions | 3 | 3 |
| 2.5 Affordability & Contextual Payments | 7 | 1 |
| 3.2 Merchant Onboarding Guide | 11 | 6 |
| 3.3 Investment Category Onboarding | 5 | 4 |
| 3.4 MCC Limits and Caps | 4 | 3 |
| 4.1 AutoPay | 6 | 6 |
| 4.3 AutoPay Onboarding Guide | 3 | 3 |
| 5.1 Settlements | 6 | 3 |
| 5.2 Refunds & Reversals | 5 | 1 |
| 5.4 Smart Routing & Uptime | 4 | 2 |

**Totals:** 41 comment threads opened directly by a human, 0 human replies inside threads (including ones opened by Claude), 22 Claude-opened threads with no human reply at all (excluded from the body above).
