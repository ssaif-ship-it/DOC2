UPI Collect is a server to server pull mechanism. Your customer enters their UPI ID (VPA) on your checkout page, your backend sends a payment request to that VPA, and they approve it from their UPI application after receiving a notification.

### The customer experience

<figure>
<svg viewBox="0 0 1000 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The five screens presented to the customer during UPI Collect: choosing UPI as the payment method, entering a UPI ID, a payment request waiting on the customer's UPI app with a countdown timer, approving the request inside that app, and confirmation.">
<title>The customer experience during UPI Collect</title>
<desc>Five phone screens in sequence: 1) the checkout page's payment method list with UPI selected, 2) the UPI ID entry screen with a text field and a Verify and Pay button, 3) a payment request screen with a countdown timer and a Cancel Request link, shown while the request waits on the customer's UPI app, 4) the customer's own UPI app opened to a Send screen with the amount and a Make Payment button, 5) a confirmation screen after payment, noting that the webhook confirms the result.</desc>
<defs>
<marker id="cfcArrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M1 1L9 5L1 9" fill="none" stroke="#9AA5B1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<text x="80" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">1. Selects UPI</text>
<text x="290" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">2. Enters VPA</text>
<text x="500" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">3. Request sent</text>
<text x="710" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">4. Approves</text>
<text x="920" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">5. Confirmed</text>

<line x1="150" y1="165" x2="218" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfcArrow2)"/>
<text x="184" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="9" fill="#6B7280">selects UPI</text>

<line x1="360" y1="165" x2="428" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfcArrow2)"/>
<text x="394" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="9" fill="#6B7280">submits VPA</text>

<line x1="570" y1="165" x2="638" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfcArrow2)"/>
<text x="604" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="9" fill="#6B7280">opens app</text>

<line x1="780" y1="165" x2="848" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfcArrow2)"/>
<text x="814" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="9" fill="#6B7280">approves</text>

<!-- Phone 1: payment method list -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="10" y="40" width="140" height="250" rx="20" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="10" y1="78" x2="150" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="22" y="64" font-size="12.5" font-weight="700" fill="#111827">Checkout</text>
<text x="22" y="96" font-size="9" fill="#6B7280">Select payment option</text>
<rect x="22" y="106" width="12" height="12" rx="3" fill="#F3F4F6" stroke="#E5E7EB"/>
<text x="42" y="116" font-size="9.5" fill="#374151">Card</text>
<line x1="22" y1="130" x2="138" y2="130" stroke="#F3F4F6" stroke-width="1"/>
<rect x="18" y="138" width="124" height="32" rx="7" fill="#F4F0FA" stroke="#5A28A3" stroke-width="1.5"/>
<rect x="26" y="148" width="12" height="12" rx="3" fill="#5A28A3"/>
<text x="46" y="158" font-size="9.5" font-weight="700" fill="#5A28A3">UPI</text>
<circle cx="132" cy="154" r="5" fill="#5A28A3"/>
<rect x="22" y="180" width="12" height="12" rx="3" fill="#F3F4F6" stroke="#E5E7EB"/>
<text x="42" y="190" font-size="9.5" fill="#374151">Wallets</text>
<line x1="22" y1="204" x2="138" y2="204" stroke="#F3F4F6" stroke-width="1"/>
<rect x="22" y="212" width="12" height="12" rx="3" fill="#F3F4F6" stroke="#E5E7EB"/>
<text x="42" y="222" font-size="9.5" fill="#374151">Net Banking</text>
<line x1="22" y1="236" x2="138" y2="236" stroke="#F3F4F6" stroke-width="1"/>
</g>

<!-- Phone 2: VPA entry -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="220" y="40" width="140" height="250" rx="20" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="220" y1="78" x2="360" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="232" y="64" font-size="12.5" font-weight="700" fill="#111827">Pay by UPI</text>
<text x="232" y="96" font-size="9" fill="#6B7280">Open with</text>
<circle cx="252" cy="122" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="252" y="146" text-anchor="middle" font-size="8" fill="#374151">GPay</text>
<circle cx="284" cy="122" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="284" y="146" text-anchor="middle" font-size="8" fill="#374151">PhonePe</text>
<text x="232" y="166" font-size="9" fill="#6B7280">UPI ID</text>
<rect x="232" y="172" width="116" height="26" rx="5" fill="#F9FAFB" stroke="#D1D5DB"/>
<text x="240" y="189" font-size="8.5" fill="#374151">9800000000@ybl</text>
<text x="232" y="212" font-size="7.5" fill="#9CA3AF">Format: mobilenumber@bank</text>
<rect x="232" y="222" width="116" height="32" rx="8" fill="#5A28A3"/>
<text x="290" y="242" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">Verify and Pay</text>
</g>

<!-- Phone 3: request sent, waiting -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="430" y="40" width="140" height="250" rx="20" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<text x="500" y="106" text-anchor="middle" font-size="10" font-weight="700" fill="#111827">Please accept the</text>
<text x="500" y="120" text-anchor="middle" font-size="10" font-weight="700" fill="#111827">request on your UPI app</text>
<text x="500" y="142" text-anchor="middle" font-size="8.5" fill="#6B7280">Complete the payment in</text>
<text x="500" y="154" text-anchor="middle" font-size="8.5" fill="#6B7280">your UPI application</text>
<text x="500" y="196" text-anchor="middle" font-size="19" font-weight="700" fill="#16A34A">04:08</text>
<text x="500" y="246" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5A28A3">Cancel Request</text>
</g>

<!-- Phone 4: approves inside UPI app -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="640" y="40" width="140" height="250" rx="20" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="640" y1="78" x2="780" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="652" y="64" font-size="12.5" font-weight="700" fill="#111827">Send</text>
<circle cx="710" cy="106" r="17" fill="#F4F0FA" stroke="#5A28A3" stroke-width="1.5"/>
<text x="710" y="111" text-anchor="middle" font-size="11" font-weight="700" fill="#5A28A3">S</text>
<text x="710" y="140" text-anchor="middle" font-size="10" font-weight="700" fill="#111827">Your Store</text>
<text x="710" y="162" text-anchor="middle" font-size="13" font-weight="700" fill="#111827">₹1,240</text>
<text x="652" y="192" font-size="8.5" fill="#6B7280">Debit from</text>
<rect x="652" y="198" width="12" height="12" rx="3" fill="#F3F4F6" stroke="#E5E7EB"/>
<text x="670" y="208" font-size="8" fill="#374151">Linked bank account</text>
<rect x="652" y="222" width="116" height="32" rx="8" fill="#5A28A3"/>
<text x="710" y="242" text-anchor="middle" font-size="10.5" font-weight="700" fill="#FFFFFF">Make Payment</text>
</g>

<!-- Phone 5: confirmed -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="850" y="40" width="140" height="250" rx="20" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<circle cx="920" cy="108" r="28" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
<polyline points="908,108 917,117 934,97" fill="none" stroke="#16A34A" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="920" y="162" text-anchor="middle" font-size="11.5" font-weight="700" fill="#111827">Payment received</text>
<text x="920" y="178" text-anchor="middle" font-size="9.5" fill="#6B7280">Returned to checkout</text>
<rect x="864" y="200" width="112" height="42" rx="8" fill="#F4F0FA" stroke="#DDD3EF"/>
<text x="920" y="217" text-anchor="middle" font-size="9" font-weight="700" fill="#5A28A3">Confirmed via</text>
<text x="920" y="230" text-anchor="middle" font-size="9" fill="#6543A0">webhook</text>
</g>
</svg>
<figcaption>The customer chooses UPI from the payment method list, enters their UPI ID and submits, and a payment request is sent to their UPI application. The checkout page shows a countdown while the request waits. The customer opens their UPI application, reviews the amount and the linked account, and taps Make Payment. The checkout page updates once the webhook confirms the result. Compared to UPI Intent, this adds a waiting step and a manual application switch.</figcaption>
</figure>

Compared to UPI Intent, Collect adds two extra steps for your customer: waiting for a notification to arrive, and switching to their UPI application by hand rather than being taken there directly. That is why UPI Intent ([section 2.1](#doc-2-1)) is what we recommend by default for mobile checkout, and Dynamic QR ([section 2.3](#doc-2-3)) for desktop checkout.

### Where UPI Collect is restricted

Effective **February 28, 2026**, Cashfree does not accept new UPI Collect requests initiated on Android or on desktop, including requests used to register a new UPI mandate by manual VPA entry. Existing integrations on these platforms must migrate to UPI Intent for mobile checkout or Dynamic QR for desktop checkout. A Collect request sent from a restricted platform after this date will fail.

### Where UPI Collect is still allowed

* **iOS.** Both the iOS application and iOS mobile web (Safari or Chrome on an iPhone or iPad) remain unaffected by the restriction above, for now.
* **Capital markets and broking.** Merchants operating under MCC 6211 or 6012 (IPO and secondary market use cases) may continue to use Collect, validated against the investor's own registered bank account.
* **Existing mandates.** Debiting, modifying, or revoking a UPI mandate that already exists (AutoPay, OTM) continues to run on Collect, on any platform. This does not extend to creating a new mandate by manual VPA entry, which follows the restriction above. See [section 4.1](#doc-4-1) for mandate creation options.
* **eRupi vouchers and PACB flows.** Both remain exempt from the restriction.

<!-- Claude, flagging for Saif: the February 28, 2026 date and the exemption list are carried over unchanged from the current file. I have not re-verified these against NPCI or an internal compliance source, and the project's own review notes flag the exact NPCI circular number as still unconfirmed. Do not treat this section as compliance-signed-off. -->

<!-- Claude, flagging for Saif: the diagram above is now built directly from a real screen recording of the Collect flow (payment method selection, UPI ID entry, the request-and-timer screen, the UPI app's own Send screen, and the success state), with the merchant name and bank name replaced by generic placeholders. If a real screen recording of this flow is hosted separately at some point, it can replace the diagram with a <video> embed the same way the AutoPay video in section 4.1 is embedded. -->
