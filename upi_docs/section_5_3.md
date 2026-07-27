5.3 Standard Error Codes
========================

This guide outlines standard non-technical business failures, network response codes, and error normalization rules in UPI processing. It helps engineering and customer support teams distinguish between recoverable user errors, bank outages, and compliance blocks to optimize checkout retry paths.

1\. Overview & Error Architecture
---------------------------------

When a UPI transaction fails, the failure signal originates at one of three layers before being reported back to your application:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   [ Customer / UPI App ] ---> [ NPCI Switch / Remitter Bank ] ---> [ Gateway / Switch ] ---> [ Merchant Backend ]        (User Error)                 (Bank/Network Error)             (Normalized API)            (Handled Code)   `

1.  **User / Account Errors (Business Failures):** Actionable issues originating from customer state (e.g., entering an incorrect PIN, insufficient account balance, or breaching daily limits).
    
2.  **Bank / Switch Errors (Technical Failures):** Infrastructure issues at the remitter bank's Core Banking System (CBS) or NPCI routing switch.
    
3.  **Compliance & Policy Blocks:** Failures triggered by regulatory guardrails (e.g., TPV account mismatch, restricted MCC flow block, or 24-hour velocity caps).
    

### Gateway Error Payload Structure

To abstract bank-specific error strings across different acquirers, the gateway returns a standardized error contract in both API responses and webhooks:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   {    "event": "PAYMENT_FAILED",    "data": {      "order_id": "order_99887766",      "cf_payment_id": 18294021,      "payment_status": "FAILED",      "error_details": {        "error_code": "INSUFFICIENT_FUNDS",        "error_type": "USER_ERROR",        "error_subcode": "ZA",        "error_message": "The customer account has insufficient funds to complete the transaction.",        "raw_bank_response": "ZA - REMITTER BANK INSUFFICIENT BALANCE"      }    }  }   `

2\. Master NPCI Error Code & Business Failure Mapping
-----------------------------------------------------

The table below maps standard NPCI error codes, raw bank responses, root causes, and recommended user/checkout actions:

NPCI Code

Gateway Error Code

Root Cause / Business Context

Category

Recommended Action / UI Guidance

**ZA**

INSUFFICIENT\_FUNDS

Remitter account balance is lower than transaction amount.

User Error

Prompt user to choose another bank account, RuPay Credit Card, or alternative payment method. Do not retry automatically.

**ZM**

INCORRECT\_PIN

Customer entered an incorrect 4-digit or 6-digit UPI PIN.

User Error

Prompt customer to re-enter PIN carefully or reset UPI PIN in their UPI app.

**Z6**

PIN\_ATTEMPTS\_EXCEEDED

Customer entered an incorrect UPI PIN 3 consecutive times; account blocked for 24h.

User Error

Instruct customer to wait 24 hours or reset PIN using their debit card in their UPI app.

**ZK**

ACCOUNT\_BLOCKED

Customer's bank account is frozen, inactive, or restricted by the issuing bank.

Compliance / Risk

Advise customer to contact their issuing bank to remove account blocks.

**U16**

TRANSACTION\_LIMIT\_EXCEEDED

Transaction exceeds daily per-transaction cap ($\\text{₹}1,00,000$ standard P2M or $\\text{₹}5,00,000$ special MCC cap).

Limit Error

Request customer to split order amount or use NetBanking / Credit Card.

**U30**

NEW\_USER\_VELOCITY\_CAP

Customer registered, changed device, or reset PIN within the last 24 hours (capped at $\\text{₹}5,00,000 \\rightarrow \\text{₹}5,000$).

Anti-Fraud Cap

Show message: _"UPI limit capped at ₹5,000 for 24 hours following phone/PIN setup. Please pay using NetBanking."_

**U19**

TPV\_ACCOUNT\_MISMATCH

Paid account does not match registered investor account details (MCC 6211 Capital Markets).

Compliance Block

Inform user that payment must originate strictly from their pre-registered bank account.

**U01**

VPA\_NOT\_FOUND

Virtual Payment Address (VPA / UPI ID) entered does not exist or handle is deleted.

Input Error

Prompt user to re-check and type a valid UPI handle (e.g., name@upi).

**U69**

COLLECT\_BLOCKED\_FOR\_MCC

Collect request initiated for an MCC restricted to Intent/QR only (Gaming 5816, Wallet 6540, Rent 6513).

Integration Block

Switch checkout implementation to **UPI Intent** or **Dynamic QR** flow.

**U14**

ENCRYPTION\_ERROR

Device Common Library (CL) token expired or cryptographic handshake failed.

Technical

Ask user to retry transaction or restart their UPI app.

**U66**

CBS\_UNREACHABLE

Remitter bank Core Banking System (CBS) is temporarily down or timed out.

Network Failure

Automatically retry via secondary acquiring route or show bank outage status.

3\. High-Priority Business Scenarios & Edge Cases
-------------------------------------------------

### 3.1 Third-Party Verification (TPV) Failures (U19)

In investment and capital markets flows (MCC 6211 / 6012), regulatory mandates require validating the remitter account against customer record.

*   **Trigger:** Customer initiates a payment using a UPI ID linked to Account $A$, but registered profile has Account $B$.
    
*   **Gateway Action:** Transaction is aborted before money leaves the bank, failing with TPV\_ACCOUNT\_MISMATCH.
    
*   $$\\text{Expected Account: } \\text{XXXX-XXXX-}1234$$
    

### 3.2 The 24-Hour Velocity Cooling-Off Rule (U30)

To prevent account takeover fraud, NPCI caps transactions at $\\text{₹}5,000$ for 24 hours after:

1.  Initial UPI registration on a device.
    
2.  Device binding/SIM change.
    
3.  UPI PIN reset/change.
    

If an order is $\\text{₹}15,000$, NPCI will decline the transaction with code U30 even if the user has ample account balance. Checkouts should detect U30 and offer non-UPI fallback instruments.

### 3.3 Restricted Flow Errors (U69)

Attempting to send a "pull" (Collect) request for restricted business categories results in an immediate U69 rejection.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   [Merchant App] -- Collect Request (MCC 5816) --> [NPCI Switch] -- REJECT (U69: Collect Blocked) --> [Merchant]   `

To resolve this permanently, merchants operating in restricted MCCs must eliminate VPA entry screens and use **UPI Intent Deep Links** or **Dynamic QR Codes**.

4\. Merchant Retry Matrix & Smart Logic
---------------------------------------

Not all errors should trigger an automated retry. The decision tree below details how checkout frontend applications should handle specific failure states:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML                          `[ Payment Failure Received ]                                         |                  +----------------------+----------------------+                  |                                             |         [ User-Fixable Error ]                      [ Technical / Network ]     (ZA, ZM, U01, U16, U19, U30)                       (U66, U14, B1, Timeout)                  |                                             |     Do NOT retry automatically.                     Can retry automatically!     Show actionable UI alert.                      Route to backup acquirer node     Prompt user for input/fallback.                or allow 1 immediate auto-retry.`

### Action Logic Summary

1.  **INSUFFICIENT\_FUNDS / INCORRECT\_PIN:** Display inline prompt. Do **not** trigger background retries.
    
2.  **CBS\_UNREACHABLE / SYSTEM\_TIMEOUT:** Gateway handles internal retry across healthy bank pipes. If terminal failure is reached, offer a 1-click retry button.
    
3.  **TRANSACTION\_LIMIT\_EXCEEDED:** Do not offer retry with UPI. Instantly toggle checkout tab to Credit/Debit Cards or NetBanking.
    

5\. Webhook Integration Checklist for Failure Handling
------------------------------------------------------

*   \[ \] **Subscribe to PAYMENT\_FAILED Webhooks:** Ensure backend listens for terminal failure webhooks to release reserved inventory immediately.
    
*   \[ \] **Parse Subcode Metadata:** Store error\_subcode and raw\_bank\_response in transaction logs for analytics and support debugging.
    
*   \[ \] **Filter Non-Actionable Alerts:** Do not trigger internal engineering alerts for customer-driven errors (ZA, ZM); monitor spike rates only for infrastructure errors (U66, B1).
    
*   \[ \] **Synchronize Order Lifecycle:** Ensure stock allocation is unblocked instantly when U19 (TPV Mismatch) or U69 (Collect Blocked) occurs.