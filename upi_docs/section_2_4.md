UPI QR codes bridge the gap between offline and online payments, as well as desktop and mobile environments. By adhering to the interoperable BharatQR and UPI QR standards, these solutions allow customers to scan and pay using any UPI PSP app. 

Depending on your integration environment and reconciliation needs, there are three primary QR architectures you can deploy.

### 1. Static QR

A Static QR code is a fixed image that does not change. It encodes only your base merchant VPA (Virtual Payment Address) and merchant details.

* **How it works:** When a customer scans a Static QR, their app identifies the merchant, but the customer must manually type in the payment amount before entering their PIN.
* **Best for:** Small offline retail storefronts, generic donation pages, or low-tech payment collection.
* **Limitations:** Because the amount is variable and the QR does not contain a unique order ID, automated server-to-server reconciliation is very difficult. You rely on SMS notifications or manual ledger checks to confirm payments.

### 2. Dynamic QR

A Dynamic QR code is generated on the fly for every single transaction. It encodes your merchant VPA, the exact payment amount, and a unique Order ID or Reference Number.

* **How it works:** When a customer scans this QR, the amount is pre-filled and locked. The customer cannot change it; they simply enter their PIN to authorize.
* **Best for:** Desktop website checkouts, self-checkout kiosks, automated vending machines, and organized retail POS systems.
* **Benefits:** Perfect reconciliation. Because the exact Order ID is baked into the QR code, your backend instantly receives a Webhook tying the successful payment to the exact shopping cart or invoice.

### 3. POD (Pay on Demand) QR Code

POD QR (`podQR`) is a Cashfree UPI QR variant designed for pay-on-delivery / delayed-payment use cases — situations where a standard UPI QR doesn't fit because the customer isn't paying immediately at the time the QR is generated (e.g., a delivery invoice, a printed restaurant bill, or a WhatsApp/digital invoice sent ahead of collection).

**Problem with a standard UPI QR:**
* **No retries** — a failed payment attempt kills the transaction; the customer has to be issued a fresh QR/link, causing confusion and lost revenue.
* **Short TTL** — standard QR codes expire quickly, which doesn't work for invoices where payment may happen hours or days later.

**How POD QR solves this:**

| Feature | Behavior |
| :--- | :--- |
| **Payment retries allowed** | The same QR keeps working for repeated attempts until the TTL expires — no need to regenerate. |
| **Customisable TTL** | Configurable from a few hours up to 30+ days, instead of the few-minute expiry on a normal QR. |
| **Smarter session handling** | The final payment status is confirmed only after TTL expiry (via a status check), avoiding premature failures. |

**Best suited for:** Pay-on-Delivery, printed invoices, and WhatsApp/digital invoices — anywhere the payer might not pay on the first try or might pay later.
