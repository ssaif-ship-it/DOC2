Flash UPI lets your customer pay with UPI entirely inside your app, without being redirected to a separate UPI application such as Google Pay, PhonePe, or BHIM. It runs on BHIM VEGA, built in partnership with Axis Bank and NPCI.

### Why this matters

A standard UPI payment sends your customer out of your app to a separate UPI application, where they choose a bank account and enter their PIN, before being sent back once the payment completes. That round trip commonly takes over twenty seconds, and every step spent outside your app is a place your customer can lose signal, get distracted, or drop off. Flash UPI removes all of those steps. The entire payment, from your customer tapping Pay to confirmation, happens inside your app in under five seconds, and they never leave it.

<!-- Claude, flagging for Saif: "over twenty seconds" and "under five seconds" come directly from Cashfree's own Flash UPI plus BHIM VEGA product deck (Google Slides, shared 2026-08-28), not from independently measured production data. Treat these as product marketing figures until confirmed against real transaction telemetry. -->

### What your customer experiences

The exact steps depend on whether your customer has used Flash UPI before, and whether they already hold a UPI ID with the partner bank.

**A returning customer who has already registered.**

1. Your customer lands on your checkout page and selects Flash UPI.
2. They enter their UPI PIN, and the payment is complete.

**A customer with an existing UPI ID at the partner bank, registering for the first time.**

1. Your customer lands on your checkout page and selects Add Bank Account.
2. They choose their SIM and grant permission to send text messages. This is what binds Flash UPI to their device.
3. Their bank account details are fetched automatically and linked to their existing UPI ID.
4. They enter their UPI PIN, and the payment is complete.

**A customer who has used UPI before, but not with the partner bank.**

1. Your customer lands on your checkout page and selects Add Bank Account.
2. They choose their SIM and grant permission to send text messages, which binds the device.
3. They pick their bank from the list, and every account they hold there is fetched.
4. A new UPI ID is created in the format `mobilenumber@axis`, and linked to any account that already has a UPI PIN set.
5. They enter their UPI PIN, and the payment is complete.

**A customer who has never used UPI.**

1. Your customer lands on your checkout page and selects Add Bank Account.
2. They choose their SIM and grant permission to send text messages, which binds the device.
3. They pick their bank from the list, and every account they hold there is fetched.
4. Since no UPI PIN exists yet, they are asked for their debit card details and an OTP to set one.
5. They enter their new UPI PIN, and the payment is complete.

<img width="1728" height="1136" alt="8aa94f95-ac3e-458d-a29b-fa5daef220f3" src="https://github.com/user-attachments/assets/3827df1c-ea2a-453c-9efd-8486f6c363c9">

### Why it is faster and more reliable

Two things make this possible. Device binding, done once through SMS permission, is what lets Cashfree recognise your customer's device on every later payment, without sending them anywhere else to prove who they are. And multi bank dynamic routing means a payment is not locked to a single fixed path between your customer's bank and yours, if one route is slow or unavailable, the payment can move to another. A standard UPI plugin typically binds a payment to one fixed payer and payee route, and cannot do this.

### Who this fits best

Flash UPI is built for businesses where checkout speed and repeat, high frequency payments matter most, ride hailing, food delivery, and other checkouts your customer returns to often, where every extra second before confirmation costs you conversions.

### Before you build on it

Flash UPI's partner bank is Axis Bank. Any new UPI ID Flash UPI creates for a customer who did not already have one carries the `@axis` handle, regardless of which bank the customer actually holds their account with, since the UPI ID belongs to the partner bank relationship rather than the customer's own bank.

<!-- Claude, flagging for Saif: eligibility, onboarding requirements and pricing for merchants who want to enable Flash UPI are not covered in this section or in the source deck. If there is a merchant facing activation process (comparable to the SoftPOS activation flow in 2.4), it belongs here. -->

### Benefits

* **A faster, smoother checkout.** Your customer completes payment in one screen, with no app switching.
* **Higher success rates.** Cashfree's own product materials state 10 to 15 percent higher success rates than a standard UPI redirect flow, driven by multi bank routing and the removal of redirect related failures. This is a meaningful increase from what this section previously stated, 4 to 5 percent, see the flag above.
* **A fully in-app experience.** With no redirection, you keep control over the customer journey from start to finish, and full visibility into where a payment succeeds or fails.
* **No dependency on third party UPI applications.** Payments do not route through an external UPI application, which removes a common source of timeouts and gives you clearer visibility when a payment does fail.

<!-- Claude, flagging for Saif: the 10 to 15 percent figure and the 4 to 5 percent figure it replaces cannot both be right, and I have not been able to verify either against real data, only against Cashfree's own marketing deck. Please confirm which number, if either, is safe to publish before this goes live. -->
