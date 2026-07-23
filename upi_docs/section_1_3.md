2.1 UPI Intent

UPI Intent is the most seamless, frictionless payment flow available for mobile users. If your customers are shopping on a mobile website or inside your Android/iOS app, this is the flow you should default to.

How it works:
Instead of asking the user to type in their UPI ID (which causes typos and drop-offs) or asking them to scan a QR code (which is impossible if they are shopping on their phone), UPI Intent uses a "deep link."

When the user taps "Pay with UPI," your app/website triggers a specific link (starting with upi://pay?...). The phone's operating system instantly detects this and opens a bottom sheet showing all the UPI apps currently installed on the user's phone (Google Pay, PhonePe, Paytm, CRED, etc.).

The user taps their preferred app, the app opens with the exact payment amount pre-filled, and they just enter their PIN.

Key Benefits:

Highest Success Rate: Because the user doesn't have to manually switch apps, wait for SMS notifications, or type anything, this flow boasts the highest transaction success rates in the industry.

Zero VPA Entry: Completely eliminates failed transactions due to user typos.

Native Experience: Keeps the user in a smooth, continuous flow without jarring browser redirects.

The Standard Flow:

Checkout: The user selects UPI on your checkout page.

Order Creation: Your backend calls the Cashfree API to create an order.

Intent Invocation: You pass the returned UPI deep link to your mobile frontend.

App Selection: The user's phone OS handles app selection natively.

Authorization: The user enters their UPI PIN in their chosen app.

Return: The UPI app pushes the user back to your app/website.

Verification: Always rely on the Server-to-Server Webhook to verify the final payment status before showing the success screen to the user.