UPI Collect is a server to server pull mechanism. Your customer enters their UPI ID (VPA) on your checkout page, your backend sends a payment request to that VPA, and they approve it from their UPI application after receiving a notification.

<video src="UPI%20collect.mp4" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>

### The customer experience

Compared to UPI Intent, Collect adds two extra steps for your customer: waiting for a notification to arrive, and switching to their UPI application by hand rather than being taken there directly. That is why UPI Intent ([section 2.1](#doc-2-1)) is what we recommend by default for mobile checkout, and Dynamic QR ([section 2.3](#doc-2-3)) for desktop checkout.

### Where UPI Collect is restricted

Effective **February 28, 2026**, Cashfree does not accept new UPI Collect requests initiated on Android or on desktop, including requests used to register a new UPI mandate by manual VPA entry. Existing integrations on these platforms must migrate to UPI Intent for mobile checkout or Dynamic QR for desktop checkout. A Collect request sent from a restricted platform after this date will fail.

### Where UPI Collect is still allowed

*   **iOS.** Both the iOS application and iOS mobile web (Safari or Chrome on an iPhone or iPad) remain unaffected by the restriction above, for now.
*   **Capital markets and broking.** Merchants operating under MCC 6211 or 6012 (IPO and secondary market use cases) may continue to use Collect, validated against the investor's own registered bank account.
*   **Existing mandates.** Debiting, modifying, or revoking a UPI mandate that already exists (AutoPay, OTM) continues to run on Collect, on any platform. This does not extend to creating a new mandate by manual VPA entry, which follows the restriction above. See [section 4.1](#doc-4-1) for mandate creation options.
*   **eRupi vouchers and PACB flows.** Both remain exempt from the restriction.
