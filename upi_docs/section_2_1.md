UPI Intent is the payment flow you should default to whenever your customer is checking out on a mobile device, whether that is your mobile website or your own application. It asks your customer to do only two things: select a UPI application, and enter their PIN.

<video src="upi%20intent.mp4" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>

### What the customer experiences

<figure>
<svg viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The four screens presented to the customer during UPI Intent: the checkout page, the UPI application picker, the selected application with the amount and payee already populated, and confirmation after the PIN is entered.">
<title>The customer experience during UPI Intent</title>
<desc>Four phone screens in sequence: 1) the checkout page with a Pay button, 2) a picker listing the UPI applications installed on the device, 3) the selected application opened with the amount, payee and bank account already populated, 4) a confirmation screen after the PIN is entered, noting that the webhook confirms the result.</desc>
<defs>
<marker id="cfiArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
<path d="M1 1L9 5L1 9" fill="none" stroke="#9AA5B1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>

<!-- step labels -->
<text x="90" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">1. Checkout</text>
<text x="330" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">2. Selects app</text>
<text x="570" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">3. Prefilled</text>
<text x="810" y="24" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="12" font-weight="700" fill="#111827">4. Confirmed</text>

<!-- connecting arrows -->
<line x1="170" y1="165" x2="248" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfiArrow)"/>
<text x="209" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="10.5" fill="#6B7280">selects Pay</text>

<line x1="410" y1="165" x2="488" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfiArrow)"/>
<text x="449" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="10.5" fill="#6B7280">selects app</text>

<line x1="650" y1="165" x2="728" y2="165" stroke="#9AA5B1" stroke-width="1.5" marker-end="url(#cfiArrow)"/>
<text x="689" y="150" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="10.5" fill="#6B7280">enters PIN</text>

<!-- Phone 1: Checkout -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="10" y="40" width="160" height="250" rx="22" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="10" y1="78" x2="170" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="24" y="64" font-size="13" font-weight="700" fill="#111827">Checkout</text>
<rect x="24" y="92" width="132" height="10" rx="3" fill="#F3F4F6"/>
<rect x="24" y="110" width="90" height="10" rx="3" fill="#F3F4F6"/>
<line x1="24" y1="188" x2="156" y2="188" stroke="#E5E7EB" stroke-width="1"/>
<text x="24" y="206" font-size="11.5" fill="#6B7280">Total</text>
<text x="156" y="206" text-anchor="end" font-size="13" font-weight="700" fill="#111827">₹1,240</text>
<rect x="24" y="222" width="132" height="34" rx="8" fill="#16A34A"/>
<text x="90" y="243" text-anchor="middle" font-size="12.5" font-weight="700" fill="#FFFFFF">Pay now</text>
</g>

<!-- Phone 2: App picker -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="250" y="40" width="160" height="250" rx="22" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="250" y1="78" x2="410" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="264" y="64" font-size="13" font-weight="700" fill="#111827">Pay with UPI</text>
<text x="264" y="100" font-size="10.5" fill="#6B7280">Open with</text>
<circle cx="290" cy="128" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="290" y="152" text-anchor="middle" font-size="8.5" fill="#374151">GPay</text>
<circle cx="330" cy="128" r="13" fill="#F4F0FA" stroke="#5A28A3" stroke-width="2"/>
<text x="330" y="152" text-anchor="middle" font-size="8.5" fill="#374151">PhonePe</text>
<circle cx="370" cy="128" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="370" y="152" text-anchor="middle" font-size="8.5" fill="#374151">Paytm</text>
<text x="264" y="182" font-size="10.5" fill="#6B7280">Other UPI apps</text>
<circle cx="290" cy="210" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="290" y="234" text-anchor="middle" font-size="8.5" fill="#374151">BHIM</text>
<circle cx="330" cy="210" r="13" fill="#F9FAFB" stroke="#E5E7EB" stroke-width="1.5"/>
<text x="330" y="234" text-anchor="middle" font-size="8.5" fill="#374151">and more</text>
</g>

<!-- Phone 3: prefilled -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="490" y="40" width="160" height="250" rx="22" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<line x1="490" y1="78" x2="650" y2="78" stroke="#E5E7EB" stroke-width="1"/>
<text x="504" y="64" font-size="12.5" font-weight="700" fill="#111827">Paying your store</text>
<text x="504" y="98" font-size="17" font-weight="700" fill="#111827">₹1,240</text>
<text x="504" y="120" font-size="10" fill="#6B7280">From</text>
<rect x="504" y="126" width="112" height="10" rx="3" fill="#F3F4F6"/>
<text x="504" y="168" font-size="11" fill="#374151">Enter UPI PIN</text>
<rect x="504" y="178" width="18" height="22" rx="4" fill="#F9FAFB" stroke="#D1D5DB"/>
<rect x="530" y="178" width="18" height="22" rx="4" fill="#F9FAFB" stroke="#D1D5DB"/>
<rect x="556" y="178" width="18" height="22" rx="4" fill="#F9FAFB" stroke="#D1D5DB"/>
<rect x="582" y="178" width="18" height="22" rx="4" fill="#F9FAFB" stroke="#D1D5DB"/>
<circle cx="513" cy="189" r="3.5" fill="#111827"/>
<circle cx="539" cy="189" r="3.5" fill="#111827"/>
<rect x="504" y="222" width="132" height="34" rx="8" fill="#5A28A3"/>
<text x="570" y="243" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">Approve payment</text>
</g>

<!-- Phone 4: done -->
<g font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<rect x="730" y="40" width="160" height="250" rx="22" fill="#FFFFFF" stroke="#E5E7EB" stroke-width="2"/>
<circle cx="810" cy="110" r="32" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
<polyline points="796,110 806,120 826,98" fill="none" stroke="#16A34A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<text x="810" y="168" text-anchor="middle" font-size="12.5" font-weight="700" fill="#111827">Payment received</text>
<text x="810" y="186" text-anchor="middle" font-size="10.5" fill="#6B7280">Returned to checkout</text>
<rect x="746" y="212" width="128" height="46" rx="8" fill="#F4F0FA" stroke="#DDD3EF"/>
<text x="810" y="230" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5A28A3">Confirmed via</text>
<text x="810" y="244" text-anchor="middle" font-size="9.5" fill="#6543A0">webhook</text>
</g>
</svg>
<figcaption>The customer selects Pay, chooses a UPI application from the system-generated list, and completes the payment with the amount, payee, and account details already populated. No manual data entry is required at any step.</figcaption>
</figure>

Your customer taps Pay on your checkout page. Their phone opens a list of the UPI applications installed on the device, they pick the one they use, and it opens with the payment amount, payee, and account details already filled in. They enter their UPI PIN, and control returns to your checkout page.

### Why this flow is recommended

UPI Intent avoids the two places customers usually get stuck in other UPI flows: typing a VPA by hand, which is easy to get wrong, and scanning a QR code, which does not work when your customer is checking out on the very device they would need to scan with. Because UPI Intent asks for no manual entry and no extra app switching beyond the guided flow, it completes at a higher rate than the flows that do.

### How it works

UPI Intent runs on a deep link that starts with `upi://pay?...`. When your customer taps Pay, your checkout builds this link and hands it to the phone's operating system, which checks it against every UPI application installed on the device and shows them as options. From there, Cashfree and your customer's UPI application handle the rest of the transaction between them, your side of the integration only needs to trigger the link and wait for confirmation.

### Integration options

There are three ways to trigger UPI Intent, depending on how your checkout is already built.

#### 1. Using Cashfree's SDK, or Web Checkout in a browser

This is the default path, and it works for most merchants. You do not need to write any code to show the UPI application picker, the operating system handles that natively the moment the link is triggered. It covers the Android, iOS, React Native, and Flutter SDKs, along with Cashfree's hosted Web Checkout when it opens in a mobile browser or through a full page redirect, rather than inside your own application.

> **Platform note:** On Android, the `upi://pay` link resolves consistently, since every major UPI application registers for this scheme. On iOS, it behaves the same way in Safari and inside a native application, but is less reliable inside certain in-app browsers, such as the webview used by social apps for links opened from a feed, and in some other embedded browser environments. In these cases, iOS may not raise an error, and the link can fail without any visible response to the customer. If a meaningful share of your iOS traffic comes through contexts like these, do not rely on UPI Intent alone. UPI Collect ([section 2.2](#doc-2-2)) remains available on iOS, and Dynamic QR ([section 2.3](#doc-2-3)) is an additional alternative.

#### 2. Loading Web Checkout inside your own WebView

If you embed Cashfree's Web Checkout page inside your own Android, iOS, React Native, Flutter, or Cordova application using a WebView, rather than opening it in a system browser, you are responsible for intercepting the UPI deep link yourself. A WebView does not hand off to other apps the way a system browser does, so without extra code the UPI option can show up on your checkout page and simply do nothing when your customer taps it. Cashfree still renders the checkout page in this case, only the deep link interception becomes your responsibility, and it differs by platform:

<style>
.cf-tabs{margin:20px 0 28px;border:1px solid #E5E7EB;border-radius:10px;overflow:hidden;background:#FFFFFF;}
.cf-tabs-nav{display:flex;border-bottom:1px solid #E5E7EB;background:#F9FAFB;}
.cf-tab-btn{flex:1;padding:12px 16px;font-size:14px;font-weight:600;color:#6B7280;background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;font-family:inherit;}
.cf-tab-btn:hover{color:#374151;}
.cf-tab-btn.cf-tab-active{color:#5A28A3;border-bottom:2px solid #5A28A3;background:#FFFFFF;}
.cf-tab-panel{padding:18px 20px 22px;}
.cf-tab-panel[hidden]{display:none;}
.cf-tab-panel > *:first-child{margin-top:0;}
.cf-tab-panel > *:last-child{margin-bottom:0;}
</style>

<div class="cf-tabs" data-cftabs>

<div class="cf-tabs-nav">
<button type="button" class="cf-tab-btn cf-tab-active" data-tab="android">Android</button>
<button type="button" class="cf-tab-btn" data-tab="ios">iOS</button>
</div>

<div class="cf-tab-panel" data-panel="android">

Override `shouldOverrideUrlLoading` on the `WebViewClient`, match the request URL against the required UPI schemes, confirm that a handler exists on the device, and launch it using an `ACTION_VIEW` intent.

```kotlin
override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
    val url = request.url.toString()
    val upiSchemes = listOf("upi://pay", "tez://", "gpay://", "paytmmp://", "phonepe://")
    if (upiSchemes.any { url.startsWith(it) }) {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        if (intent.resolveActivity(context.packageManager) != null) context.startActivity(intent)
        return true
    }
    return false
}
```

Cashfree also provides a feature-flag mode, in which the application picker is rendered within the checkout page directly, and a code-based mode, in which a JS bridge named `Android` is registered to handle the interaction.

<!-- Claude, this snippet is illustrative, built only from the verified method and scheme names, not copied from Cashfree's own sample repo. Point engineers to the Custom Checkout for Android guide linked below for the real, working sample. -->

</div>

<div class="cf-tab-panel" data-panel="ios" hidden>

The checkout runs inside a `WKWebView`. Every UPI application scheme to be detected (`bhim`, `paytmmp`, `phonepe`, `tez`, `credpay`, and others) must be declared under `LSApplicationQueriesSchemes` in the application's `Info.plist`, and checked with `canOpenURL` before you try to open it.

```swift
if UIApplication.shared.canOpenURL(url) {
    UIApplication.shared.open(url)
}
```

A `WKScriptMessageHandler` JS bridge allows the checkout page to query which UPI applications are installed. This integration path also requires the application's bundle ID to be whitelisted by Cashfree.

<!-- Claude, same as the Android snippet above, illustrative only. -->

</div>

</div>

<script>
(function () {
    document.querySelectorAll('[data-cftabs]').forEach(function (root) {
        if (root.dataset.cftabsBound) return;
        root.dataset.cftabsBound = '1';
        var btns = root.querySelectorAll('.cf-tab-btn');
        btns.forEach(function (btn) {
            btn.addEventListener('click', function () {
                btns.forEach(function (b) { b.classList.remove('cf-tab-active'); });
                root.querySelectorAll('.cf-tab-panel').forEach(function (p) { p.hidden = true; });
                btn.classList.add('cf-tab-active');
                root.querySelector('.cf-tab-panel[data-panel="' + btn.dataset.tab + '"]').hidden = false;
            });
        });
    });
})();
</script>

Full implementation details and sample code are available for [Custom Checkout for Android](https://www.cashfree.com/docs/payments/online/web/custom-checkout-android) and [Custom Checkout for iOS](https://www.cashfree.com/docs/payments/online/web/custom-checkout-ios).

#### 3. Integrating directly against the API

If you do not use Cashfree's SDK or Web Checkout at all, and build your own checkout interface from the ground up, you retrieve the deep link from the API rather than from a rendered checkout page. The deep link does not come back in the Create Order response, it comes from the Order Pay call, in the payload for the UPI payment method you requested.

```json
{
  "payment_method": {
    "upi": {
      "channel": "link"
    }
  }
}
```

Set `payment_method.upi.channel` to `"link"` and you get the `upi://pay?...` string directly in the response. Check the API Reference for the current field name and response shape, since this is versioned and does change. If your custom interface is itself embedded in a WebView, the interception steps above still apply to you.

> **Warning:** Never trust the frontend app-switch return alone to verify a payment. Always wait for the backend Webhook confirmation from Cashfree.

<!-- Claude, flagging for Saif: the Android/iOS Custom Checkout details were re-verified on 2026-08-28 directly against the live cashfree.com/docs/payments/online/web/custom-checkout-android and -ios pages. Those two pages are specifically about embedding Cashfree's own Web Checkout inside a WebView, they say so directly, they are not about a merchant built custom UI. The three way split above (SDK/Web Checkout in a browser, Web Checkout inside a WebView, direct API integration) reflects that. Still unconfirmed: whether "Seamless" is a distinct integration mode with its own deep-link enumeration, that is what Ayushi's original comment asked about specifically, and needs a product/eng answer rather than another doc lookup. -->
