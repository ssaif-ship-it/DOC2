UPI Collect is a standard server-to-server "pull" mechanism. In this flow, the customer provides their Virtual Payment Address (VPA/UPI ID) on your checkout page. Your backend then sends a payment request directly to that VPA. The user receives a push notification or SMS, opens their UPI app (like Google Pay or PhonePe), and enters their PIN to authorize the transaction.

While this was once a standard integration, it inherently introduces friction (users must wait for network notifications and manually switch apps) and yields lower success rates compared to UPI Intent.

> **[VIDEO PLACEHOLDER, not yet recorded]** Collect flow walkthrough, the customer's side, end to end.
>
> **Shot list:**
> 1. Customer on your checkout page, types their VPA into the UPI ID field, taps Pay.
> 2. Checkout page shows a "waiting for confirmation" state.
> 3. Customer's phone: a push notification or SMS arrives from their UPI app.
> 4. Customer opens the UPI app and sees the payment request, your merchant name and the amount.
> 5. Customer enters their UPI PIN.
> 6. Success screen inside the UPI app.
> 7. Back on your checkout page: it updates to show payment confirmed.
>
> **Format:** screen recording, phone screen is what matters most, 30 to 45 seconds, no voiceover needed. Once you have the clip, host it the same way as the AutoPay video in 4.1 (a GitHub user-attachments link) and swap this block for:
>
> ```
> <video src="https://github.com/user-attachments/assets/YOUR-ASSET-ID" autoplay loop muted playsinline width="100%">
>   Your browser does not support the video tag.
> </video>
> ```

### Collect Restriction on Android (Effective February 28, 2026)

<!-- Claude, flagging for Saif: Ayushi's comment on this heading says "and desktop both -- for both UPI and UPI Autopay," which would widen this restriction beyond Android-only standard retail Collect to cover desktop too, and possibly AutoPay execution as well. That would contradict the Mandate Execution exemption bullet below, which explicitly keeps Collect available for AutoPay execution. Left unchanged pending confirmation from Ayushi on the actual scope before editing this. -->

To combat payment spam and push the ecosystem towards higher-converting flows, Cashfree has blocked UPI Collect requests on Android, effective **February 28, 2026**, in line with NPCI's broader direction of moving merchant collections towards UPI Intent and QR.

For standard e-commerce and retail transactions on Android, merchants are now required to default to **UPI Intent** (for mobile checkouts) or **Dynamic QR Codes** (for desktop/web checkouts). Standard Collect requests sent for everyday retail transactions on Android are blocked, resulting in failed transactions if you have not migrated.

**iOS mobile app and mobile web transactions are unaffected by this block for now.**

### Collect Exemptions: Valid Use Cases

Even on Android, UPI Collect remains a permitted and necessary integration for:

*   **Capital Markets & Broking:** For merchants operating under MCC 6211 or 6012 (IPO creation, execution and revoke, and Secondary Market use cases), Collect is still permitted and used with Third-Party Validation (TPV). It ensures the payment is pulled exactly from the investor's pre-registered bank account.
*   **Mandate Execution (AutoPay, OTM):** Recurring payments rely on the Collect architecture for execution, modification and revoke on a mandate that already exists. When a subscription is due, the merchant's server triggers a pre-authorized Collect request against the user's account, which executes automatically without requiring an additional PIN entry (within allowed limits). This exemption covers execution only, not creation: setting up a new mandate does not use Collect. See [4.1 AutoPay](#doc-4-1) for the supported creation modes.
*   **eRupi vouchers:** eRupi voucher transactions are exempt from the block.
*   **PACB-related flows:** Transactions routed through PACB are exempt from the block.
