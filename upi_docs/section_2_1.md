UPI Intent is the most seamless, frictionless payment flow available for mobile users. If your customers are shopping on a mobile website or inside your Android/iOS app, this is the flow you should default to.

### How it works

Instead of asking the user to type in their UPI ID (which causes typos and drop-offs) or asking them to scan a QR code (which is impossible if they are shopping on their phone), UPI Intent uses a "deep link."

When the user taps "Pay with UPI," your app/website triggers a specific link (starting with `upi://pay?...`). The phone's operating system instantly detects this and opens a bottom sheet showing all the UPI apps currently installed on the user's phone (Google Pay, PhonePe, Paytm, CRED, etc.).

The user taps their preferred app, the app opens with the exact payment amount pre-filled, and they just enter their PIN.

### Key Benefits

* **Highest Success Rate:** Because the user doesn't have to manually switch apps, wait for SMS notifications, or type anything, this flow boasts the highest transaction success rates in the industry.
* **Zero VPA Entry:** Completely eliminates failed transactions due to user typos.
* **Native Experience:** Keeps the user in a smooth, continuous flow without jarring browser redirects.

### The Technical Architecture

To understand the secure integration behind the scenes, here is the technical architectural flow of UPI Intent. This details how the intent data, signatures, and encrypted payloads are routed between the Merchant App, the Payment Service Providers (PSPs), and the NPCI switch:

![UPI Intent Technical Architecture](image_158674.jpg)

### The Standard Flow

1. **Checkout:** The user selects UPI on your checkout page.
2. **Order Creation:** Your backend calls the Cashfree API to create an order.
3. **Intent Invocation:** You pass the returned UPI deep link to your mobile frontend.
4. **App Selection:** The user's phone OS handles app selection natively.
5. **Authorization:** The user enters their UPI PIN in their chosen app.
6. **Return:** The UPI app pushes the user back to your app/website.
7. **Verification:** Always rely on the Server-to-Server Webhook to verify the final payment status before showing the success screen to the user.

> **Warning:** Never trust the frontend app-switch return alone to verify a payment. Always wait for the backend Webhook confirmation from Cashfree.
