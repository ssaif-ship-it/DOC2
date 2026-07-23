UPI Collect is a standard server-to-server "pull" mechanism. In this flow, the customer provides their Virtual Payment Address (VPA/UPI ID) on your checkout page. Your backend then sends a payment request directly to that VPA. The user receives a push notification or SMS, opens their UPI app (like Google Pay or PhonePe), and enters their PIN to authorize the transaction.

While this was once a standard integration, it inherently introduces friction (users must wait for network notifications and manually switch apps) and yields lower success rates compared to UPI Intent.

### NPCI Sunset Guidelines (Effective February 2026)

To combat payment spam, reduce unauthorized mandate requests, and push the ecosystem towards higher-converting flows, the NPCI deprecated standard P2M (Person-to-Merchant) Collect flows effective **February 2026**.

For standard e-commerce and retail transactions, merchants are now strictly required to default to **UPI Intent** (for mobile checkouts) or **Dynamic QR Codes** (for desktop/web checkouts). Standard Collect requests sent for everyday retail transactions are heavily throttled or proactively blocked by the NPCI Switch, resulting in failed transactions and potential compliance warnings.

### Collect Exemptions: Valid Use Cases

The sunset of standard P2M Collect does not mean the architecture is entirely dead. Strict exemptions exist where UPI Collect remains a permitted, compliant, and necessary integration:

* **Capital Markets & Broking (TPV):** For merchants operating under MCC 6211 or 6012, Collect is still permitted and heavily utilized in tandem with Third-Party Verification (TPV). It ensures the payment is pulled exactly from the investor's pre-registered bank account.
* **Desktop-to-Mobile Flows:** When a user is checking out on a desktop computer and chooses to type in their UPI ID rather than scanning a QR code, a Collect request is necessary to push the authorization prompt to their mobile phone.
* **iOS Platform Limitations:** In certain hybrid app environments or specific iOS browser flows where standard deep linking (Intent) fails or is blocked by the OS, Collect acts as an approved fallback mechanism to ensure the user can still pay.
* **Mandate Execution (AutoPay):** Recurring payments rely entirely on the Collect architecture. When a subscription is due, the merchant's server triggers a pre-authorized Collect request against the user's account, which executes automatically without requiring an additional PIN entry (within allowed limits).
