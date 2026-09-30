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

Before every execution, you must send a Pre-Debit Notification (PDN) to the customer's UPI app, at least 24 hours ahead of the debit. If a PDN push does not go through on the first try, Cashfree retries it automatically, about an hour apart, before giving up. The 24-hour countdown to the actual debit only starts once a PDN has gone through successfully, not when you first attempt to send it.

*   **The amount cannot change after the PDN is sent.** If the amount you actually debit differs from the amount stated in the PDN, the issuing bank declines the transaction on amount-match grounds. This is not a retry situation, correct the amount and notify again for the next attempt.
*   **If the PDN never goes through** (all of Cashfree's own retries exhausted, or a delivery failure on the bank's or PSP's side), the debit is blocked for that cycle. This is also not something you retry directly, the execution simply cannot proceed without a delivered PDN.

> **Exemptions:** PDNs are not required for Daily frequency mandates, same-day executions, or auto-replenishment use cases like NETC FASTag (MCC 4784) and RuPay NCMC (MCC 7412).

<!-- Claude, note for Saif: added the PDN auto-retry behavior and the On-Demand D+1 to D+14 charge window in Section 1, from the internal retry-mechanics reference you pasted (30 Sep). Left out the retry count and hourly cadence for PDN specifically, since your source cites two different intervals for it in different places (1 hour apart in one place, no interval given elsewhere) and I did not want to state a number I could not cross-check, said "about an hour apart" to stay directionally correct without overclaiming precision. Also left out the internal error codes, service/table names, and the Cashfree-managed vs Controlled(MERCHANT) execution flag for On-Demand, that last one needs a merchant-facing explanation of what it actually changes for you before it belongs here, happy to add it if you tell me what a merchant does differently under each. -->

## 6. Denied Payments and Retries

A debit can still fail even after the PDN goes through. What you do next depends on why it failed, there are three different situations below, and they are not handled the same way.

| What happened | What you do about it |
| :-- | :-- |
| **Customer-side and temporary:** low balance, a brief network issue at the customer's bank, an inactive-but-not-closed account | **Periodic subscriptions:** Cashfree retries automatically, up to **3 more attempts** the same day, spaced at least an hour apart, until 11:30 PM IST that day. A successful retry reactivates the subscription. **On-Demand:** there is no fixed cycle to retry within, you simply raise a new charge yourself whenever you are ready. |
| **The account or mandate itself is broken:** closed/invalid account, a mandate already cancelled or deactivated, a name mismatch | Retrying the mandate will not work. The customer needs to set up a brand new mandate. |
| **Blocked by something outside normal banking:** a court order, a frozen account, KYC pending, or a fraud/risk block on the customer's side | Retrying will not fix this. Follow up with the customer directly. |

Whichever of these applies, you are not limited to the mandate retry alone. You can always send the customer a one-time [payment link](#doc-2-3) to collect that specific due amount right away, it does not depend on the mandate at all, so it still works while the mandate itself is broken or being recreated.

<!-- Claude, note for Saif: rewrote this per your "confusing and wrong" comment. Moved the Periodic vs On-Demand distinction into the table row itself instead of only the intro paragraph, since that was the confusing part, a merchant reading row 1 alone couldn't tell what happens for On-Demand. Added the payment-link fallback per your comment on this section ("even after retries, we can send payment link"), worded as a one-time collection only, it doesn't fix or recreate the mandate, since Cashfree's own No-Code Payment Links product is documented for one-off payments only, not mandates (see the note in 4.3). Linked to 2.3, which is where 3.2 already points merchants for payment links.

Follow-up (30 Sep, per your internal retry-mechanics reference): corrected the Periodic retry cadence. This previously said "no more than 1 per day... before the current cycle expires," which implied retries could spread across multiple days. Your source says all retries happen the same charge day, spaced at least an hour apart, stopping at 11:30 PM IST that day or on success, whichever comes first. Fixed accordingly. Also added a fraud/risk block to row 3's examples, since your source lists it alongside court orders and frozen accounts. -->

## 7. Tracking Executions: SeqNum

Every mandate execution is tracked using a sequential number (SeqNum), month one is `SeqNum: 1`, month two is `SeqNum: 2`, and so on.

If a cycle's execution is ultimately not recovered, whether retries were exhausted, the cycle expired, or the failure was non-recoverable, that SeqNum stands cancelled. You skip it and move to the next sequence number (e.g., `SeqNum: 3`) for the following cycle. A missed SeqNum does not pause or restart the sequence.

## 8. Pause & Revoke (The Loan Exception)

Customers can pause or permanently revoke their active mandates directly from their UPI app. Any attempt to debit a paused or revoked mandate results in an immediate technical decline.

**The MCC 7322 Exception:** To protect lenders, merchants operating under **MCC 7322 (Debt Collection / Loans)** can set the **Revocable Flag to `N`** during mandate creation. This removes the Pause and Cancel buttons from the customer's UPI app for that mandate. The borrower cannot cancel it themselves, only the lender can cancel a non-revocable mandate, by contacting the acquiring bank directly.
