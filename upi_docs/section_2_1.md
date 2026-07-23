2.1 UPI Intent

UPI Intent is the most seamless, frictionless payment flow available for mobile users. If your customers are shopping on a mobile website or inside your Android/iOS app, this is the flow you should default to.

How it works

Instead of asking the user to type in their UPI ID (which causes typos and drop-offs) or asking them to scan a QR code (which is impossible if they are shopping on their phone), UPI Intent uses a "deep link."

When the user taps "Pay with UPI," your app/website triggers a specific link (starting with upi://pay?...). The phone's operating system instantly detects this and opens a bottom sheet showing all the UPI apps currently installed on the user's phone (Google Pay, PhonePe, Paytm, CRED, etc.).

The user taps their preferred app, the app opens with the exact payment amount pre-filled, and they just enter their PIN.

Key Benefits

Highest Success Rate: Because the user doesn't have to manually switch apps, wait for SMS notifications, or type anything, this flow boasts the highest transaction success rates in the industry.

Zero VPA Entry: Completely eliminates failed transactions due to user typos.

Native Experience: Keeps the user in a smooth, continuous flow without jarring browser redirects.

The Technical Architecture

To understand the secure integration behind the scenes, here is the technical architectural flow of UPI Intent. This details how the intent data, signatures, and encrypted payloads are routed between the Merchant App, the Payment Service Providers (PSPs), and the NPCI switch:

<img width="1198" height="533" alt="Screenshot 2026-07-23 at 5 00 03 PM" src="https://github.com/user-attachments/assets/8201d117-2075-4d7c-b362-2f4eadd5fd01" />