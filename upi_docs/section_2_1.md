UPI Intent hands your customer directly to their own UPI application to complete the payment, rather than asking them to type a VPA or scan a QR code. Default to this flow whenever your customer is checking out on a mobile device, whether that is your mobile website or your own application.

<video src="upi%20intent.mp4" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>

### What the customer experiences

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
