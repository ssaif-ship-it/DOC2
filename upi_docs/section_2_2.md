UPI Collect is a standard server-to-server "pull" mechanism. In this flow, the customer provides their Virtual Payment Address (VPA/UPI ID) on your checkout page. Your backend then sends a payment request directly to that VPA. The user receives a push notification or SMS, opens their UPI app (like Google Pay or PhonePe), and enters their PIN to authorize the transaction.

While this was once a standard integration, it inherently introduces friction (users must wait for network notifications and manually switch apps) and yields lower success rates compared to UPI Intent.

### Collect Restriction on Android (Effective February 28, 2026)

To combat payment spam and push the ecosystem towards higher-converting flows, Cashfree has blocked UPI Collect requests on Android, effective **February 28, 2026**, in line with NPCI's broader direction of moving merchant collections towards UPI Intent and QR.

For standard e-commerce and retail transactions on Android, merchants are now required to default to **UPI Intent** (for mobile checkouts) or **Dynamic QR Codes** (for desktop/web checkouts). Standard Collect requests sent for everyday retail transactions on Android are blocked, resulting in failed transactions if you have not migrated.

**iOS mobile app and mobile web transactions are unaffected by this block for now.**

### Collect Exemptions: Valid Use Cases

Even on Android, UPI Collect remains a permitted and necessary integration for:

*   **Capital Markets & Broking (TPV):** For merchants operating under MCC 6211 or 6012 (IPO creation, execution and revoke, and Secondary Market use cases), Collect is still permitted and used with Third-Party Validation (TPV). It ensures the payment is pulled exactly from the investor's pre-registered bank account.
*   **Mandate Execution (AutoPay, OTM):** Recurring payments rely on the Collect architecture for execution, modification and revoke. When a subscription is due, the merchant's server triggers a pre-authorized Collect request against the user's account, which executes automatically without requiring an additional PIN entry (within allowed limits).
*   **eRupi vouchers:** eRupi voucher transactions are exempt from the block.
*   **PACB-related flows:** Transactions routed through PACB are exempt from the block.
*   **Desktop-to-Mobile Flows:** When a user is checking out on a desktop computer and chooses to type in their UPI ID rather than scanning a QR code, a Collect request is necessary to push the authorization prompt to their mobile phone.
