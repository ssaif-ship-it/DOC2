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

### Collect Restriction on Android and Desktop (Effective February 28, 2026)

To combat payment spam and push the ecosystem towards higher-converting flows, Cashfree has blocked UPI Collect requests on Android and desktop, effective **February 28, 2026**, in line with NPCI's broader direction of moving merchant collections towards UPI Intent and QR.

For standard e-commerce and retail transactions, merchants are now required to default to **UPI Intent** (for mobile checkouts) or **Dynamic QR Codes** (for desktop/web checkouts). Standard Collect requests sent from Android or desktop are blocked, resulting in failed transactions if you have not migrated. This also covers registering a new UPI mandate by having the customer manually type their VPA, see the Mandate Execution exemption below for what still works.

**iOS is unaffected by this block for now, both the iOS app and iOS mobile web (Safari or Chrome on an iPhone or iPad). This does not extend to desktop browsers, which are covered by the restriction above.**

### Collect Exemptions: Valid Use Cases

Even on Android and desktop, UPI Collect remains a permitted and necessary integration for:

*   **Capital Markets & Broking:** For merchants operating under MCC 6211 or 6012 (IPO creation, execution and revoke, and Secondary Market use cases), Collect is still permitted and used with Third-Party Validation (TPV). It ensures the payment is pulled exactly from the investor's pre-registered bank account.
*   **Mandate Execution (AutoPay, OTM):** Recurring payments rely on the Collect architecture for execution, modification and revoke on a mandate that already exists. When a subscription is due, the merchant's server triggers a pre-authorized Collect request against the user's account, which executes automatically without requiring an additional PIN entry (within allowed limits), regardless of platform. This exemption does not cover *creating* a new mandate by manual VPA entry, that follows the same Android and desktop restriction as standard payments (iOS remains exempt). See [4.1 AutoPay](#doc-4-1) for the three supported creation modes, Intent, QR, and Collect where still permitted.
*   **eRupi vouchers:** eRupi voucher transactions are exempt from the block.
*   **PACB-related flows:** Transactions routed through PACB are exempt from the block.
