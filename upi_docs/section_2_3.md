UPI QR codes bridge the gap between offline and online payments, as well as desktop and mobile environments. By adhering to the interoperable BharatQR and UPI QR standards, these solutions allow customers to scan and pay using any UPI PSP app.

Depending on your integration environment and reconciliation needs, there are three primary QR architectures you can deploy.

### 1. Static QR

<!-- Claude, flagging for Saif: leaving space for a Static QR photo here too, please upload one (drag it into a GitHub comment or issue to get a user-attachments URL, the same way the 2.6 and 4.1 images and video got added) and I will wire it in right away. -->

A Static QR code is a fixed image that does not change. It encodes only your base merchant VPA (Virtual Payment Address) and merchant details.

*   **How it works:** When a customer scans a Static QR, their app identifies the merchant, but the customer must manually type in the payment amount before entering their PIN. Because the QR carries no order ID, matching a payment back to a specific order relies on SMS notifications or manual ledger checks rather than automated reconciliation.
*   **Best for:** Offline-only merchants with no website or app, and no way to generate a QR per order or transaction, i.e. situations where the QR genuinely cannot be loaded dynamically. Payment is collected in person, at a fixed counter or standee, in close proximity to the customer. If you sell online, deliver, or invoice remotely instead, move to Dynamic QR below, it solves this by putting the order ID in the QR itself.

### 2. Dynamic QR

A Dynamic QR code is generated on the fly for every single transaction. It encodes your merchant VPA, the exact payment amount, and a unique Order ID or Reference Number.

*   **How it works:** When a customer scans this QR, the amount is pre-filled and locked. The customer cannot change it; they simply enter their PIN to authorize.
*   **Best for:** Desktop website checkouts, self-checkout kiosks, automated vending machines, and organized retail POS systems.
*   **Benefits:** Perfect reconciliation. Because the exact Order ID is baked into the QR code, your backend instantly receives a Webhook tying the successful payment to the exact shopping cart or invoice.
*   **How you generate it:** Create the order with `POST /orders`, then call Order Pay with `payment_method.upi.channel` set to `"qrcode"`. The response gives you the QR payload to render, already carrying that order's ID. See [3.2 Step 5](#doc-3-2) for the full request shape.

## 3. POD QR

<!-- Claude, flagging for Saif: you asked for an image here. I do not have a POD QR flow diagram to embed, please upload one (drag it into a GitHub comment or issue to get a user-attachments URL, the same way the 2.6 and 4.1 images and video got added) and I will wire it in right away. -->

POD QR (podQR) is a Cashfree UPI QR variant designed for **pay-on-delivery / delayed-payment** use cases, that is, situations where a standard UPI QR does not fit because your customer is not paying immediately at the time the QR is generated (a delivery invoice, a printed restaurant bill, or a WhatsApp/digital invoice sent ahead of collection).

### What POD QR Gives You

| Feature | Behavior |
| :-- | :-- |
| **Payment retries allowed** | The *same* QR keeps working for repeated attempts, so you never need to regenerate one for your customer. |
| **A TTL built for delay** | Configurable from a few hours up to 30+ days, so the QR stays valid for as long as your customer actually takes to pay. |
| **Smarter session handling** | The final payment status is confirmed only after the TTL expires, via a status check, so a slow payer never registers as a premature failure. |

**Best suited for:** Pay-on-Delivery, printed invoices, and WhatsApp or digital invoices, that is, anywhere the payer might not pay on the first try or might pay later.

---
