UPI AutoPay is a recurring payments framework built on the Unified Payments Interface (UPI). It lets your customer set up a mandate (a Standing Instruction) once, and after that one-time authorization, their account can be debited automatically for every subsequent cycle without them opening their UPI app again, within the limits described below. It is commonly used for subscriptions, loan EMIs, insurance premiums, and utility bills.

Merchants can initiate mandate creation via three modes: **QR Scanning**, **Intent Deep Links**, or **Collect Requests**.

<video src="https://github.com/user-attachments/assets/cc00d497-1171-4b8d-be57-edde6a77320c" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>

## 1. The First Decision: Periodic or On-Demand

Before you create a mandate, decide which of the two AutoPay types fits your billing model. Everything else in this section, frequency, amount rule, and retries, follows from this choice.

| Type | How it works | Best for |
| :-- | :-- | :-- |
| **Periodic** | You register a fixed frequency (Daily, Monthly, Yearly, and so on) when creating the mandate. Cashfree automatically schedules and triggers the debit on each due date, you do not call an API to fire it. | Subscriptions, EMIs, insurance premiums, anything with a predictable billing calendar. |
| **On-Demand** | The mandate is created without a fixed schedule. You trigger each charge yourself by raising it through the API, for a date at least a day out and up to 14 days ahead, never for the same day, the 24-hour PDN notice in Section 5 below still applies. | Usage-based billing, ad-hoc top-ups, or any case where you do not know the next debit date in advance. |

### On-Demand: Two Ways to Trigger a Charge

This choice only applies to On-Demand mandates. Periodic mandates always run the Cashfree-Managed way, Cashfree's scheduler owns the billing calendar end to end, so there is nothing to manually trigger or retry.

By default, when you raise an On-Demand charge with a single call to `POST /subscriptions/pay`, Cashfree manages everything from there, sending the PDN, waiting out the mandatory 24-hour window, then executing the debit automatically, and retrying it for you if an attempt fails (see Section 5 and Section 6 below for the attempt counts). You get the final success or failure webhook, not a running account of each attempt.

If you need tighter control, for example custom retry timing or precise settlement alignment, you can ask your Cashfree account manager to enable the Merchant-Controlled flow for your account, it is not switched on by default. Once enabled, notifying and debiting become two separate calls you make yourself:

*   Call `POST /subscriptions/pay/controlled/notify-mandate` to send the PDN.
*   Once the PDN has succeeded and the 24-hour window has passed, call `POST /subscriptions/pay/controlled/execute-mandate` to trigger the debit.

Under this Merchant-Controlled flow, Cashfree never auto-debits and never auto-retries, if a step fails, you decide whether and when to call the same endpoint again with a new attempt ID. The two flows also cannot be mixed on the same charge, one raised through `/subscriptions/pay` is locked to the Cashfree-managed path and will reject the controlled endpoints.

A few guardrails still apply even though you are driving the timing yourself:

*   **Attempt caps:** up to 7 PDN attempts (1 initial plus 6 retries) and up to 4 charge attempts (1 initial plus 3 retries) per charge cycle. Going past either limit is rejected (`payment_notification_restriction_error` or `payment_execution_restriction_error`, "max number reached").
*   **One of each type at a time:** a new PDN can only be sent once the previous PDN on that cycle has reached a final outcome, success or failure, and separately, a new charge attempt can only be made once the previous charge attempt has reached a final outcome (`Prev_PDN_In_Progress` / `Prev_Execution_In_Progress`).
*   **A charge needs a successful PDN first:** the charge endpoint rejects the call until a PDN on that cycle has actually succeeded, not just been attempted.
*   **A narrow charge window:** charges are only allowed the day after a successful PDN or the day after that, never later, and consecutive charge attempts must be at least an hour apart.
*   **NPCI blackout windows:** debit and notification attempts are blocked during certain NPCI-governed windows. These shift over time, so there's no fixed list of hours to publish here, the rejection response always tells you the next time you're allowed to try.
*   **Attempt-level visibility:** a dedicated webhook fires on every PDN attempt (`SUBSCRIPTION_PAYMENT_CONTROLLED_NOTIFICATION_STATUS`) and every charge attempt (`SUBSCRIPTION_PAYMENT_CONTROLLED_EXECUTION_STATUS`), plus GET APIs to poll and reconcile, instead of the Cashfree-Managed flow's single final webhook.

<!-- Claude, note for Saif: added per your 30 Sep answer on Cashfree-Managed vs Merchant-Controlled flow. Kept to the endpoints and what a merchant actually does differently, left out the PaymentControlType enum values and the internal service name, those don't change how a merchant integrates.

Follow-up, 5 Oct: expanded with everything from your Controlled vs Uncontrolled breakdown and the follow-up Q&A. Confirmed Periodic is Cashfree-Managed only, Controlled is On-Demand-only and gated/opt-in (left out the internal feature-flag name). For the error codes and webhook names, cross-checked Cashfree's own public API docs first.

Correction, 5 Oct, same day: you then shared the confidential "Merchant-Controlled Subscription Charging Integration Guide" PDF, which is more authoritative than the public docs for this (it has the full error reference and exact webhook names), so re-did this against it. Fixes: the webhook names were missing "PAYMENT_" (real ones are SUBSCRIPTION_PAYMENT_CONTROLLED_NOTIFICATION_STATUS and SUBSCRIPTION_PAYMENT_CONTROLLED_EXECUTION_STATUS); dropped the "custom caps available on request" line, the guide states 7 and 4 as hard limits with no mention of per-merchant configurability; replaced the "4-day window" framing with the guide's actual, twice-stated, error-backed rule (charges only allowed on T+1 or T+2 after PDN success, nothing later); dropped the specific peak-hour clock times entirely, the guide explicitly says not to hardcode blackout windows since NPCI can change them; and fixed the concurrency rule, it's same-type-only (PDN blocks a new PDN, charge blocks a new charge), the charge-needs-a-successful-PDN-first requirement is a separate rule, not a concurrency lock.

Flagging for you: the guide's own "Timing in one line" summary box says "the charge remains active for attempts up to day T+4," which doesn't match the T+2 cutoff stated everywhere else in the same document, including a named rejection error for charging after T+2. Went with T+2 here since it's corroborated multiple times; you may want to get that cleared up with whoever owns the guide. -->

## 2. Frequencies (Periodic Mandates Only)

If you chose Periodic, you must register one of the following frequencies at mandate creation: Daily, Weekly, Fortnightly, Monthly, Bimonthly, Quarterly, Half-yearly, or Yearly.

<!-- Claude, flagging for Saif, not confirmed: this section used to list "As Presented" as a ninth Periodic frequency. I could not confirm that classification and removed it rather than leave it stated as fact. Cashfree's own Subscriptions Overview page (cashfree.com/docs/payments/subscription/introduction) assigns As Presented's defining behaviour, debiting a variable amount whenever a bill is generated, to On-Demand, not Periodic. The RBI Digital Payments E-Mandate Framework, 2026 does not use the term As Presented at all, it only distinguishes Fixed Amount and Variable Amount mandates. The only place "As Presented" appears anywhere on Cashfree's site is the Payment Modes page, written as "As and when presented," listed for physical/NACH mandate forms, not confirmed for UPI Autopay specifically. The MCC ceiling numbers in 4.4 look like real NPCI data and I have left that table alone, but whether those ceilings sit under Periodic or under On-Demand needs a definitive answer from your NPCI or compliance contact before this doc asserts either way. -->

## 3. Amount Rules: Exact or Max

Alongside frequency, every mandate also carries an amount rule:

| Amount Rule | Description |
| :-- | :-- |
| **EXACT** | You are authorized to debit the exact amount specified (e.g., exactly ₹1,000 for a fixed subscription). |
| **MAX** | You are authorized to debit up to a ceiling per cycle (e.g., up to ₹5,000 for a variable utility bill). If you collect less than the ceiling in one cycle, you cannot carry the difference forward and collect it in a later cycle. |

## 4. How Much Can Go Through Without a PIN

NPCI limits how much can be automatically debited before the customer has to re-enter their UPI PIN, this is their Additional Factor of Authentication, or AFA. Most merchants get a standard ceiling of ₹15,000 per debit; a short list of high-value categories (credit card bills, insurance premiums, mutual funds, and a few others) get a higher ₹1,00,000 ceiling instead. Above whichever ceiling applies to your category, the customer has to enter their PIN for that specific cycle.

The exact ceiling for your category, and the matching registration limits, are in **[4.4 MCC-Specific Limits](#doc-4-4)**, check that table rather than assuming ₹15,000 applies to you by default.

**First execution is a special case:** if it happens within 5 minutes of mandate creation, the PIN the customer just entered to create the mandate covers it too, no separate PIN entry. If the first debit is scheduled for later instead, it always needs a fresh PIN entry regardless of amount, this one time, even if it is below ₹15,000.

At mandate creation, Cashfree also runs a ₹1 verification debit on its own end, you do not need to trigger or configure this. Depending on how the mandate is set up, this ₹1 is either reversed back to the customer automatically (typically the same day), or retained and counted toward the first debit on the mandate rather than refunded separately. Either way, it always shows up as its own line item in your settlement report and dashboard, it is never silently absorbed or netted into another transaction, so you can trace it if a customer asks about it.
<!-- Claude, note for Saif: rewritten from your team's confirmation (24 Sep) that this depends on configuration (auto-reversed vs retained toward first debit), and that it always appears as its own traceable line item settling on the normal cycle. Internal system/report field names left out as not merchant-relevant. -->

## 5. The Pre-Debit Notification (PDN)

Before every execution, you must send a Pre-Debit Notification (PDN) to the customer's UPI app, at least 24 hours ahead of the debit. If a PDN push does not go through on the first try, Cashfree retries it automatically, once an hour, up to 6 times (7 attempts in total, including the first). These retries must wrap up early enough to leave a full 24 hours before your charge date, since a PDN needs that much lead time to clear before the debit. The 24-hour countdown to the actual debit only starts once a PDN has gone through successfully, not when you first attempt to send it.

*   **The amount cannot change after the PDN is sent.** If the amount you actually debit differs from the amount stated in the PDN, the issuing bank declines the transaction on amount-match grounds. This is not a retry situation, correct the amount and notify again for the next attempt.
*   **If the PDN never goes through** (all retries exhausted, or the lead time runs out first), the charge moves to a failed state for that cycle and no debit is attempted. This is also not something you retry directly, the execution simply cannot proceed without a delivered PDN.

If your business raises a high volume of same-day charges and the default hourly cadence does not fit, Cashfree can configure a faster retry interval or a different retry count for your account, ask your account manager.

This is the Cashfree-Managed behavior. On-Demand mandates using the Merchant-Controlled flow follow a different process instead, see the On-Demand section above.

> **Exemptions:** PDNs are not required for Daily frequency mandates, same-day executions, or auto-replenishment use cases like NETC FASTag (MCC 4784) and RuPay NCMC (MCC 7412).

<!-- Claude, note for Saif: updated with the exact PDN retry count (6 retries, 7 attempts total, 1 hour apart) and the 11:30 PM IST day-before cut-off, now that your 30 Sep timing document cross-confirms the numbers I'd previously hedged on. Also added the merchant-configurable retry cadence as a "ask your account manager" fact, without naming the internal config parameters, since a merchant can't self-serve this via API or dashboard per your material. Resolves comment c_9srjm7vgmumpmnx5 on the Controlled flow question, see the new subsection above Section 2. -->

## 6. Denied Payments and Retries

A debit can still fail even after the PDN goes through, and what happens next depends entirely on why. Here are the three cases you will run into:

<div style="display: flex; flex-direction: column; gap: 14px; margin: 20px 0;">

  <div style="border: 1px solid #eae5f2; border-left: 4px solid #22c55e; border-radius: 10px; padding: 18px 20px; background: #fafafa;">
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 6px; flex-wrap: wrap;">
      <div style="font-weight: 700; font-size: 15px; color: #0f172a;">Customer-Side and Temporary</div>
      <span style="display: inline-block; background-color: #c6f6d5; color: #22543d; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; white-space: nowrap;">Retryable</span>
    </div>
    <div style="color: #64748b; font-size: 13px; margin-bottom: 12px;">Low balance, a brief network issue at the customer's bank, an inactive-but-not-closed account</div>
    <ul style="color: #334155; font-size: 14px; line-height: 1.6; margin: 0; padding-left: 18px;">
      <li>Auto-retried by Cashfree: up to 3 retries (4 attempts total), at least 1hr apart, same day (Cashfree-Managed flow, see the On-Demand section in Section 1 for Merchant-Controlled)</li>
      <li>All attempts fail: Periodic waits for its next scheduled cycle automatically; On-Demand needs a fresh charge raised via the API</li>
    </ul>
  </div>

  <div style="border: 1px solid #eae5f2; border-left: 4px solid #ef4444; border-radius: 10px; padding: 18px 20px; background: #fafafa;">
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 6px; flex-wrap: wrap;">
      <div style="font-weight: 700; font-size: 15px; color: #0f172a;">Broken Account or Invalid Mandate</div>
      <span style="display: inline-block; background-color: #fed7d7; color: #742a2a; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; white-space: nowrap;">Not retryable</span>
    </div>
    <div style="color: #64748b; font-size: 13px; margin-bottom: 12px;">Closed/invalid account, a mandate already cancelled or deactivated, a name mismatch</div>
    <div style="color: #334155; font-size: 14px;">Not retryable. The customer needs to set up a brand-new mandate.</div>
  </div>

  <div style="border: 1px solid #eae5f2; border-left: 4px solid #ef4444; border-radius: 10px; padding: 18px 20px; background: #fafafa;">
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 6px; flex-wrap: wrap;">
      <div style="font-weight: 700; font-size: 15px; color: #0f172a;">Blocked by Banking or Regulatory Restrictions</div>
      <span style="display: inline-block; background-color: #fed7d7; color: #742a2a; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; white-space: nowrap;">Not retryable</span>
    </div>
    <div style="color: #64748b; font-size: 13px; margin-bottom: 12px;">A court order, a frozen account, KYC pending, or a fraud/risk block on the customer's side</div>
    <div style="color: #334155; font-size: 14px;">Not retryable. Resolution is on the customer or their bank, reach out to them directly.</div>
  </div>

</div>

None of this limits you to the mandate alone, though. A one-time [payment link](#doc-2-3) can collect that specific due amount right away regardless of which case applies, it does not depend on the mandate, so it still works while the mandate itself is broken or being recreated.

<!-- Claude, note for Saif: rebuilt as cards per your feedback that a table was the wrong format for this content, plus a pass on the sentence framing, less "Retrying X will not work" repeated verbatim across rows, more natural phrasing per case. Facts unchanged from before: same retry counts, timing, and the payment-link fallback. Colors follow the site's existing badge palette (green/red from 3.3's badges).

Follow-up: fixed a real error in card 1, not just wording. The automatic retry (3 more attempts, hourly, same day, until 11:30 PM IST) is not Periodic-only, your source material describes it as the same mechanic for both types ("On-Demand: no fixed cycle to auto-retry into after the day's attempts exhaust" implies the day's attempts happen for On-Demand too). The real difference, per your Periodic vs On-Demand comparison table, is only what happens once retries are exhausted: a Periodic subscription just waits for its next scheduled cycle automatically, while an On-Demand charge is marked failed with no next cycle to fall into, so you have to raise a fresh one yourself. Rewrote the card to say the retry mechanic applies to both, and scope "reactivates" to Periodic only, since On-Demand doesn't have a persistent subscription state to reactivate.

Second follow-up: reworked the three headings per your feedback, and pulled in the terminology/timing precision from the rewrite you pasted (3 retries = 4 attempts total; retries run on the charge date after the 24h PDN window; each failed attempt is marked FAILED). Did not add the internal bank codes (Z9, UT, U67, ZX, XC, ZH, K1, U16) from that draft, those are the internal codes you told me earlier not to expose on a merchant-facing page, so the cause lists stay in plain language. Open question for you: once retries are exhausted, does the subscription's ON HOLD status persist until the next cycle actually fires, or does it revert to normal/ACTIVE while it waits? The second line of card 1 currently doesn't name a status there at all, wanted to confirm before adding one.

Third follow-up: removed the "11:30 PM IST" cutoff claim from both this card and Section 5 above. Your Controlled vs Uncontrolled document raised doubt on whether that exact cutoff time is accurate or universal (it may be specific to one flow, or not something Cashfree discloses for the default automatic flow at all), so pulling the specific clock time until it's verified. Kept the parts that are still solid: the attempt counts (7 total PDN, 4 total debit) and the 1-hour minimum spacing.

Fourth follow-up, 5 Oct: now that you've confirmed Periodic is Cashfree-Managed only and the 7/4 numbers hold for Uncontrolled too, added a cross-reference from this card (and from Section 5) to the expanded On-Demand subsection in Section 1, so Controlled-flow merchants know their retry behavior is different and where to find it, and added the same account-manager configurability note here that Section 5 already had for PDN. Did not re-add an exact cutoff time since you confirmed there is no hard clock cutoff, timing in the Cashfree-Managed flow is just the 24h buffer plus 1hr spacing, run by Cashfree's internal scheduler.

Fifth follow-up, 5 Oct: cut all three cards down to bullet points per your feedback that the paragraphs were too dense, looked at how Juspay documents this (short tables and bullet points, not prose) as a reference point. Dropped the account-manager configurability mention and the FAILED/ON HOLD status terminology from card 1, both still findable in Section 5 and don't need repeating here. Cards 2 and 3 are now one line each, as you asked, no fact changes, same retry counts and same retryable/not-retryable conclusions as before. -->

## 7. Tracking Executions: SeqNum

Every mandate execution is tracked using a sequential number (SeqNum), month one is `SeqNum: 1`, month two is `SeqNum: 2`, and so on.

If a cycle's execution is ultimately not recovered, whether retries were exhausted, the cycle expired, or the failure was non-recoverable, that SeqNum stands cancelled. You skip it and move to the next sequence number (e.g., `SeqNum: 3`) for the following cycle. A missed SeqNum does not pause or restart the sequence.

## 8. Pause & Revoke

Customers can pause or permanently revoke their active mandates directly from their UPI app. Any attempt to debit a paused or revoked mandate results in an immediate technical decline.

**The MCC 7322 Exception:** To protect lenders, merchants operating under **MCC 7322 (Debt Collection / Loans)** can set the **Revocable Flag to `N`** during mandate creation. This removes the Pause and Cancel buttons from the customer's UPI app for that mandate. The borrower cannot cancel it themselves, only the lender can cancel a non-revocable mandate, by contacting the acquiring bank directly.
