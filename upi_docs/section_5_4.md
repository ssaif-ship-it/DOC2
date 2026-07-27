<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Customer-Facing Payment Error Messaging — Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --ink:#0A0E1A;
    --panel:#111729;
    --panel-2:#161d33;
    --hairline:#26304d;
    --text:#E9EBF3;
    --muted:#8B93AC;
    --mint:#5EEAD4;
    --mint-dim:rgba(94,234,212,0.14);
    --amber:#F5A623;
    --amber-dim:rgba(245,166,35,0.14);
    --blue:#4C8DFF;
    --blue-dim:rgba(76,141,255,0.14);
    --violet:#B18CFF;
    --violet-dim:rgba(177,140,255,0.14);
    --gray:#8A93AC;
    --gray-dim:rgba(138,147,172,0.14);
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    margin:0;
    background:var(--ink);
    color:var(--text);
    font-family:'IBM Plex Sans',sans-serif;
    font-size:16px;
    line-height:1.6;
  }
  ::selection{background:var(--mint-dim); color:var(--mint);}

  h1,h2,h3,.disp{font-family:'Space Grotesk',sans-serif; letter-spacing:-0.01em;}
  code, .mono, .code-cell, .tag-code{font-family:'IBM Plex Mono',monospace;}

  a{color:var(--mint);}

  /* Layout shell */
  .shell{
    display:grid;
    grid-template-columns:264px 1fr;
    max-width:1280px;
    margin:0 auto;
  }
  @media (max-width:900px){
    .shell{grid-template-columns:1fr;}
    nav.sidebar{display:none;}
  }

  /* Sidebar */
  nav.sidebar{
    position:sticky;
    top:0;
    height:100vh;
    overflow-y:auto;
    padding:32px 20px 32px 28px;
    border-right:1px solid var(--hairline);
  }
  .brand{
    font-size:13px;
    text-transform:uppercase;
    letter-spacing:0.14em;
    color:var(--muted);
    margin-bottom:4px;
  }
  .brand-title{
    font-family:'Space Grotesk',sans-serif;
    font-size:19px;
    font-weight:600;
    color:var(--text);
    margin-bottom:28px;
    line-height:1.3;
  }
  .navlist{list-style:none; padding:0; margin:0;}
  .navlist li{margin-bottom:2px;}
  .navlist a{
    display:block;
    padding:7px 10px;
    border-radius:6px;
    color:var(--muted);
    text-decoration:none;
    font-size:13.5px;
    border-left:2px solid transparent;
    transition:background .15s, color .15s, border-color .15s;
  }
  .navlist a:hover{background:var(--panel); color:var(--text);}
  .navlist a.active{
    color:var(--mint);
    background:var(--mint-dim);
    border-left:2px solid var(--mint);
  }
  .navlist .num{
    display:inline-block;
    width:20px;
    color:var(--muted);
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
  }
  .navlist a.active .num{color:var(--mint);}

  /* Main content */
  main{padding:0 44px 120px;}
  @media (max-width:900px){main{padding:0 20px 100px;}}

  .hero{
    padding:64px 0 48px;
    border-bottom:1px solid var(--hairline);
    margin-bottom:56px;
  }
  .eyebrow{
    color:var(--mint);
    font-family:'IBM Plex Mono',monospace;
    font-size:12.5px;
    letter-spacing:0.08em;
    text-transform:uppercase;
    margin-bottom:14px;
  }
  .hero h1{
    font-size:40px;
    font-weight:700;
    line-height:1.15;
    margin:0 0 16px;
    max-width:680px;
  }
  .hero p.lede{
    color:var(--muted);
    font-size:16.5px;
    max-width:640px;
    margin:0 0 40px;
  }

  /* pipeline */
  .pipeline{
    display:grid;
    grid-template-columns:1fr auto 1fr auto 1fr;
    gap:14px;
    align-items:stretch;
  }
  @media (max-width:760px){
    .pipeline{grid-template-columns:1fr; gap:10px;}
    .pipeline .arrow{transform:rotate(90deg); margin:0 auto;}
  }
  .stage{
    background:var(--panel);
    border:1px solid var(--hairline);
    border-radius:10px;
    padding:18px 18px 20px;
    position:relative;
  }
  .stage .stage-label{
    font-family:'IBM Plex Mono',monospace;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.08em;
    color:var(--muted);
    margin-bottom:10px;
  }
  .stage .stage-audience{font-size:13px; color:var(--muted); margin-bottom:12px;}
  .stage .stage-payload{
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
    color:var(--text);
    background:var(--ink);
    border:1px solid var(--hairline);
    border-radius:6px;
    padding:10px 12px;
    line-height:1.5;
    word-break:break-word;
  }
  .stage.final{border-color:var(--mint); box-shadow:0 0 0 1px var(--mint) inset;}
  .stage.final .stage-payload{color:var(--mint); background:var(--mint-dim); border-color:transparent;}
  .arrow{display:flex; align-items:center; color:var(--muted); font-size:20px;}

  /* sections */
  section{margin-bottom:64px; scroll-margin-top:24px;}
  .section-head{
    display:flex;
    align-items:baseline;
    gap:14px;
    margin-bottom:8px;
    padding-bottom:14px;
    border-bottom:1px solid var(--hairline);
  }
  .section-head .n{
    font-family:'IBM Plex Mono',monospace;
    color:var(--mint);
    font-size:15px;
  }
  .section-head h2{
    font-size:24px;
    margin:0;
    font-weight:600;
  }
  section > p.intro{color:var(--muted); max-width:760px; margin-top:16px;}

  .callout{
    background:var(--amber-dim);
    border:1px solid rgba(245,166,35,0.35);
    border-radius:8px;
    padding:14px 16px;
    font-size:14px;
    color:#F5C773;
    margin:20px 0;
  }
  .callout strong{color:var(--amber);}

  /* generic tables */
  .tablewrap{overflow-x:auto; border:1px solid var(--hairline); border-radius:10px; margin-top:20px;}
  table{border-collapse:collapse; width:100%; font-size:13.5px;}
  thead th{
    text-align:left;
    background:var(--panel-2);
    color:var(--muted);
    font-family:'IBM Plex Mono',monospace;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.05em;
    padding:12px 14px;
    border-bottom:1px solid var(--hairline);
    white-space:nowrap;
  }
  tbody td{
    padding:12px 14px;
    border-bottom:1px solid var(--hairline);
    vertical-align:top;
    color:var(--text);
  }
  tbody tr:last-child td{border-bottom:none;}
  tbody tr:hover{background:rgba(255,255,255,0.02);}
  td.code-cell{font-family:'IBM Plex Mono',monospace; font-size:12.5px; color:var(--mint); white-space:nowrap;}
  td.reason-cell{font-family:'IBM Plex Mono',monospace; font-size:12.5px; color:var(--text); white-space:nowrap;}
  td.msg-cell{color:var(--text); max-width:340px;}
  td.cta-cell{color:var(--muted); font-size:12.5px; white-space:nowrap;}

  /* source pills */
  .pill{
    display:inline-flex;
    align-items:center;
    gap:6px;
    padding:3px 10px 3px 8px;
    border-radius:99px;
    font-size:11.5px;
    font-family:'IBM Plex Mono',monospace;
    font-weight:500;
    white-space:nowrap;
  }
  .pill::before{content:''; width:6px; height:6px; border-radius:50%;}
  .pill.customer{background:var(--amber-dim); color:var(--amber);}
  .pill.customer::before{background:var(--amber);}
  .pill.bank{background:var(--blue-dim); color:var(--blue);}
  .pill.bank::before{background:var(--blue);}
  .pill.cashfree{background:var(--violet-dim); color:var(--violet);}
  .pill.cashfree::before{background:var(--violet);}
  .pill.unknown{background:var(--gray-dim); color:var(--gray);}
  .pill.unknown::before{background:var(--gray);}

  .source-legend{display:flex; flex-wrap:wrap; gap:10px; margin:22px 0 4px;}
  .source-card{
    flex:1 1 220px;
    background:var(--panel);
    border:1px solid var(--hairline);
    border-radius:10px;
    padding:16px 16px 18px;
  }
  .source-card h4{margin:8px 0 6px; font-size:14.5px; font-family:'Space Grotesk',sans-serif;}
  .source-card p{margin:0; font-size:12.8px; color:var(--muted);}
  .source-card .owner{font-size:11.5px; color:var(--muted); margin-top:8px; font-family:'IBM Plex Mono',monospace;}

  /* subsection titles */
  h3.sub{
    font-size:16px;
    margin:36px 0 4px;
    font-weight:600;
    display:flex;
    align-items:center;
    gap:10px;
  }
  h3.sub .pill{font-size:11px;}

  /* payload / code block */
  pre.payload{
    background:var(--panel);
    border:1px solid var(--hairline);
    border-radius:10px;
    padding:18px 20px;
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    color:var(--text);
    overflow-x:auto;
    line-height:1.7;
  }
  pre.payload .k{color:var(--blue);}
  pre.payload .v{color:var(--mint);}

  /* template cards */
  .tpl-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:16px; margin-top:20px;}
  .tpl-card{
    background:var(--panel);
    border:1px solid var(--hairline);
    border-radius:10px;
    padding:18px 18px 20px;
  }
  .tpl-card .tpl-title{
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:0.06em;
    color:var(--muted);
    margin-bottom:10px;
    font-family:'IBM Plex Mono',monospace;
  }
  .tpl-card p{
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    color:var(--text);
    line-height:1.7;
    margin:0;
  }
  .tpl-card .var{color:var(--mint);}

  /* UI mockup for section 6 */
  .modal-mock{
    max-width:480px;
    background:var(--panel);
    border:1px solid var(--hairline);
    border-radius:14px;
    padding:26px 26px 22px;
    margin-top:22px;
    box-shadow:0 20px 50px rgba(0,0,0,0.35);
  }
  .modal-mock .m-head{display:flex; align-items:center; gap:10px; margin-bottom:14px;}
  .modal-mock .m-icon{
    width:34px; height:34px; border-radius:50%;
    background:var(--amber-dim); color:var(--amber);
    display:flex; align-items:center; justify-content:center;
    font-size:17px; flex:none;
  }
  .modal-mock .m-title{font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:16px;}
  .modal-mock .m-body{font-size:14px; color:var(--muted); margin-bottom:14px; line-height:1.6;}
  .modal-mock .m-next{font-size:13px; color:var(--text); margin-bottom:20px;}
  .modal-mock .m-next b{color:var(--mint); font-weight:500;}
  .modal-mock .m-ctas{display:flex; gap:10px; margin-bottom:16px; flex-wrap:wrap;}
  .btn{
    font-family:'IBM Plex Sans',sans-serif;
    font-size:13px; font-weight:600;
    padding:9px 16px; border-radius:7px;
    border:1px solid var(--hairline);
    cursor:default;
  }
  .btn.primary{background:var(--mint); color:var(--ink); border:none;}
  .btn.secondary{background:transparent; color:var(--text);}
  .modal-mock .m-ref{font-family:'IBM Plex Mono',monospace; font-size:11.5px; color:var(--muted); border-top:1px solid var(--hairline); padding-top:14px;}
  .mock-annot{display:flex; flex-wrap:wrap; gap:8px; margin-top:16px;}
  .mock-annot span{
    font-size:11.5px; color:var(--muted); background:var(--ink);
    border:1px solid var(--hairline); padding:5px 10px; border-radius:99px;
  }

  /* distribution bars */
  .bars{margin-top:22px; display:flex; flex-direction:column; gap:12px;}
  .bar-row{display:grid; grid-template-columns:190px 1fr 60px; align-items:center; gap:14px;}
  .bar-row .label{font-family:'IBM Plex Mono',monospace; font-size:12.5px; color:var(--text);}
  .bar-track{background:var(--panel); border-radius:5px; height:14px; overflow:hidden; border:1px solid var(--hairline);}
  .bar-fill{height:100%; border-radius:5px 0 0 5px; background:linear-gradient(90deg, var(--mint), var(--blue));}
  .bar-row .pct{font-family:'IBM Plex Mono',monospace; font-size:12.5px; color:var(--muted); text-align:right;}

  .action-list{margin-top:26px; display:grid; gap:12px;}
  .action-item{
    display:grid; grid-template-columns:80px 1fr; gap:16px;
    background:var(--panel); border:1px solid var(--hairline); border-radius:10px; padding:14px 16px;
  }
  .action-item .ac-code{font-family:'IBM Plex Mono',monospace; color:var(--mint); font-size:13px;}
  .action-item .ac-text{font-size:13.5px; color:var(--text);}
  .action-item .ac-text b{color:var(--muted); font-weight:500;}

  footer{
    border-top:1px solid var(--hairline);
    margin-top:40px;
    padding-top:24px;
    color:var(--muted);
    font-size:12.5px;
  }
</style>
</head>
<body>

<div class="shell">
  <nav class="sidebar">
    <div class="brand">Reference Guide</div>
    <div class="brand-title">Customer-Facing Payment Error Messages</div>
    <ul class="navlist" id="navlist">
      <li><a href="#s1"><span class="num">01</span>Three-Layer Error Model</a></li>
      <li><a href="#s2"><span class="num">02</span>Categorization by Source</a></li>
      <li><a href="#s3"><span class="num">03</span>Master Message Matrix</a></li>
      <li><a href="#s4"><span class="num">04</span>AutoPay &amp; Subscriptions</a></li>
      <li><a href="#s5"><span class="num">05</span>Notification Templates</a></li>
      <li><a href="#s6"><span class="num">06</span>UI Layout Rules</a></li>
      <li><a href="#s7"><span class="num">07</span>Sandbox Simulation</a></li>
      <li><a href="#s8"><span class="num">08</span>Failure Distribution</a></li>
    </ul>
  </nav>

  <main>
    <div class="hero">
      <div class="eyebrow">§5.5 · Customer-Facing Messages</div>
      <h1>Translate raw bank codes into messages people can act on.</h1>
      <p class="lede">Every UPI or card failure arrives as a raw, technical string from the issuing bank or switch — <span class="mono" style="color:var(--muted)">U30|DEBIT HAS BEEN FAILED|Z9|INSUFFICIENT FUNDS</span> and the like. Shown to a customer as-is, it produces confusion, support tickets, and abandoned carts. This guide is the translation layer.</p>

      <div class="pipeline">
        <div class="stage">
          <div class="stage-label">Layer 1 · Raw</div>
          <div class="stage-audience">Internal logs, gateway routing, switch recon</div>
          <div class="stage-payload">U30|DEBIT HAS FAILED|Z9|INSUFFICIENT FUNDS IN CUSTOMER (REMITTER) ACCOUNT</div>
        </div>
        <div class="arrow">→</div>
        <div class="stage">
          <div class="stage-label">Layer 2 · Normalized</div>
          <div class="stage-audience">Merchant APIs, webhooks, analytics</div>
          <div class="stage-payload">error_code: TRANSACTION_DECLINED<br>error_reason: debit_failed<br>error_source: bank</div>
        </div>
        <div class="arrow">→</div>
        <div class="stage final">
          <div class="stage-label">Layer 3 · Customer-facing</div>
          <div class="stage-audience">Checkout UI, app modals, SMS / Email</div>
          <div class="stage-payload">"Your payment failed due to insufficient balance. Please add funds and try again, or use a different account."</div>
        </div>
      </div>
    </div>

    <section id="s1">
      <div class="section-head"><span class="n">01</span><h2>The Three-Layer Error Model</h2></div>
      <p class="intro">Every payment failure undergoes a three-stage translation. Only the third stage should ever be rendered on a customer-facing screen — layers one and two stay in logs, dashboards, and merchant APIs.</p>

      <h3 class="sub">Cashfree normalized payload structure</h3>
      <p class="intro" style="margin-top:6px;">Cashfree automatically abstracts raw bank responses inside the <code style="color:var(--mint)">error_details</code> object:</p>
      <pre class="payload">{
  "error_details": {
    "<span class="k">error_code</span>": "<span class="v">TRANSACTION_DECLINED</span>",
    "<span class="k">error_description</span>": "<span class="v">payment has been declined</span>",
    "<span class="k">error_reason</span>": "<span class="v">debit_failed</span>",
    "<span class="k">error_source</span>": "<span class="v">bank</span>",
    "<span class="k">error_code_raw</span>": "<span class="v">Z9</span>",
    "<span class="k">error_description_raw</span>": "<span class="v">INSUFFICIENT FUNDS IN CUSTOMER (REMITTER) ACCOUNT</span>"
  }
}</pre>
      <div class="callout"><strong>Implementation rule —</strong> never expose <code>error_code_raw</code> or <code>error_description_raw</code> in customer UI. Map <code>error_source</code> + <code>error_reason</code> + <code>error_code</code> to user-friendly messaging instead.</div>
    </section>

    <section id="s2">
      <div class="section-head"><span class="n">02</span><h2>Categorization by Error Source</h2></div>
      <p class="intro"><code style="color:var(--mint)">error_source</code> sets the tone and the primary call-to-action for the message shown to the customer.</p>

      <div class="source-legend">
        <div class="source-card">
          <span class="pill customer">customer</span>
          <h4>Customer input or account state</h4>
          <p>Wrong PIN, low balance, user cancel.</p>
          <div class="owner">Fix owner: Customer · Tone: Helpful &amp; instructional</div>
        </div>
        <div class="source-card">
          <span class="pill bank">bank</span>
          <h4>Issuing bank unavailable</h4>
          <p>Bank CBS is down, timed out, or restricted.</p>
          <div class="owner">Fix owner: Issuing bank / customer · Tone: Reassuring &amp; empathetic</div>
        </div>
        <div class="source-card">
          <span class="pill cashfree">cashfree</span>
          <h4>Gateway-level issue</h4>
          <p>Routing, configuration, or validation issue.</p>
          <div class="owner">Fix owner: Gateway / merchant · Tone: Apologetic &amp; generic</div>
        </div>
        <div class="source-card">
          <span class="pill unknown">unknown</span>
          <h4>Unclassified response</h4>
          <p>Network response that doesn't map cleanly.</p>
          <div class="owner">Fix owner: System · Tone: Encouraging, 1-click retry</div>
        </div>
      </div>
    </section>

    <section id="s3">
      <div class="section-head"><span class="n">03</span><h2>Master Message Matrix — One-Time Payments</h2></div>

      <h3 class="sub"><span class="pill customer">customer</span>Customer-driven failures</h3>
      <div class="tablewrap"><table>
        <thead><tr><th>error_reason</th><th>Raw codes</th><th>Customer-facing UI message</th><th>CTA</th></tr></thead>
        <tbody>
          <tr><td class="reason-cell">insufficient_funds</td><td class="code-cell">Z9, 1005</td><td class="msg-cell">Your payment failed because your account has insufficient balance. Please top up your account or use another payment method.</td><td class="cta-cell">Add Funds &amp; Retry / Switch Method</td></tr>
          <tr><td class="reason-cell">invalid_pin</td><td class="code-cell">ZM, 55</td><td class="msg-cell">The UPI PIN entered was incorrect. Please try again.</td><td class="cta-cell">Re-enter PIN</td></tr>
          <tr><td class="reason-cell">pin_attempts_exceeded</td><td class="code-cell">Z6</td><td class="msg-cell">UPI PIN attempts exceeded for today. Please wait 24 hours or reset your PIN in your UPI app.</td><td class="cta-cell">Reset PIN in App</td></tr>
          <tr><td class="reason-cell">user_dropped / transaction_cancelled</td><td class="code-cell">U09, U69, ZA</td><td class="msg-cell">The transaction was cancelled or closed before completion.</td><td class="cta-cell">Try Again</td></tr>
          <tr><td class="reason-cell">collect_expired</td><td class="code-cell">U69</td><td class="msg-cell">The payment request expired. Please trigger a new request.</td><td class="cta-cell">Resend Request</td></tr>
          <tr><td class="reason-cell">transaction_flagged_for_risk</td><td class="code-cell">K1, U16</td><td class="msg-cell">Your bank blocked this payment for security reasons. Please try a different account or card.</td><td class="cta-cell">Choose Other Method</td></tr>
          <tr><td class="reason-cell">invalid_vpa</td><td class="code-cell">ZH, UX</td><td class="msg-cell">The UPI ID entered is invalid or inactive. Please verify and re-enter.</td><td class="cta-cell">Edit UPI ID</td></tr>
          <tr><td class="reason-cell">vpa_restricted</td><td class="code-cell">ZG, ZE</td><td class="msg-cell">This UPI handle is restricted from receiving payment requests. Please use an alternative method.</td><td class="cta-cell">Switch Method</td></tr>
          <tr><td class="reason-cell">limit_exceeded</td><td class="code-cell">Z7, Z8, 1143</td><td class="msg-cell">Transaction exceeds your daily UPI spending limit. Try paying a smaller amount or use NetBanking.</td><td class="cta-cell">Use NetBanking / Card</td></tr>
        </tbody>
      </table></div>

      <h3 class="sub"><span class="pill bank">bank</span>Bank-driven failures</h3>
      <div class="tablewrap"><table>
        <thead><tr><th>error_reason</th><th>Raw codes</th><th>Customer-facing UI message</th><th>CTA</th></tr></thead>
        <tbody>
          <tr><td class="reason-cell">debit_failed</td><td class="code-cell">U30, U19</td><td class="msg-cell">Your bank could not complete this payment right now. Please try again or use another payment method.</td><td class="cta-cell">Retry / Switch Method</td></tr>
          <tr><td class="reason-cell">remitter_not_available / cbs_offline</td><td class="code-cell">S96, UT, XY</td><td class="msg-cell">Your bank's servers are temporarily offline. Please try again in a few minutes.</td><td class="cta-cell">Retry in 5 mins</td></tr>
          <tr><td class="reason-cell">high_response_time</td><td class="code-cell">U90, U91</td><td class="msg-cell">Your bank is taking longer than usual to respond. Please try again shortly.</td><td class="cta-cell">Retry</td></tr>
          <tr><td class="reason-cell">account_blocked_frozen</td><td class="code-cell">YE, ZX</td><td class="msg-cell">Your bank account is restricted or frozen. Please contact your bank branch for assistance.</td><td class="cta-cell">Contact Bank</td></tr>
          <tr><td class="reason-cell">account_closed</td><td class="code-cell">ZY</td><td class="msg-cell">The bank account linked to this payment is inactive or closed. Please link a new account.</td><td class="cta-cell">Change Account</td></tr>
          <tr><td class="reason-cell">cut_off_in_process</td><td class="code-cell">XT</td><td class="msg-cell">Your bank is undergoing routine end-of-day maintenance. Please try again shortly.</td><td class="cta-cell">Retry in 15 mins</td></tr>
        </tbody>
      </table></div>

      <h3 class="sub"><span class="pill cashfree">cashfree</span>Gateway / configuration failures</h3>
      <div class="tablewrap"><table>
        <thead><tr><th>error_reason</th><th>Customer-facing UI message</th><th>Action for merchant engineering</th></tr></thead>
        <tbody>
          <tr><td class="reason-cell">invalid_amount</td><td class="msg-cell">Unable to process payment. Please verify the order amount and try again.</td><td class="msg-cell" style="color:var(--muted)">Validate min/max checkout bounds before invoking API.</td></tr>
          <tr><td class="reason-cell">payment_method_not_configured</td><td class="msg-cell">This payment option is temporarily unavailable. Please choose another method.</td><td class="msg-cell" style="color:var(--muted)">Verify MID product activation &amp; MCC payment mode permissions.</td></tr>
          <tr><td class="reason-cell">gateway_error</td><td class="msg-cell">Something went wrong while initiating your transaction. Please try again.</td><td class="msg-cell" style="color:var(--muted)">Alert internal operations; inspect Cashfree status health.</td></tr>
          <tr><td class="reason-cell">network_error</td><td class="msg-cell">Network connection timed out. Please check your internet and retry.</td><td class="msg-cell" style="color:var(--muted)">Ensure idempotent API retries.</td></tr>
        </tbody>
      </table></div>
    </section>

    <section id="s4">
      <div class="section-head"><span class="n">04</span><h2>AutoPay &amp; Subscription Messages</h2></div>
      <p class="intro">Recurring billing needs distinct handling — the customer is typically absent during auto-debit executions.</p>

      <h3 class="sub">Mandate authorization <span style="color:var(--muted); font-weight:400; font-size:13px;">(customer present)</span></h3>
      <div class="tablewrap"><table>
        <thead><tr><th>Setup failure</th><th>Customer-facing UI message</th><th>CTA</th></tr></thead>
        <tbody>
          <tr><td class="reason-cell">Cancelled by user</td><td class="msg-cell">AutoPay setup was cancelled. Please complete setup to activate your subscription.</td><td class="cta-cell">Resume Setup</td></tr>
          <tr><td class="reason-cell">Incorrect PIN</td><td class="msg-cell">Incorrect UPI PIN entered during setup. Please re-enter your PIN.</td><td class="cta-cell">Re-enter PIN</td></tr>
          <tr><td class="reason-cell">Bank not supported</td><td class="msg-cell">Your bank does not currently support UPI AutoPay. Please use eNACH or Debit Card.</td><td class="cta-cell">Use NetBanking / Card</td></tr>
          <tr><td class="reason-cell">Mandate ceiling breached</td><td class="msg-cell">The recurring fee exceeds the maximum ceiling limit set on this mandate.</td><td class="cta-cell">Setup New Mandate</td></tr>
        </tbody>
      </table></div>

      <h3 class="sub">Recurring debit executions <span style="color:var(--muted); font-weight:400; font-size:13px;">(customer absent)</span></h3>
      <p class="intro" style="margin-top:6px;">Scheduled charge failures dispatch automated SMS, email, or push notifications:</p>
      <div class="tablewrap"><table>
        <thead><tr><th>Failure cause</th><th>Notification text</th><th>In-app status</th><th>Handling action</th></tr></thead>
        <tbody>
          <tr><td class="reason-cell">Insufficient Funds (Z9)</td><td class="msg-cell">"Your [Service] payment of ₹[Amount] failed due to low balance. Please top up your account — we will re-attempt in 24 hours."</td><td class="msg-cell">Payment Failed: Low Balance. Auto-retry scheduled.</td><td class="msg-cell" style="color:var(--muted)">Auto-retry up to 9 times (1hr+ intervals).</td></tr>
          <tr><td class="reason-cell">Mandate Revoked (QC)</td><td class="msg-cell">"Your AutoPay mandate for [Service] was revoked. Please re-authorize AutoPay to maintain uninterrupted access."</td><td class="msg-cell">AutoPay Revoked. Tap to re-activate.</td><td class="msg-cell" style="color:var(--muted)">Terminal state. Prompt mandate creation.</td></tr>
          <tr><td class="reason-cell">Mandate Expired (QD)</td><td class="msg-cell">"Your AutoPay mandate has reached its expiry date. Please set up a new mandate to continue your subscription."</td><td class="msg-cell">Mandate Expired. Renew now.</td><td class="msg-cell" style="color:var(--muted)">Terminal state. Prompt mandate creation.</td></tr>
          <tr><td class="reason-cell">Account Restricted (YE)</td><td class="msg-cell">"Your scheduled payment failed because your bank account is restricted. Please update your payment details."</td><td class="msg-cell">Account Restricted. Update payment method.</td><td class="msg-cell" style="color:var(--muted)">Pause subscription.</td></tr>
          <tr><td class="reason-cell">PDN Undelivered</td><td class="msg-cell">"We could not deliver your 24-hour pre-debit payment reminder. Please enable notifications in your UPI app."</td><td class="msg-cell">Reminder Delivery Failed.</td><td class="msg-cell" style="color:var(--muted)">Re-queue Pre-Debit Notification (PDN).</td></tr>
          <tr><td class="reason-cell">Loan Mandate Revocation Attempt (MCC 7322)</td><td class="msg-cell">"Your EMI debit failed. Please contact [LenderName] directly to resolve your payment setup."</td><td class="msg-cell">EMI Debit Failed. Contact Lender.</td><td class="msg-cell" style="color:var(--muted)">Do not instruct user to revoke via app (revokeable=N flag active).</td></tr>
        </tbody>
      </table></div>
    </section>

    <section id="s5">
      <div class="section-head"><span class="n">05</span><h2>Ready-to-Use Notification Templates</h2></div>
      <div class="tpl-grid">
        <div class="tpl-card">
          <div class="tpl-title">One-time payment failure · SMS / Push</div>
          <p><span class="var">[MerchantName]</span>: Your payment of ₹<span class="var">[Amount]</span> for Order #<span class="var">[OrderId]</span> could not be processed (<span class="var">[Reason]</span>). Please retry or select another payment option: <span class="var">[CheckoutLink]</span></p>
        </div>
        <div class="tpl-card">
          <div class="tpl-title">AutoPay low balance alert · SMS / Email</div>
          <p><span class="var">[MerchantName]</span>: Your subscription payment of ₹<span class="var">[Amount]</span> failed due to low account balance. Please add funds to your account. We will retry the payment automatically within 24 hours.</p>
        </div>
        <div class="tpl-card">
          <div class="tpl-title">Refund initiated notice · SMS / Email</div>
          <p><span class="var">[MerchantName]</span>: A refund of ₹<span class="var">[Amount]</span> for Order #<span class="var">[OrderId]</span> has been initiated. Reference UTR: <span class="var">[ARN/UTR]</span>. The credit will reflect in your account within 1–3 business days.</p>
        </div>
      </div>
    </section>

    <section id="s6">
      <div class="section-head"><span class="n">06</span><h2>Error Message UI Layout Rules</h2></div>
      <p class="intro">Every error modal or checkout alert banner needs four components: a clear status header, a contextual explanation, an actionable next step, and an order reference tag.</p>

      <div class="modal-mock">
        <div class="m-head">
          <div class="m-icon">!</div>
          <div class="m-title">Payment Could Not Be Completed</div>
        </div>
        <div class="m-body">Your bank declined this transaction due to insufficient account balance.</div>
        <div class="m-next"><b>What to do next:</b> Please add funds to your bank account and retry, or select an alternative payment method.</div>
        <div class="m-ctas">
          <div class="btn primary">Add Funds &amp; Retry</div>
          <div class="btn secondary">Choose Other Mode</div>
        </div>
        <div class="m-ref">Order Reference: #ORD-99887766</div>
      </div>
      <div class="mock-annot">
        <span>① Clear status header</span>
        <span>② Contextual explanation</span>
        <span>③ Actionable next step</span>
        <span>④ Order reference tag</span>
      </div>
    </section>

    <section id="s7">
      <div class="section-head"><span class="n">07</span><h2>Sandbox Testing &amp; Error Simulation</h2></div>
      <p class="intro">Use Cashfree's Payment Error Code Simulator in the sandbox environment to test error handling logic without real money.</p>
      <div class="tablewrap"><table>
        <thead><tr><th>Simulator mock code</th><th>Simulated failure mode</th><th>Verified API response</th></tr></thead>
        <tbody>
          <tr><td class="code-cell">INSUFFICIENT_FUND</td><td class="msg-cell">Low account balance</td><td class="reason-cell">error_reason: "insufficient_funds"</td></tr>
          <tr><td class="code-cell">INCORRECT_PIN</td><td class="msg-cell">Wrong UPI PIN</td><td class="reason-cell">error_reason: "invalid_pin"</td></tr>
          <tr><td class="code-cell">COLLECT_EXPIRED</td><td class="msg-cell">5-minute Collect timeout</td><td class="reason-cell">error_reason: "collect_expired"</td></tr>
          <tr><td class="code-cell">ISSUER_NOT_AVAILABLE</td><td class="msg-cell">Bank CBS offline</td><td class="reason-cell">error_reason: "cbs_offline"</td></tr>
        </tbody>
      </table></div>
    </section>

    <section id="s8">
      <div class="section-head"><span class="n">08</span><h2>Distribution of Common UPI Failures</h2></div>
      <p class="intro">Focusing UI design effort on the top failure codes resolves roughly 75% of customer drop-offs on UPI.</p>

      <div class="bars">
        <div class="bar-row"><span class="label">U69 · Collect Expired</span><div class="bar-track"><div class="bar-fill" style="width:100%"></div></div><span class="pct">~36%</span></div>
        <div class="bar-row"><span class="label">U30 · Debit Failed</span><div class="bar-track"><div class="bar-fill" style="width:75%"></div></div><span class="pct">~27%</span></div>
        <div class="bar-row"><span class="label">Z9 · Low Balance</span><div class="bar-track"><div class="bar-fill" style="width:8%"></div></div><span class="pct">~3%</span></div>
        <div class="bar-row"><span class="label">U67 · Debit Timeout</span><div class="bar-track"><div class="bar-fill" style="width:7%"></div></div><span class="pct">~2.5%</span></div>
        <div class="bar-row"><span class="label">ZA · Customer Declined</span><div class="bar-track"><div class="bar-fill" style="width:4%"></div></div><span class="pct">1.4%</span></div>
        <div class="bar-row"><span class="label">ZM · Wrong PIN</span><div class="bar-track"><div class="bar-fill" style="width:4%"></div></div><span class="pct">1.4%</span></div>
      </div>

      <div class="action-list">
        <div class="action-item"><span class="ac-code">U69 · 36%</span><span class="ac-text">Auto-render a fresh Dynamic QR code or Intent button <b>with a countdown timer</b>.</span></div>
        <div class="action-item"><span class="ac-code">U30 · 27%</span><span class="ac-text">Prompt an immediate <b>1-click retry</b> or bank account switch.</span></div>
        <div class="action-item"><span class="ac-code">Z9 · 3%</span><span class="ac-text">Prompt <b>balance top-up</b> or a credit card payment.</span></div>
      </div>
    </section>

    <footer>Internal reference · Customer-Facing Payment Error Messaging · §5.5</footer>
  </main>
</div>

<script>
  const links = document.querySelectorAll('#navlist a');
  const sections = Array.from(links).map(l => document.querySelector(l.getAttribute('href')));
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const idx = sections.indexOf(entry.target);
      if (entry.isIntersecting && idx !== -1) {
        links.forEach(l => l.classList.remove('active'));
        links[idx].classList.add('active');
      }
    });
  }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
  sections.forEach(s => s && io.observe(s));
</script>

</body>
</html>
