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

### 3. POD QR (Pay-on-Delivery)

POD QR is a specialized application of Dynamic QR built specifically for the logistics, e-commerce, and food delivery sectors to digitize "Cash on Delivery" (COD) orders.

* **How it works:** When a delivery agent reaches the customer's doorstep, the agent's handheld device or app generates a Dynamic QR for the exact invoice amount. The customer scans the agent's screen to pay. 
* **Benefits:** 
  * **Cash Reduction:** Drastically reduces cash-handling costs, theft risks, and the hassle of carrying exact change.
  * **Instant Agent Confirmation:** The delivery agent's app receives real-time confirmation via Webhook the moment the payment succeeds, allowing them to instantly hand over the package.
  * **Status Tracking:** If a transaction gets stuck in a "Pending" state, the backend can manage the timeout gracefully, preventing the agent from waiting indefinitely.
