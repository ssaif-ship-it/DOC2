## 1. Overview & Error Architecture

When a UPI transaction or recurring debit fails, the failure signal originates at one of three layers before being reported back to your application:

<div class="cf-flow-wrap">
  <style>
    .cf-flow-wrap {
      margin: 20px 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .cf-flow {
      display: flex;
      align-items: stretch;
      flex-wrap: nowrap;
      gap: 8px;
    }
    .cf-flow-step {
      flex: 1 1 0;
      min-width: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      background: #F9FAFB;
      color: #1f2933;
      border: 1px solid #E5E7EB;
      border-top: 3px solid #5A28A3;
      border-radius: 8px;
      padding: 12px 10px;
      text-align: center;
    }
    .cf-flow-title {
      font-size: 12.5px;
      font-weight: 600;
      line-height: 1.35;
      color: #1f2933;
    }
    .cf-flow-caption {
      margin-top: 7px;
      font-size: 11.5px;
      color: #6b7684;
      font-weight: 500;
      letter-spacing: 0.2px;
    }
    .cf-flow-arrow {
      flex: 0 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #5A28A3;
      font-size: 18px;
      font-weight: 700;
      min-width: 14px;
    }
    @media (max-width: 680px) {
      .cf-flow { flex-direction: column; }
      .cf-flow-step { width: 100%; }
      .cf-flow-title { font-size: 14px; }
      .cf-flow-caption { font-size: 12.5px; }
      .cf-flow-arrow { transform: rotate(90deg); padding: 2px 0; }
    }
  </style>
  <div class="cf-flow">
    <div class="cf-flow-step">
      <div class="cf-flow-title">Customer / UPI App</div>
      <div class="cf-flow-caption">User Error</div>
    </div>
    <div class="cf-flow-arrow">&rarr;</div>
    <div class="cf-flow-step">
      <div class="cf-flow-title">NPCI Switch / Remitter Bank</div>
      <div class="cf-flow-caption">Bank / Network Error</div>
    </div>
    <div class="cf-flow-arrow">&rarr;</div>
    <div class="cf-flow-step">
      <div class="cf-flow-title">Gateway / Switch</div>
      <div class="cf-flow-caption">Normalized API</div>
    </div>
    <div class="cf-flow-arrow">&rarr;</div>
    <div class="cf-flow-step">
      <div class="cf-flow-title">Merchant Backend</div>
      <div class="cf-flow-caption">Handled Code</div>
    </div>
  </div>
</div>

1.  **User / Account Errors (Business Failures):** Actionable issues originating from customer state (e.g., entering an incorrect PIN, insufficient account balance, or breaching daily limits).
2.  **Bank / Switch Errors (Technical Failures):** Infrastructure issues at the remitter bank's Core Banking System (CBS) or NPCI routing switch.
3.  **Compliance & Policy Blocks:** Failures triggered by regulatory guardrails (e.g., TPV account mismatch, restricted MCC flow block, or 24-hour velocity caps).
4.  **AutoPay & Mandate State Failures:** Failures specific to recurring mandate executions (e.g., paused/revoked mandates, missing 24h pre-debit notifications, or sequence number desynchronization).

### Gateway Error Payload Structure

To abstract bank-specific error strings across different acquirers, the gateway returns a standardized error contract in both API responses and webhooks:

```json
{
  "event": "PAYMENT_FAILED",
  "data": {
    "order_id": "order_99887766",
    "cf_payment_id": 18294021,
    "payment_status": "FAILED",
    "error_details": {
      "error_code": "INSUFFICIENT_FUNDS",
      "error_type": "USER_ERROR",
      "error_subcode": "ZA",
      "error_message": "The customer account has insufficient funds to complete the transaction.",
      "raw_bank_response": "ZA - REMITTER BANK INSUFFICIENT BALANCE"
    }
  }
}
```

## 2. Master NPCI Error Code & Business Failure Mapping

The table below lists every NPCI and gateway error code Cashfree currently maps, with the failure category and a plain language explanation of what happened. Search across all columns, filter any single column, or click a column heading to sort.

<section id="cf-errors">
  <style>
    #cf-errors{
      --cf-bg:#ffffff;
      --cf-fg:#1f2933;
      --cf-muted:#6b7684;
      --cf-border:#E5E7EB;
      --cf-border-strong:#cbd2d9;
      --cf-accent:#5A28A3;
      --cf-accent-soft:#F4F0FA;
      --cf-head-bg:#F9FAFB;
      --cf-row-hover:#FAFAFB;
      --cf-radius:8px;
      --cf-mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;

      box-sizing:border-box;
      background:var(--cf-bg);
      color:var(--cf-fg);
      padding:1.25rem;
      border:1px solid var(--cf-border);
      border-radius:var(--cf-radius);
      font-family:inherit;
      font-size:14px;
      line-height:1.5;
      margin:1.5rem 0;
    }
    #cf-errors *,#cf-errors *::before,#cf-errors *::after{box-sizing:border-box;}

    #cf-errors .cf-head{display:flex;gap:.75rem;align-items:center;margin-bottom:1rem;}
    #cf-errors .cf-tools{display:flex;gap:.5rem;align-items:center;flex:1;flex-wrap:wrap;}

    #cf-errors input[type=search],
    #cf-errors input[type=text],
    #cf-errors select{
      font:inherit;font-size:.8125rem;color:var(--cf-fg);background:var(--cf-bg);
      border:1px solid var(--cf-border-strong);border-radius:6px;
      padding:.4rem .55rem;width:100%;min-width:0;
      transition:border-color .12s ease,box-shadow .12s ease;
    }
    #cf-errors input::placeholder{color:var(--cf-muted);opacity:.85;}
    #cf-errors input:focus,#cf-errors select:focus{
      outline:none;border-color:var(--cf-accent);
      box-shadow:0 0 0 3px color-mix(in srgb,var(--cf-accent) 18%,transparent);
    }
    #cf-errors .cf-global{min-width:230px;}
    #cf-errors .cf-btn{
      font:inherit;font-size:.8125rem;cursor:pointer;white-space:nowrap;
      background:var(--cf-bg);color:var(--cf-fg);
      border:1px solid var(--cf-border-strong);border-radius:6px;padding:.4rem .7rem;
    }
    #cf-errors .cf-btn:hover:not(:disabled){border-color:var(--cf-accent);color:var(--cf-accent);}
    #cf-errors .cf-btn:disabled{opacity:.45;cursor:default;}

    #cf-errors .cf-scroll{
      overflow-x:auto;border:1px solid var(--cf-border);
      border-radius:var(--cf-radius);-webkit-overflow-scrolling:touch;
    }
    #cf-errors table{width:100%;border-collapse:collapse;font-size:.875rem;margin:0;}
    #cf-errors thead th{
      background:var(--cf-head-bg);text-align:left;font-weight:600;
      padding:0;border-bottom:1px solid var(--cf-border);vertical-align:top;
    }
    #cf-errors .cf-sortbtn{
      display:flex;align-items:center;gap:.35rem;width:100%;
      font:inherit;font-weight:600;color:inherit;background:none;border:0;
      padding:.6rem .7rem .5rem;cursor:pointer;text-align:left;
    }
    #cf-errors .cf-sortbtn:hover{color:var(--cf-accent);}
    #cf-errors .cf-arrow{font-size:.65rem;opacity:.3;transition:opacity .12s;}
    #cf-errors th[aria-sort="ascending"] .cf-arrow,
    #cf-errors th[aria-sort="descending"] .cf-arrow{opacity:1;color:var(--cf-accent);}
    #cf-errors .cf-filtercell{padding:0 .5rem .55rem;}

    #cf-errors tbody td{
      padding:.6rem .7rem;border-bottom:1px solid var(--cf-border);
      vertical-align:top;
    }
    #cf-errors tbody tr:last-child td{border-bottom:0;}
    #cf-errors tbody tr:hover{background:var(--cf-row-hover);}
    #cf-errors td.cf-code{
      font-family:var(--cf-mono);font-size:.8125rem;font-weight:600;
      white-space:nowrap;color:var(--cf-accent);
    }
    #cf-errors .cf-pill{
      display:inline-block;padding:.14rem .5rem;border-radius:999px;
      background:var(--cf-accent-soft);color:var(--cf-accent);
      font-size:.75rem;font-weight:600;white-space:nowrap;
    }
    #cf-errors mark{background:#FEF08A;color:inherit;border-radius:2px;padding:0 1px;}
    #cf-errors .cf-empty{padding:2.25rem 1rem;text-align:center;color:var(--cf-muted);}

    #cf-errors .cf-foot{
      display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;
      justify-content:space-between;margin-top:.9rem;font-size:.8125rem;color:var(--cf-muted);
    }
    #cf-errors .cf-pager{display:flex;gap:.3rem;align-items:center;}
    #cf-errors .cf-pager .cf-btn{padding:.3rem .6rem;min-width:32px;text-align:center;}
    #cf-errors .cf-pager .cf-btn[aria-current="true"]{
      background:var(--cf-accent);border-color:var(--cf-accent);color:#fff;
    }
    #cf-errors .cf-size{display:flex;gap:.4rem;align-items:center;}
    #cf-errors .cf-size select{width:auto;padding:.3rem 1.5rem .3rem .5rem;}
    @media (max-width:640px){
      #cf-errors{padding:1rem;}
      #cf-errors table{min-width:720px;}
    }
    @media (prefers-reduced-motion:reduce){#cf-errors *{transition:none!important;}}
  </style>

  <div class="cf-head">
    <div class="cf-tools">
      <input type="search" class="cf-global" data-cf="global" placeholder="Search all columns, e.g. a code or a keyword" aria-label="Search all columns">
      <button type="button" class="cf-btn" data-cf="reset">Clear</button>
    </div>
  </div>

  <div class="cf-scroll">
    <table data-cf="table">
      <thead data-cf="thead"></thead>
      <tbody data-cf="tbody"></tbody>
    </table>
  </div>

  <div class="cf-foot">
    <span data-cf="count">Loading...</span>
    <div class="cf-size">
      <label for="cf-pagesize">Rows</label>
      <select id="cf-pagesize" data-cf="pagesize">
        <option>10</option><option selected>20</option><option>50</option><option>100</option>
      </select>
    </div>
    <div class="cf-pager" data-cf="pager"></div>
  </div>

<script>
(function () {
  "use strict";

  /* Every mapped NPCI and gateway error code Cashfree tracks today. Search or
     sort any column below. This list lives here, not in a separate page, so
     it can never drift from what the docs say. */
  var ERROR_CODES = [
    ["Error Code","Category","Reason","Description"],
    ["U07","Gateway Error","Invalid Format","Gateway infrastructure error detected."],
    ["U10","Gateway Error","Invalid Format","Gateway infrastructure error detected."],
    ["U12","Gateway Error","Currency Mismatch","Gateway infrastructure error detected."],
    ["U15","Gateway Error","Encryption Error","Gateway infrastructure error detected."],
    ["U18","Transaction Declined","Auth Failure","Customer could not be authenticated for the transaction."],
    ["U36","Gateway Error","Response Error","Gateway infrastructure error detected."],
    ["SP","Transaction Declined","Invalid ATM PIN","Issuer bank or payment service provider declined the transaction."],
    ["U02","Transaction Declined","Transaction Amount Limit","Customer has exceeded the withdrawal amount limit."],
    ["U04","Gateway Error","Invalid Transaction","Transaction was invalid."],
    ["U06","Gateway Error","Invalid Transaction","Transaction was invalid."],
    ["U08","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["U24","Transaction Declined","Auth Timeout","Issuer bank or payment service provider declined the transaction."],
    ["OC","Transaction Declined","Credit Failed","Issuer bank or payment service provider declined the transaction."],
    ["RB","Network Error","Credit Reversal Timeout","A network infrastructure error was detected."],
    ["RN","Payment Instrument Blocked","Attempts Exceeded","Customer's payment instrument was blocked by the network."],
    ["RR","Network Error","Debit Reversal Timeout","A network infrastructure error was detected."],
    ["U01","Gateway Error","Duplicate Transaction","Gateway infrastructure error detected."],
    ["U20","Transaction Declined","Auth Timeout","Issuer bank or payment service provider declined the transaction."],
    ["NC","Transaction Declined","Credit Failed","Issuer bank or payment service provider declined the transaction."],
    ["U29","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["AJ","Transaction Declined","Inactive Card","Issuer bank or payment service provider declined the transaction."],
    ["BT","Network Error","Acquirer Bank Offline","A network infrastructure error was detected."],
    ["U05","Gateway Error","Invalid Format","Gateway infrastructure error detected."],
    ["U32","Transaction Declined","Credit Failed","Issuer bank or payment service provider declined the transaction."],
    ["U34","Transaction Declined","Transaction Reverted","Issuer bank or payment service provider declined the transaction."],
    ["U38","Gateway Error","Response Error","Gateway infrastructure error detected."],
    ["LD","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["ZX","Transaction Declined","Account Inactive Customer","Issuer bank or payment service provider declined the transaction."],
    ["XJ","Transaction Declined","Unknown Error","Issuer bank or payment service provider declined the transaction."],
    ["U88","Network Error","Network Timeout","A network infrastructure error was detected."],
    ["S0","Transaction Declined","PSP Decline Spam","Payment service provider declined the transaction."],
    ["XN","Transaction Declined","No Card Customer","Issuer bank or payment service provider declined the transaction."],
    ["XT","Transaction Declined","Cutoff Time","Issuer bank or payment service provider declined the transaction."],
    ["XY","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["YE","Transaction Declined","Account Blocked Customer","Issuer bank or payment service provider declined the transaction."],
    ["Z6","Transaction Declined","Pin Try Exceeded","Allowed number of pin retry exceeded."],
    ["M5","Payment Instrument Blocked","Account Closed","Customer's payment instrument was blocked by the network."],
    ["400","Transaction Declined","Invalid Phone Number","Entered phone number against this transaction is invalid."],
    ["403","Transaction Declined","Unauthorized User","User is not authorized to perform this action. Reach out to issuer bank."],
    ["L05","Network Error","Unknown Network Error","A network infrastructure error was detected."],
    ["NA","Transaction Declined","Unknown Error","Issuer bank or payment service provider declined the transaction."],
    ["U48","Transaction Cancelled","Customer Inactive","Transaction was cancelled or unattempted."],
    ["VK","Transaction Declined","Transaction Amount Limit","Customer has exceeded the withdrawal amount limit."],
    ["R02","Validation Failure","Invalid VPA","Customer's payment instrument was not setup properly."],
    ["U78","Technical Failure","Credit Failed","Beneficiary bank is not available."],
    ["U85","Network Error","Network Timeout","A network infrastructure error was detected."],
    ["51","Transaction Declined","Insufficient Funds","Customer account does not have sufficient balance."],
    ["XL","Transaction Declined","Expired Card","Transaction declined as the card is expired or incorrect expiry date is entered."],
    ["XR","Transaction Declined","Restricted By Bank","Issuer bank or payment service provider declined the transaction."],
    ["YD","Transaction Declined","Payment Not Allowed","Payment to this beneficiary is declined."],
    ["57","Transaction Declined","Account Holder Restricted","Account of the customer is restricted by the bank for the transaction ."],
    ["S1","Transaction Declined","Fraud Detected","Issuer bank or payment service provider declined the transaction."],
    ["500","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["404","Validation Failure","Invalid Google Pay User","User is not a valid Google Pay user. Register with correct phone number."],
    ["CF22","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["U53","Transaction Declined","Remitter Bank Unavailable","The transaction failed due to the PSP did not receive confirmation of the debit. Please ask the customer to retry."],
    ["T03","Validation Failure","Invalid Parameter","Txn note can be alphanumeric with minlength is 1 and maxlength is 50."],
    ["U22","Transaction Declined","Auth Declined","Issuer bank or payment service provider declined the transaction."],
    ["U26","Transaction Declined","PSP Declined","Issuer bank or payment service provider declined the transaction."],
    ["U31","Transaction Declined","Transaction Not Permitted","TPV payment was made using a non-registered bank account. Remitter bank declined the transaction."],
    ["U14","Gateway Error","Encryption Error","Encryption Error at NPCI."],
    ["TM","Merchant Blocked","Merchant Blocked","Transaction was declined because customer has blocked the merchant."],
    ["L04","Transaction Not Initiated","Invalid Format","Transaction was not initiated with the service provider."],
    ["94","Gateway Error","Duplicate Transaction","Transaction declined as this is the duplicate transaction."],
    ["ZG","Transaction Declined","VPA Resolution Failed","Issuer bank or payment service provider declined the transaction."],
    ["CF07","Transaction Declined","Bad Request","The request the client made is incorrect or corrupt, and the server can't understand it."],
    ["XQ","Transaction Declined","Payment Not Allowed","Payment to this beneficiary is declined."],
    ["YF","Transaction Declined","Account Blocked Merchant","Issuer bank or payment service provider declined the transaction."],
    ["XI","Validation Failure","Invalid Account","Customer's payment instrument was not setup properly."],
    ["91","Network Error","Network Timeout","Transaction failed due to host timeout."],
    ["FL","Transaction Declined","Transaction Amount Limit","Customer has exceeded the withdrawal amount limit."],
    ["HS","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["IR","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["U69","Customer Cancelled","Request Expired","Collect request expired."],
    ["5009","Transaction Failed","Technical Error","Transaction failed due to some technical error. Kindly retry or reach out to bank."],
    ["1","Transaction Declined","PSP Decline Throttle","Payment service provider declined the transaction."],
    ["U28","Transaction Declined","Remitter Bank Unavailable","The remitter bank or TPAP is currently unavailable. Please request the user to retry after some time."],
    ["CF29","Technical Failure","Cred Error","Transaction failed due to issues with bank credentials."],
    ["SA","Transaction Declined","Payment Not Allowed","Payment from this type of source account (CC/PPI/od) is not allowed."],
    ["ZA","Customer Auth Failure","Customer Decline","This transaction has been declined/cancelled by the customer."],
    ["ZM","Network Error","Invalid Pin","The customer entered an invalid pin. Please request the customer to try again with the correct pin."],
    ["B3","Transaction Declined","Restricted Account","TPV payment was made using a non-registered bank account. Payment was made using a restricted account as per bank policy (e.g., minor account, proprietor account)."],
    ["CF23","Technical Failure","Remitter Bank Unavailable","Resource that you are trying to reach is currently unavailable. Please retry after some time."],
    ["ZH","Network Error","Invalid VPA","Customer has entered incorrect VPA."],
    ["U81","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["FAILURE","Transaction Declined","Unknown Error","Issuer bank or payment service provider declined the transaction."],
    ["U30","Transaction Declined","Debit Failed","The remitter (customer's) bank declined the transaction. Please request the user to try again or check with their bank."],
    ["U16","Transaction Declined","Risk Threshold Exceeded","Issuer bank or payment service provider declined the transaction."],
    ["U67","Customer Cancelled","High Response Time","Declined because of high response time from remitter bank."],
    ["Z9","Network Error","Insufficient Funds","Insufficient funds in the user's account. Please request the user to retry after adding sufficient funds."],
    ["Z8","Transaction Declined","Per Transaction Limit Exceeded","The transaction amount exceeded the limit set by the user's bank. Please request the customer to verify this with their bank."],
    ["U90","Customer Cancelled","Remitter Bank Unavailable","The remitter bank deemed high response time. Please request the user to retry after some time."],
    ["U91","Customer Cancelled","Acquiring Bank Unavailable","The beneficiary bank deemed high response time. Please request the user to retry after some time."],
    ["UT","Customer Cancelled","Remitter Bank Unavailable","Remitter bank is not available."],
    ["U19","Transaction Declined","Authentication Failure","Issuer bank or payment service provider declined the transaction."],
    ["HS3","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["CF02","Technical Failure","Api Timeout","Bank API time out."],
    ["M16","Transaction Declined","Risk Decline","Transaction declined by risk model of NPCI."],
    ["XV","Transaction Declined","Compliance Violation","TPV payment was made using a non-registered bank account. Remitter bank declined the transaction due to a compliance violation."],
    ["0","Customer Cancelled","Request Expired","Collect request expired."],
    ["ZU","Transaction Declined","Transaction Limit Exceeded","The transaction failed due to limit set by the customer's bank exceeded. Please ask the customer to check with their bank."],
    ["DT","Transaction Declined","Bank Decline","The provided account number is invalid or not found in the beneficiary bank's records."],
    ["ZI","Transaction Declined","Debit Failed","Transaction declined due to suspected fraud based on the beneficiary risk score."],
    ["U21","Transaction Declined","Auth Failure","Customer could not be authenticated for the transaction."],
    ["U23","Transaction Declined","Auth Timeout","Issuer bank or payment service provider declined the transaction."],
    ["U25","Transaction Declined","","Issuer bank or payment service provider declined the transaction."],
    ["U27","Transaction Declined","PSP Unresponsive","Issuer bank or payment service provider declined the transaction."],
    ["U37","Gateway Error","Response Error","Gateway infrastructure error detected."],
    ["U11","Gateway Error","Credentials Missing","Gateway infrastructure error detected."],
    ["U13","Network Error","External Error","A network infrastructure error was detected."],
    ["ND","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["OD","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["RM","Transaction Declined","Invalid MPIN","Issuer bank or payment service provider declined the transaction."],
    ["RP","Network Error","Debit Reversal Timeout","A network infrastructure error was detected."],
    ["U68","Transaction Declined","Credit Failed","Issuer bank or payment service provider declined the transaction."],
    ["ZE","Transaction Declined","PSP Declined","Transaction not permitted to the customer's UPI ID (VPA) by the PSP."],
    ["ZD","Transaction Declined","Debit Failed","The transaction declined by remitter (customer's) bank, please ask the customer to check with their bank before retrying."],
    ["XU","Transaction Declined","Cutoff Time","Issuer bank or payment service provider declined the transaction."],
    ["U89","Transaction Declined","Bank Decline Throttle","Issuer bank or payment service provider declined the transaction."],
    ["FP","Transaction Declined","Transaction Amount Limit","Customer has exceeded the withdrawal amount limit."],
    ["54","Validation Failed","Card Expired","The UPI ID associated with the debit card is already expired."],
    ["Z7","Transaction Declined","Debit Limit Exceeded","Transaction frequency limit set by the remitting bank has been exceeded."],
    ["UP","Customer Cancelled","PSP Timeout","Received timeout response from payment service provider."],
    ["Null Error Code","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["U35","Gateway Error","Response Error","Gateway infrastructure error detected."],
    ["B2","Payment Instrument Inactive","Multiple Names Linked","Customer's payment instrument is inactive."],
    ["YC","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction."],
    ["XP","Transaction Declined","Debit Failed","Issuer bank or payment service provider declined the transaction, transaction not permitted for the user."],
    ["5007","Network Error","Invalid VPA","Customer has entered incorrect VPA."],
    ["5008","Payment Instrument Blocked","PSP Timeout","Customer's payment instrument was blocked by the network."],
    ["5010","Technical Failure","Technical Decline","Transaction failed due to some technical error. Kindly retry or reach out to bank."],
    ["CF11","Transaction Failed","Technical Error","Issue in decrypting the payment information. Please try again."],
    ["5087","Technical Failure","Account Number Missing","Payer account number and payer IFSC are missing. Please enter these details."],
    ["CF15","Customer Cancelled","Invalid Credentials","Transaction failed due to issues with bank credentials."],
    ["XX","Transaction Declined","Invalid Details","The transaction failed due to invalid details in the payment, please verify the details and retry."],
    ["UM1","Transaction Declined","Customer Decline","The UPI mandate request was successfully initiated and is awaiting user approval."],
    ["UN8","Transaction Declined","Customer Decline","The payment could not proceed because the users UPI app or bank is not registered to handle UPI transactions."],
    ["UM9","Transaction Declined","Debit Failed","The mandate setup request was declined by the bank or app. Please retry or use a different UPI app."],
    ["UM0","Transaction Declined","Debit Failed","The mandate setup request was declined by the bank or app. Please retry or use a different UPI app."],
    ["NO","Transaction Declined","Debit Failed","The transaction declined by remitter (customer's) bank, please ask the customer to check with their bank before retrying."],
    ["K1","Transaction Declined","Suspected Fraud","The transaction was declined by the remitter bank due to a high risk score or suspected fraud activity."],
    ["U92","Transaction Declined","Remitter Bank Unavailable","The remitter bank or TPAP is currently unavailable. Please retry after some time."],
    ["UX","Transaction Declined","Invalid VPA","UPI virtual address (VPA) used has expired or is no longer valid. Please request the user to retry with a valid VPA."],
    ["V","Transaction Declined","Transaction Details Missing","Some of the details related to the transaction are missing in the request."],
    ["409","Validation Failure","Duplicate Transaction","Duplicate transaction id found."],
    ["S99","Transaction Declined","Debit Failed","The remitter (customer's) bank declined the transaction. Please request the user to try again or check with their bank."],
    ["8010","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["2","Customer Auth Failure","Collect Request Expired","Collect expired, the customer did not approve or complete the payment within the permitted time frame."],
    ["86","Transaction Declined","Debit Failed","The transaction failed due to an internal error at the remitter's bank or server."],
    ["V03","Transaction Declined","Invalid Credentials","Transaction failed due to invalid or missing UPI credentials. Please check and try again."],
    ["92","Customer Auth Failure","Collect Request Expired","Collect expired, the customer did not approve or complete the payment within the permitted time frame."],
    ["503","Network Error","Bank Offline","Request session is timed out. Kindly retry after some time."],
    ["M2","Validation Failed","Limit Exceed","Amount limit is exceeded for this customer."],
    ["S3","Transaction Declined","Fraud Detected","Issuer bank or payment service provider declined the transaction."],
  ];

  var CONFIG = { pageSize: 20, monoColumns: /code$|^code/i, maxPillOptions: 16 };

  var root = document.getElementById("cf-errors");
  var $ = function (n) { return root.querySelector('[data-cf="' + n + '"]'); };
  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };

  /* Natural sort: numbers numerically, U9 before U16, blanks last. */
  function compare(a, b) {
    var na = parseFloat(a), nb = parseFloat(b);
    var aN = a.trim() !== "" && isFinite(na), bN = b.trim() !== "" && isFinite(nb);
    if (aN && bN) return na - nb;
    if (a.trim() === "") return 1;
    if (b.trim() === "") return -1;
    return a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
  }

  function highlight(value, term) {
    if (!term) return esc(value);
    var idx = value.toLowerCase().indexOf(term.toLowerCase());
    if (idx < 0) return esc(value);
    return esc(value.slice(0, idx)) + "<mark>" + esc(value.slice(idx, idx + term.length)) +
           "</mark>" + esc(value.slice(idx + term.length));
  }

  var headers = ERROR_CODES[0], rows = ERROR_CODES.slice(1);
  var colFilters = headers.map(function () { return ""; });
  var colKinds = [];
  var globalTerm = "", sortCol = -1, sortDir = 1, page = 1;
  var pageSize = CONFIG.pageSize;

  function classify() {
    colKinds = headers.map(function (h, i) {
      if (CONFIG.monoColumns.test(h.trim())) return "code";
      var seen = {}, n = 0, longest = 0;
      for (var r = 0; r < rows.length; r++) {
        var v = rows[r][i] || "";
        if (v.length > longest) longest = v.length;
        if (longest > 28) return "text";
        if (!seen[v]) { seen[v] = 1; n++; }
        if (n > CONFIG.maxPillOptions) return "text";
      }
      return n > 1 ? "enum" : "text";
    });
  }

  function distinct(i) {
    var seen = {}, out = [];
    rows.forEach(function (r) {
      var v = (r[i] || "").trim();
      if (v && !seen[v]) { seen[v] = 1; out.push(v); }
    });
    return out.sort(function (a, b) { return compare(a, b); });
  }

  function buildHead() {
    var titles = "<tr>" + headers.map(function (h, i) {
      return '<th scope="col" aria-sort="none" data-col="' + i + '">' +
        '<button type="button" class="cf-sortbtn" data-sort="' + i + '">' +
        '<span>' + esc(h) + '</span><span class="cf-arrow" aria-hidden="true">&#9650;&#9660;</span>' +
        "</button></th>";
    }).join("") + "</tr>";

    var filters = "<tr>" + headers.map(function (h, i) {
      var lbl = 'aria-label="Filter by ' + esc(h) + '"';
      var ctrl = colKinds[i] === "enum"
        ? '<select data-filter="' + i + '" ' + lbl + '><option value="">All</option>' +
          distinct(i).map(function (v) { return '<option value="' + esc(v) + '">' + esc(v) + "</option>"; }).join("") +
          "</select>"
        : '<input type="text" data-filter="' + i + '" placeholder="Filter..." ' + lbl + ">";
      return '<th class="cf-filtercell">' + ctrl + "</th>";
    }).join("") + "</tr>";

    $("thead").innerHTML = titles + filters;
  }

  function visibleRows() {
    var g = globalTerm.trim().toLowerCase();
    return rows.filter(function (r) {
      for (var i = 0; i < headers.length; i++) {
        var f = colFilters[i];
        if (!f) continue;
        var cell = (r[i] || "");
        if (colKinds[i] === "enum") { if (cell.trim() !== f) return false; }
        else if (cell.toLowerCase().indexOf(f.toLowerCase()) === -1) return false;
      }
      if (!g) return true;
      return r.some(function (c) { return String(c).toLowerCase().indexOf(g) !== -1; });
    });
  }

  function render() {
    var data = visibleRows();

    if (sortCol > -1) {
      data = data.slice().sort(function (a, b) {
        return compare(a[sortCol] || "", b[sortCol] || "") * sortDir;
      });
    }

    var total = data.length;
    var pages = Math.max(1, Math.ceil(total / pageSize));
    if (page > pages) page = pages;
    var start = (page - 1) * pageSize;
    var slice = data.slice(start, start + pageSize);
    var term = globalTerm.trim();

    $("tbody").innerHTML = slice.length
      ? slice.map(function (r) {
          return "<tr>" + headers.map(function (h, i) {
            var v = r[i] || "";
            var cellTerm = term || (colKinds[i] !== "enum" ? colFilters[i] : "");
            var inner = highlight(v, cellTerm);
            if (colKinds[i] === "code") return '<td class="cf-code">' + inner + "</td>";
            if (colKinds[i] === "enum" && v.trim()) return '<td><span class="cf-pill">' + inner + "</span></td>";
            return "<td>" + inner + "</td>";
          }).join("") + "</tr>";
        }).join("")
      : '<tr><td class="cf-empty" colspan="' + headers.length +
        '">No error code matches those filters. Try clearing one.</td></tr>';

    $("count").textContent = total
      ? "Showing " + (start + 1) + " to " + Math.min(start + pageSize, total) +
        " of " + total + (total === rows.length ? "" : " filtered") + " codes"
      : "0 of " + rows.length + " codes";

    var btns = [], want = {};
    want[1] = want[pages] = 1;
    for (var p = page - 1; p <= page + 1; p++) if (p > 0 && p <= pages) want[p] = 1;
    var list = Object.keys(want).map(Number).sort(function (a, b) { return a - b; });
    btns.push('<button type="button" class="cf-btn" data-page="' + (page - 1) + '"' +
      (page === 1 ? " disabled" : "") + ' aria-label="Previous page">Prev</button>');
    var prev = 0;
    list.forEach(function (p) {
      if (prev && p - prev > 1) btns.push('<span style="padding:0 .2rem;">...</span>');
      btns.push('<button type="button" class="cf-btn" data-page="' + p + '"' +
        (p === page ? ' aria-current="true"' : "") + ">" + p + "</button>");
      prev = p;
    });
    btns.push('<button type="button" class="cf-btn" data-page="' + (page + 1) + '"' +
      (page === pages ? " disabled" : "") + ' aria-label="Next page">Next</button>');
    $("pager").innerHTML = pages > 1 ? btns.join("") : "";

    root.querySelectorAll("thead th[data-col]").forEach(function (th) {
      var i = +th.dataset.col;
      th.setAttribute("aria-sort", i === sortCol ? (sortDir === 1 ? "ascending" : "descending") : "none");
    });
  }

  var timer;
  function debounced() { clearTimeout(timer); timer = setTimeout(function () { page = 1; render(); }, 110); }

  root.addEventListener("input", function (e) {
    var t = e.target;
    if (t.dataset.cf === "global") { globalTerm = t.value; debounced(); return; }
    if (t.dataset.filter !== undefined) { colFilters[+t.dataset.filter] = t.value; debounced(); }
  });

  root.addEventListener("change", function (e) {
    var t = e.target;
    if (t.dataset.cf === "pagesize") { pageSize = +t.value; page = 1; render(); }
  });

  root.addEventListener("click", function (e) {
    var s = e.target.closest("[data-sort]");
    if (s) {
      var i = +s.dataset.sort;
      if (sortCol === i) { sortDir = -sortDir; } else { sortCol = i; sortDir = 1; }
      page = 1; render(); return;
    }
    var p = e.target.closest("[data-page]");
    if (p && !p.disabled) { page = +p.dataset.page; render(); root.scrollIntoView({ block: "start" }); return; }
    if (e.target.dataset.cf === "reset") {
      globalTerm = ""; colFilters = []; sortCol = -1; sortDir = 1; page = 1;
      $("global").value = "";
      root.querySelectorAll("[data-filter]").forEach(function (el) { el.value = ""; });
      render();
    }
  });

  classify();
  buildHead();
  render();
})();
</script>
</section>

## 3. High-Priority Business Scenarios & Edge Cases

### 3.1 Third-Party Verification (TPV) Failures (U19)

In investment and capital markets flows (MCC 6211 / 6012), regulatory mandates require validating the remitter account against customer record.

*   **Trigger:** Customer initiates a payment using a UPI ID linked to Account A, but registered profile has Account B.

*   **Gateway Action:** Transaction is aborted before money leaves the bank, failing with `TPV_ACCOUNT_MISMATCH`.

*   **Handling:** Display explicit error banner detailing the expected account number last 4 digits:

    > Expected Account: `XXXX-XXXX-1234`


### 3.2 The 24-Hour Velocity Cooling-Off Rule (U30)

To prevent account takeover fraud, NPCI caps transactions at ₹5,000 for 24 hours after:

1.  Initial UPI registration on a device.
2.  Device binding/SIM change.
3.  UPI PIN reset/change.

If an order is ₹15,000, NPCI will decline the transaction with code U30 even if the user has ample account balance. Checkouts should detect U30 and offer non-UPI fallback instruments.
