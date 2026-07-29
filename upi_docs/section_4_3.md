While standard UPI flows (Intent, Collect) transfer funds instantly, certain business models require a pre-authorization mechanism. Merchants often need to secure a customer's financial commitment upfront, but only capture the funds when a service is fulfilled, an order is adjusted, or a trade is executed.

UPI addresses this through **Mandate Block (Lien)** functionality. The customer pre-authorizes a transaction, freezing the required funds directly within their bank account. The money is only debited when the merchant initiates execution at a later time. This completely eliminates custodial risk, keeping money safely in the customer's account until the exact moment of payment.

## 1. Mandate Architecture Comparison

| Feature / Attribute | One-Time Mandates (OTM) | UPI AutoPay | SBMD / UPI Reserve Pay |
| :--- | :--- | :--- | :--- |
| **Mandate Recurrence** | One-Time | Recurring | Recurring |
| **Blocking of Funds (Lien)** | ✅ Yes | ❌ No | ✅ Yes |
| **Execution Pattern** | Single debit | Multiple debits per cycle | Multiple debits against 1 block |
| **Debit Failure Risk** | Near Zero (Funds Blocked) | High (Balance dependent) | Near Zero (Funds Blocked) |
| **Purpose Codes** | 01 | SI / Various | 76 (Trading), 77 (Retail) |
| **PIN Authentication** | 1-Time at Block creation | 1-Time at Setup | 1-Time at Block creation |

## 2. One-Time Mandates (OTM)

A One-Time Mandate allows a merchant to block funds for a single transaction and execute a single debit at a later time.

### Key Specifications

- **Purpose Code:** `01`
- **Primary Use Cases:** Hotel reservations, security deposits, IPO subscriptions (ASBA), e-commerce Pay-on-Delivery, and train ticket booking (IRCTC).
- **Execution:** A single debit up to the blocked amount (execution ≤ blocked amount). Once executed, the mandate is permanently closed, and any residual balance is automatically unblocked.
- **Mandate Creation:** Payee-initiated (Collect mode) or Payer-initiated (Intent/QR).
- **Mandate Operations:** `CREATE`, `MODIFY`, `REVOKE`.
- **Max Validity:** Configured by merchant/acquirer (up to 30 years maximum).

### Execution Rules & Mechanics

1. **Order Creation:** Call `POST /orders` with `authorize_only: true` and pass an authorization object detailing block amount and validity windows.
2. **Authorization:** Customer enters their UPI PIN via Intent, Collect, or Dynamic QR → issuing bank places a lien on the requested amount.
3. **Capture:** Merchant calls the **Pre-Authorization Capture API** with the final execution amount (≤ blocked amount). The bank debits the customer and settles the money to the merchant.
4. **Void/Release:** If an order is cancelled or unfulfilled, the merchant calls the **Void API**, immediately releasing the lien back to the customer.

> **TDR Pricing Rule:** Transaction Discount Rate (TDR) is charged upon mandate creation success. Even if a mandate is voided without capture, creation cost pricing applies.

## 3. Single Block Multiple Debits (SBMD) / UPI Reserve Pay

SBMD is an extension of OTM. It allows a merchant to block a maximum ceiling amount once and execute multiple partial debits against that single block over time — until the funds are exhausted, revoked, or expired.

Unlike traditional AutoPay, where individual recurring debits can fail due to low balance, SBMD guarantees that every debit execution is backed by pre-reserved funds.

### SBMD Purpose Codes & Vertical Specifications

#### Purpose Code 76 — Secondary Market Trading

Designed specifically for equity, derivative, and commodity broking under MCC 6211.

- **Flagship Use Case:** Investors block funds in their bank account against the Clearing Corporation (CC). As trades are executed by the broker throughout the day, the CC debits the block to settle trade obligations.
- **Maximum Transaction Limit:** Exceptional cap of ₹5,00,000 per block (aligned with RBI-approved ASBA limits).
- **Mandate Initiation:** Payer-Initiated strictly (Intent, QR, SDK). Collect mode is strictly prohibited.
- **Mandate Operations:** `CREATE` and `REVOKE` only. `MODIFY` is not permitted.
- **Revocable Flag:** Must be set to `N` (Non-revocable by customer inside TPAP apps). Revocation can only be triggered via merchant/CC interfaces.
- **Transaction Reference (`tr`) Format:** Must strictly follow the hyphen-separated structure:

  ```text
  TMCODE-SEGMENTCODE-UCCCODE-brokerref
  ```

  e.g., `12345-123-1122334456-brokerref`, where TM Code is 5 digits, Segment Code is 3 digits, and UCC is 12 digits.

- **Funding Sources:** Savings Accounts, Current Accounts, Overdraft Accounts.

#### Purpose Code 77 — Online Goods & Services

Designed for general e-commerce, quick commerce, travel, and mobility platforms.

- **Use Cases:** Quick commerce, online food delivery, travel bookings, cab aggregators, EV charging stations, in-app wallets (without preloading), and Pay-on-Delivery.
- **Maximum Transaction Limit:** Block capped at standard network limits of ₹10,00,000 (or standard ₹1,00,000 P2M depending on tier).
- **Block Validity:** Up to 90 days.
- **Mandate Initiation:** Payer-initiated (Intent, QR, SDK) or Payee-initiated (Collect mode permitted).
- **Mandate Operations:** `CREATE`, `MODIFY`, `REVOKE`. Modification is allowed strictly for the amount field.
- **Funding Sources:** Savings Accounts, Current Accounts, Overdrafts, RuPay Credit Cards on UPI, and Pre-Sanctioned Credit Lines.

#### Purpose Codes 78 & 79

Reserved by NPCI for upcoming product extensions and industry verticals.

### SBMD Use Case Deep Dives

| Vertical | Example |
| :--- | :--- |
| **Secondary Markets** | Investor blocks ₹5L against CC; broker debits per trade. |
| **Quick Commerce** | User blocks ₹2,000; mini-orders debit without PIN re-entry. |
| **Travel Bookings** | User blocks ₹10,000; flight, hotel, and cab debit as booked. |
| **In-App Wallets** | Funds stay in customer's bank; debited only on usage. |

## 4. Consumer Branding: UPI Reserve Pay

**UPI Reserve Pay** is NPCI's official consumer-facing brand name for SBMD. While technical specifications, APIs, and switch routing use "SBMD", customer-facing interfaces inside TPAP apps (Google Pay, PhonePe, Paytm, CRED) display "UPI Reserve Pay".

**In-App Messaging Example:** *"UPI Reserve Pay mandate — ₹10,000 blocked for [Merchant Name]"*

> **Merchant UX Best Practice:** Use "UPI Reserve Pay" in checkout banners and tooltips to build consumer familiarity with fund-blocking mechanics.

## 5. End-to-End Lifecycle & Architecture

The SBMD lifecycle operates across three distinct phases, separating authorization from physical fund transfer:

```text
[ Phase 1: Block ]  ---> Customer approves PIN ---> Bank liens funds ---> Mandate Active
[ Phase 2: Debit ]  ---> Merchant sends ReqPay  ---> Bank lifts lien ---> Debits exact amount
[ Phase 3: Release] ---> Expiry / Revoke API    ---> Bank drops lien ---> Unused balance freed
```

### Phase 1: Block (Mandate Creation)

1. Customer initiates mandate creation via Intent, QR, SDK, or Collect (Purpose Code 77 only).
2. The issuing bank prompts the user for their 4-digit or 6-digit UPI PIN.
3. Upon PIN validation, the issuing bank places a lien on the requested amount.
4. The switch returns confirmation back to the merchant.

**Sample Intent deep link structure for SBMD:**

```text
upi://mandate?ver=01&pn=MerchantName&cu=INR&amrule=MAX&block=Y
&purpose=77&mc=5552&mode=13&recur=ASPRESENTED&am=10000.00
&orgid=000000&rev=N&share=N&tn=Description&validitystart=27072026
&validityend=25102026&pa=merchant@bank&tr=REFERENCE123&txnType=CREATE
```

- `block=Y` — Triggers account lien.
- `recur=ASPRESENTED` — Configures multi-debit capability.
- `purpose=76 / 77` — Enforces industry-specific rules and ceilings.
- `amrule=MAX` — Declares amount as a maximum cap.

### Phase 2: Debit (Execution)

1. Merchant issues a `ReqPay` execution API call referencing the Unique Mandate Number (UMN) and required debit amount (≤ remaining lien).
2. The remitter bank verifies the digital signature attached to the mandate.
3. The bank temporarily lifts the lien, debits the exact requested execution amount, and re-applies the lien to any remaining unused balance:

   ```text
   Remaining Balance = Original Block − Σ(Successful Debits)
   ```

> **Mandatory Execution Rule:** Member banks are strictly prohibited from declining SBMD execution requests. All eligibility and status checks must be completed during initial mandate creation.

> **Timeout & Retries (Retail 77):** If an execution times out, it is treated as an immediate decline and reversed in real-time. Merchants can retry execution up to 3 times in 24 hours.

### Phase 3: Release (Unblock / Revoke)

Unutilized funds are released back to the customer's available balance under three conditions:

1. **Mandate Expiration:** Mandate validity period lapses (e.g., 90 days for retail).
2. **Explicit Revocation:** Merchant issues a `ReqMandate` (`type=REVOKE`) call.
3. **Exhaustion:** The blocked funds reach a zero balance through execution.

> **Revocation Rule:** Customers cannot directly revoke SBMD mandates inside their UPI apps. Revocation must be initiated by the merchant on behalf of the customer.

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cashfree SBMD Pre-Authorization &mdash; Integration Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --paper: #EEF3EE;
    --paper-alt: #E3EAE3;
    --card: #F7FAF7;
    --ink: #142019;
    --ink-soft: #47564C;
    --ink-faint: #7C8C81;
    --emerald: #0F6E4F;
    --emerald-dark: #0B4F39;
    --emerald-tint: #DCEBE2;
    --brick: #9C3B26;
    --brick-tint: #F3E2DB;
    --line: #C9D3C7;
    --line-strong: #A9B7AC;
    --code-bg: #12201A;
    --code-ink: #E7F1EA;
    --code-key: #7FE0AE;
    --code-comment: #6F8B7B;
    --radius: 10px;
    --font-display: 'Zilla Slab', Georgia, serif;
    --font-body: 'Inter', -apple-system, sans-serif;
    --font-mono: 'IBM Plex Mono', 'SFMono-Regular', Consolas, monospace;
    --maxw: 920px;
  }

  *{ box-sizing:border-box; }
  html{ scroll-behavior:smooth; }
  body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font-family:var(--font-body);
    line-height:1.6;
    -webkit-font-smoothing:antialiased;
  }
  @media (prefers-reduced-motion: reduce){
    html{ scroll-behavior:auto; }
    *{ animation-duration:0.001ms !important; transition-duration:0.001ms !important; }
  }

  a{ color:var(--emerald-dark); }
  :focus-visible{ outline:2px solid var(--emerald); outline-offset:2px; }

  /* ---------- layout shell ---------- */
  .shell{
    max-width:1180px;
    margin:0 auto;
    padding:0 24px;
    display:grid;
    grid-template-columns:220px minmax(0,1fr);
    gap:48px;
  }
  @media (max-width:900px){
    .shell{ grid-template-columns:1fr; }
  }

  /* ---------- header ---------- */
  header.doc-header{
    max-width:1180px;
    margin:0 auto;
    padding:56px 24px 40px;
    border-bottom:1px solid var(--line);
  }
  .eyebrow{
    font-family:var(--font-mono);
    font-size:12.5px;
    letter-spacing:0.09em;
    text-transform:uppercase;
    color:var(--emerald-dark);
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:14px;
  }
  .eyebrow::before{
    content:"";
    width:7px; height:7px;
    background:var(--emerald);
    display:inline-block;
    border-radius:1px;
    transform:rotate(45deg);
  }
  h1.title{
    font-family:var(--font-display);
    font-weight:700;
    font-size:clamp(32px,4.4vw,46px);
    line-height:1.08;
    margin:0 0 14px;
    letter-spacing:-0.01em;
    max-width:16ch;
  }
  .subtitle{
    font-size:16.5px;
    color:var(--ink-soft);
    max-width:56ch;
    margin:0 0 24px;
  }
  .badge-row{ display:flex; flex-wrap:wrap; gap:8px; }
  .badge{
    font-family:var(--font-mono);
    font-size:12px;
    padding:5px 10px;
    background:var(--emerald-tint);
    color:var(--emerald-dark);
    border-radius:5px;
    border:1px solid #C7DECD;
  }

  /* ---------- side nav ---------- */
  nav.toc{
    position:sticky;
    top:32px;
    align-self:start;
    padding-top:40px;
    font-size:13.5px;
  }
  nav.toc .toc-label{
    font-family:var(--font-mono);
    text-transform:uppercase;
    letter-spacing:0.08em;
    font-size:11px;
    color:var(--ink-faint);
    margin-bottom:12px;
  }
  nav.toc ol{
    list-style:none; margin:0; padding:0;
    border-left:1px solid var(--line);
  }
  nav.toc li{ margin:0; }
  nav.toc a{
    display:block;
    padding:7px 0 7px 16px;
    margin-left:-1px;
    border-left:1px solid transparent;
    color:var(--ink-soft);
    text-decoration:none;
  }
  nav.toc a:hover{ color:var(--ink); border-left-color:var(--line-strong); }
  @media (max-width:900px){ nav.toc{ display:none; } }

  /* ---------- main content ---------- */
  main{ padding:40px 0 80px; min-width:0; }
  section{ margin-bottom:64px; scroll-margin-top:24px; }
  h2{
    font-family:var(--font-display);
    font-size:26px;
    font-weight:700;
    margin:0 0 6px;
    display:flex;
    align-items:baseline;
    gap:10px;
  }
  h2 .num{
    font-family:var(--font-mono);
    font-size:14px;
    color:var(--emerald);
    font-weight:500;
  }
  .section-intro{ color:var(--ink-soft); margin:0 0 22px; max-width:62ch; }
  p{ margin:0 0 14px; }

  /* ---------- flow diagram (signature element) ---------- */
  .flow-card{
    background:var(--card);
    border:1px solid var(--line);
    border-radius:var(--radius);
    padding:28px 22px 20px;
    overflow-x:auto;
  }
  .flow-inner{ min-width:640px; }
  .flow-lanes{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    margin-bottom:26px;
  }
  .lane-name{
    font-family:var(--font-mono);
    font-size:12.5px;
    font-weight:600;
    text-align:center;
    color:var(--ink);
    padding-bottom:10px;
    border-bottom:2px solid var(--ink);
  }
  .lane-name span.role{
    display:block;
    font-family:var(--font-body);
    font-weight:400;
    font-size:10.5px;
    color:var(--ink-faint);
    text-transform:none;
    margin-top:2px;
  }
  .flow-steps{ position:relative; }
  .lane-guides{
    position:absolute; inset:0;
    display:grid;
    grid-template-columns:repeat(4,1fr);
    pointer-events:none;
  }
  .lane-guides div{
    border-left:1px dashed var(--line-strong);
    height:100%;
    margin:0 auto;
    width:1px;
  }
  .flow-step{
    position:relative;
    display:grid;
    grid-template-columns:34px 1fr;
    align-items:center;
    gap:10px;
    min-height:46px;
  }
  .step-badge{
    width:24px; height:24px;
    border-radius:50%;
    background:var(--ink);
    color:var(--paper);
    font-family:var(--font-mono);
    font-size:11px;
    display:flex; align-items:center; justify-content:center;
    z-index:2;
  }
  .lane-track{ position:relative; height:26px; }
  .connector{
    position:absolute;
    top:50%;
    height:2px;
    background:var(--emerald);
    transform:translateY(-50%);
  }
  .connector.reverse{ background:var(--ink-faint); }
  .connector.async{ background:transparent; border-top:2px dashed var(--brick); }
  .connector.wide{ background:transparent; border-top:2px dotted var(--ink-faint); }
  .connector::after{
    content:"";
    position:absolute;
    top:50%;
    width:0; height:0;
    border-top:5px solid transparent;
    border-bottom:5px solid transparent;
    transform:translateY(-50%);
  }
  .connector.forward::after{
    right:-1px;
    border-left:7px solid var(--emerald);
  }
  .connector.reverse::after{
    left:-1px;
    border-right:7px solid var(--ink-faint);
  }
  .connector.async::after{
    right:-1px;
    border-left:7px solid var(--brick);
  }
  .connector.wide::after{
    right:-1px;
    border-left:7px solid var(--ink-faint);
  }
  .step-label{
    position:absolute;
    top:-9px;
    left:50%;
    transform:translateX(-50%);
    background:var(--card);
    padding:0 8px;
    font-size:12px;
    white-space:nowrap;
    color:var(--ink);
  }
  .step-label code{
    font-family:var(--font-mono);
    font-size:11.5px;
    color:var(--emerald-dark);
  }
  .step-annotation{
    grid-column:2;
    font-size:12px;
    font-style:italic;
    color:var(--ink-faint);
    padding-left:6px;
  }
  .flow-legend{
    display:flex; flex-wrap:wrap; gap:18px;
    margin-top:22px;
    padding-top:16px;
    border-top:1px solid var(--line);
    font-size:12px;
    color:var(--ink-soft);
  }
  .flow-legend span{ display:inline-flex; align-items:center; gap:6px; }
  .swatch{ width:18px; height:0; border-top:2px solid var(--emerald); display:inline-block; }
  .swatch.reverse{ border-color:var(--ink-faint); }
  .swatch.async{ border-top-style:dashed; border-color:var(--brick); }
  .swatch.wide{ border-top-style:dotted; border-color:var(--ink-faint); }

  /* ---------- step articles ---------- */
  .step-article{
    background:var(--card);
    border:1px solid var(--line);
    border-radius:var(--radius);
    padding:24px 24px 22px;
    margin-bottom:20px;
  }
  .step-head{
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:6px;
    flex-wrap:wrap;
  }
  .step-num{
    font-family:var(--font-mono);
    font-size:12px;
    color:var(--emerald-dark);
    background:var(--emerald-tint);
    border-radius:5px;
    padding:2px 8px;
  }
  .step-head h3{
    font-family:var(--font-display);
    font-size:19px;
    margin:0;
    font-weight:600;
  }
  .endpoint{
    display:inline-flex;
    align-items:center;
    gap:8px;
    font-family:var(--font-mono);
    font-size:13px;
    margin:10px 0 16px;
    background:var(--ink);
    color:var(--paper);
    border-radius:6px;
    padding:7px 12px;
    width:fit-content;
  }
  .method{
    background:var(--emerald);
    color:#fff;
    padding:2px 7px;
    border-radius:4px;
    font-size:11px;
    font-weight:600;
  }
  .step-desc{ color:var(--ink-soft); font-size:14.5px; margin-bottom:14px; }

  table.headers-table{
    width:100%;
    border-collapse:collapse;
    font-size:13px;
    margin-bottom:16px;
  }
  table.headers-table th, table.headers-table td{
    text-align:left;
    padding:7px 10px;
    border-bottom:1px solid var(--line);
  }
  table.headers-table th{
    font-family:var(--font-mono);
    font-weight:500;
    color:var(--ink-faint);
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.04em;
  }
  table.headers-table td code{ font-family:var(--font-mono); font-size:12.5px; }

  /* ---------- tabbed code blocks ---------- */
  .code-block{
    background:var(--code-bg);
    border-radius:9px;
    overflow:hidden;
    margin:6px 0 4px;
  }
  .code-tabs{
    display:flex;
    align-items:center;
    background:#0D1712;
    padding:0 6px;
    border-bottom:1px solid #1F3327;
  }
  .code-tab{
    font-family:var(--font-mono);
    font-size:12px;
    color:#8FA398;
    background:transparent;
    border:none;
    padding:10px 14px 9px;
    cursor:pointer;
    border-bottom:2px solid transparent;
  }
  .code-tab:hover{ color:var(--code-ink); }
  .code-tab.active{
    color:var(--code-key);
    border-bottom-color:var(--code-key);
  }
  .copy-btn{
    margin-left:auto;
    font-family:var(--font-mono);
    font-size:11px;
    color:#8FA398;
    background:transparent;
    border:1px solid #24392C;
    border-radius:5px;
    padding:5px 9px;
    cursor:pointer;
  }
  .copy-btn:hover{ color:var(--code-ink); border-color:#3A5546; }
  .code-panel{ display:none; }
  .code-panel.active{ display:block; }
  pre{
    margin:0;
    padding:16px 18px;
    overflow-x:auto;
    font-family:var(--font-mono);
    font-size:12.8px;
    line-height:1.62;
    color:var(--code-ink);
  }
  pre .k{ color:var(--code-key); }
  pre .c{ color:var(--code-comment); }

  /* ---------- webhooks table ---------- */
  table.event-table{
    width:100%;
    border-collapse:collapse;
    font-size:13.5px;
    margin-bottom:20px;
    background:var(--card);
    border:1px solid var(--line);
    border-radius:var(--radius);
    overflow:hidden;
  }
  table.event-table th{
    text-align:left;
    background:var(--paper-alt);
    padding:10px 14px;
    font-family:var(--font-mono);
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:0.04em;
    color:var(--ink-faint);
  }
  table.event-table td{
    padding:10px 14px;
    border-top:1px solid var(--line);
    vertical-align:top;
  }
  table.event-table td:first-child{ font-family:var(--font-mono); font-size:12px; color:var(--emerald-dark); white-space:nowrap; }

  /* ---------- callout ---------- */
  .callout{
    display:flex;
    gap:14px;
    background:var(--brick-tint);
    border:1px solid #E3C3B4;
    border-left:4px solid var(--brick);
    border-radius:8px;
    padding:16px 18px;
    margin-bottom:20px;
  }
  .callout .mark{
    font-family:var(--font-display);
    font-weight:700;
    font-size:15px;
    color:var(--brick);
    flex-shrink:0;
  }
  .callout p{ margin:0 0 8px; font-size:14px; color:#5A2A1C; }
  .callout p:last-child{ margin-bottom:0; }
  .callout strong{ color:var(--ink); }

  ul.guardrail-list{ margin:0; padding-left:20px; }
  ul.guardrail-list li{ margin-bottom:10px; font-size:14.5px; color:var(--ink-soft); }
  ul.guardrail-list strong{ color:var(--ink); }

  footer{
    max-width:1180px;
    margin:0 auto;
    padding:28px 24px 60px;
    border-top:1px solid var(--line);
    font-size:12.5px;
    color:var(--ink-faint);
  }
</style>
</head>
<body>

<header class="doc-header">
  <div class="eyebrow">Integration Guide &middot; Cashfree Payments</div>
  <h1 class="title">SBMD Pre&#8209;Authorization for UPI</h1>
  <p class="subtitle">Block funds on a customer's account at checkout, capture the exact amount owed once the order is fulfilled, and release whatever's left &mdash; using Cashfree's Orders &amp; Pre&#8209;Authorization APIs.</p>
  <div class="badge-row">
    <span class="badge">Orders API</span>
    <span class="badge">UPI &middot; Single Block Multiple Debit</span>
    <span class="badge">Purpose Code 77</span>
    <span class="badge">Webhooks</span>
  </div>
</header>

<div class="shell">
  <nav class="toc">
    <div class="toc-label">On this page</div>
    <ol>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#flow">Integration flow</a></li>
      <li><a href="#step-1">1. Create pre-auth order</a></li>
      <li><a href="#step-2">2. Initiate payment</a></li>
      <li><a href="#step-3">3. Capture</a></li>
      <li><a href="#step-4">4. Void / release</a></li>
      <li><a href="#webhooks">Webhook events</a></li>
      <li><a href="#guardrails">Guardrails</a></li>
    </ol>
  </nav>

  <main>

    <section id="overview">
      <p class="section-intro" style="margin-top:6px;">Cashfree Payments provides pre-authorization and SBMD (Single Block, Multiple Debit) capabilities through its Orders &amp; Pre-Authorization APIs. This lets you place a lien on a customer's bank balance via UPI, then debit it in one or more partial captures as the order is fulfilled &mdash; releasing anything uncaptured back to the customer.</p>
    </section>

    <section id="flow">
      <h2><span class="num">&sect;</span> Integration flow</h2>
      <p class="section-intro">Four parties are involved: the customer, your merchant app, Cashfree's payment gateway, and the customer's issuing bank. Fourteen steps carry a payment from checkout to final settlement.</p>

      <div class="flow-card">
        <div class="flow-inner">
          <div class="flow-lanes">
            <div class="lane-name">Customer</div>
            <div class="lane-name">Merchant App<span class="role">your backend</span></div>
            <div class="lane-name">Cashfree PG<span class="role">gateway</span></div>
            <div class="lane-name">Issuing Bank<span class="role">bank rail</span></div>
          </div>

          <div class="flow-steps">
            <div class="lane-guides"><div></div><div></div><div></div><div></div></div>

            <!-- 1 -->
            <div class="flow-step"><div class="step-badge">1</div>
              <div class="lane-track"><div class="connector forward" style="left:12.5%;width:25%;"></div><div class="step-label">Checkout</div></div></div>
            <!-- 2 -->
            <div class="flow-step"><div class="step-badge">2</div>
              <div class="lane-track"><div class="connector forward" style="left:37.5%;width:25%;"></div><div class="step-label"><code>POST /pg/orders</code> &middot; authorize_only=true</div></div></div>
            <!-- 2 return -->
            <div class="flow-step"><div class="step-badge">&larr;</div>
              <div class="lane-track"><div class="connector reverse" style="left:37.5%;width:25%;"></div><div class="step-label">returns payment_session_id</div></div></div>
            <!-- 3 -->
            <div class="flow-step"><div class="step-badge">3</div>
              <div class="lane-track"><div class="connector forward" style="left:12.5%;width:25%;"></div><div class="step-label">Pay with UPI</div></div></div>
            <!-- 4 -->
            <div class="flow-step"><div class="step-badge">4</div>
              <div class="lane-track"><div class="connector forward" style="left:37.5%;width:25%;"></div><div class="step-label"><code>POST /pg/orders/pay</code> &middot; sbmd=true</div></div></div>
            <!-- 5 -->
            <div class="flow-step"><div class="step-badge">5</div>
              <div class="lane-track"><div class="connector forward" style="left:62.5%;width:25%;"></div><div class="step-label">Trigger lien request</div></div></div>
            <!-- 6 -->
            <div class="flow-step"><div class="step-badge">6</div>
              <div class="lane-track"><div class="connector wide" style="left:12.5%;width:75%;"></div><div class="step-label">Customer enters UPI PIN (direct, out-of-band)</div></div></div>
            <!-- 7 -->
            <div class="flow-step"><div class="step-badge">7</div>
              <div class="lane-track"><div class="connector reverse" style="left:62.5%;width:25%;"></div><div class="step-label">Lien placed confirmation</div></div></div>
            <!-- 8 -->
            <div class="flow-step"><div class="step-badge">8</div>
              <div class="lane-track"><div class="connector async" style="left:37.5%;width:25%;"></div><div class="step-label">Webhook: MANDATE_ACTIVE</div></div></div>
            <!-- 9 annotation -->
            <div class="flow-step"><div class="step-badge">9</div>
              <div class="step-annotation">Service fulfilled &mdash; e.g. order delivered</div></div>
            <!-- 10 -->
            <div class="flow-step"><div class="step-badge">10</div>
              <div class="lane-track"><div class="connector forward" style="left:37.5%;width:25%;"></div><div class="step-label"><code>POST /capture</code></div></div></div>
            <!-- 11 -->
            <div class="flow-step"><div class="step-badge">11</div>
              <div class="lane-track"><div class="connector forward" style="left:62.5%;width:25%;"></div><div class="step-label">Execute debit</div></div></div>
            <!-- 12 -->
            <div class="flow-step"><div class="step-badge">12</div>
              <div class="lane-track"><div class="connector reverse" style="left:37.5%;width:25%;"></div><div class="step-label">Capture success</div></div></div>
            <!-- 13 -->
            <div class="flow-step"><div class="step-badge">13</div>
              <div class="lane-track"><div class="connector forward" style="left:37.5%;width:25%;"></div><div class="step-label"><code>POST /void</code> &middot; release</div></div></div>
            <!-- 14 -->
            <div class="flow-step"><div class="step-badge">14</div>
              <div class="lane-track"><div class="connector forward" style="left:62.5%;width:25%;"></div><div class="step-label">Lift remaining lien</div></div></div>

          </div>

          <div class="flow-legend">
            <span><i class="swatch"></i> API call</span>
            <span><i class="swatch reverse"></i> Response / confirmation</span>
            <span><i class="swatch async"></i> Async webhook</span>
            <span><i class="swatch wide"></i> Direct bank-rail step</span>
          </div>
        </div>
      </div>
    </section>

    <section id="steps">
      <h2 style="margin-bottom:20px;"><span class="num">&sect;</span> Step-by-step implementation</h2>

      <!-- STEP 1 -->
      <article class="step-article" id="step-1">
        <div class="step-head"><span class="step-num">Step 1</span><h3>Create a pre-authorization order</h3></div>
        <p class="step-desc">Call Cashfree's Create Order API with <code style="font-family:var(--font-mono);">authorize_only: true</code> in the order configuration.</p>
        <div class="endpoint"><span class="method">POST</span> /pg/orders</div>
        <table class="headers-table">
          <tr><th>Header</th><th>Value</th></tr>
          <tr><td><code>x-client-id</code></td><td><code>&lt;YOUR_CASHFREE_APP_ID&gt;</code></td></tr>
          <tr><td><code>x-client-secret</code></td><td><code>&lt;YOUR_CASHFREE_SECRET_KEY&gt;</code></td></tr>
          <tr><td><code>x-api-version</code></td><td><code>2023-08-01</code> (or latest)</td></tr>
        </table>
        <div class="code-block" data-group="step1">
          <div class="code-tabs">
            <button class="code-tab active" data-tab="json">Request payload</button>
            <button class="copy-btn" data-copy>Copy</button>
          </div>
          <div class="code-panel active" data-panel="json"><pre><code>{
  <span class="k">"order_id"</span>: <span class="k">"ORDER_SBMD_100293"</span>,
  <span class="k">"order_amount"</span>: 2000.00,
  <span class="k">"order_currency"</span>: <span class="k">"INR"</span>,
  <span class="k">"customer_details"</span>: {
    <span class="k">"customer_id"</span>: <span class="k">"CUST_88912"</span>,
    <span class="k">"customer_name"</span>: <span class="k">"Rahul Sharma"</span>,
    <span class="k">"customer_email"</span>: <span class="k">"rahul.sharma@example.com"</span>,
    <span class="k">"customer_phone"</span>: <span class="k">"9999999999"</span>
  },
  <span class="k">"order_meta"</span>: {
    <span class="k">"return_url"</span>: <span class="k">"https://yourmerchant.com/order_status?order_id={order_id}"</span>,
    <span class="k">"notify_url"</span>: <span class="k">"https://yourmerchant.com/api/webhooks/cashfree"</span>
  },
  <span class="k">"order_tags"</span>: {
    <span class="k">"flow"</span>: <span class="k">"SBMD_RESERVE_PAY"</span>
  }
}</code></pre></div>
        </div>
      </article>

      <!-- STEP 2 -->
      <article class="step-article" id="step-2">
        <div class="step-head"><span class="step-num">Step 2</span><h3>Initiate payment &mdash; pay request with SBMD/OTM</h3></div>
        <p class="step-desc">Invoke the Order Pay API with the UPI payment payload and the SBMD parameters (shown here for UPI intent / dynamic QR mode).</p>
        <div class="endpoint"><span class="method">POST</span> /pg/orders/pay</div>
        <div class="code-block" data-group="step2">
          <div class="code-tabs">
            <button class="code-tab active" data-tab="json">Request payload</button>
            <button class="code-tab" data-tab="node">Node.js</button>
            <button class="copy-btn" data-copy>Copy</button>
          </div>
          <div class="code-panel active" data-panel="json"><pre><code>{
  <span class="k">"payment_session_id"</span>: <span class="k">"session_g7a8F9d0K1..."</span>,
  <span class="k">"payment_method"</span>: {
    <span class="k">"upi"</span>: {
      <span class="k">"channel"</span>: <span class="k">"intent"</span>,
      <span class="k">"authorize_only"</span>: true,
      <span class="k">"sbmd"</span>: true,
      <span class="k">"purpose_code"</span>: <span class="k">"77"</span>,
      <span class="k">"mandate_details"</span>: {
        <span class="k">"max_amount"</span>: 2000.00,
        <span class="k">"start_date"</span>: <span class="k">"2026-07-29"</span>,
        <span class="k">"end_date"</span>: <span class="k">"2026-10-27"</span>
      }
    }
  }
}</code></pre></div>
          <div class="code-panel" data-panel="node"><pre><code><span class="c">// Node.js SDK</span>
<span class="k">const</span> { Cashfree } = require(<span class="k">"cashfree-pg"</span>);

Cashfree.XClientId = <span class="k">"YOUR_APP_ID"</span>;
Cashfree.XClientSecret = <span class="k">"YOUR_SECRET_KEY"</span>;
Cashfree.XEnvironment = Cashfree.Environment.PRODUCTION;

<span class="k">async function</span> createSBMDPayment(paymentSessionId) {
  <span class="k">try</span> {
    <span class="k">const</span> request = {
      payment_session_id: paymentSessionId,
      payment_method: {
        upi: {
          channel: <span class="k">"intent"</span>,
          authorize_only: true,
          sbmd: true,
          purpose_code: <span class="k">"77"</span>
        }
      }
    };

    <span class="k">const</span> response = <span class="k">await</span> Cashfree.PGPay(<span class="k">"2023-08-01"</span>, request);
    console.log(<span class="k">"Pay Response:"</span>, response.data);
    <span class="c">// Redirect or trigger Intent flow on user device using response.data.data.payload</span>
  } <span class="k">catch</span> (error) {
    console.error(<span class="k">"Error initiating SBMD payment:"</span>, error.response.data);
  }
}</code></pre></div>
        </div>
      </article>

      <!-- STEP 3 -->
      <article class="step-article" id="step-3">
        <div class="step-head"><span class="step-num">Step 3</span><h3>Capture / execute debit against blocked funds</h3></div>
        <p class="step-desc">Once the lien is active, execute single or multiple partial debits against the blocked funds until the total captured amount equals the original block amount.</p>
        <div class="endpoint"><span class="method">POST</span> /pg/orders/{order_id}/authorization/capture</div>
        <div class="code-block" data-group="step3">
          <div class="code-tabs">
            <button class="code-tab active" data-tab="json">Request payload</button>
            <button class="code-tab" data-tab="python">Python</button>
            <button class="copy-btn" data-copy>Copy</button>
          </div>
          <div class="code-panel active" data-panel="json"><pre><code>{
  <span class="k">"action"</span>: <span class="k">"CAPTURE"</span>,
  <span class="k">"amount"</span>: 450.00,
  <span class="k">"reference_id"</span>: <span class="k">"EXEC_CAPTURE_001"</span>,
  <span class="k">"remark"</span>: <span class="k">"Partial execution for mini-order #1"</span>
}</code></pre></div>
          <div class="code-panel" data-panel="python"><pre><code><span class="k">import</span> requests

url = <span class="k">"https://api.cashfree.com/pg/orders/ORDER_SBMD_100293/authorization/capture"</span>

headers = {
    <span class="k">"accept"</span>: <span class="k">"application/json"</span>,
    <span class="k">"content-type"</span>: <span class="k">"application/json"</span>,
    <span class="k">"x-api-version"</span>: <span class="k">"2023-08-01"</span>,
    <span class="k">"x-client-id"</span>: <span class="k">"YOUR_APP_ID"</span>,
    <span class="k">"x-client-secret"</span>: <span class="k">"YOUR_SECRET_KEY"</span>
}

payload = {
    <span class="k">"action"</span>: <span class="k">"CAPTURE"</span>,
    <span class="k">"amount"</span>: 450.00,
    <span class="k">"reference_id"</span>: <span class="k">"EXEC_CAPTURE_001"</span>,
    <span class="k">"remark"</span>: <span class="k">"Partial debit execution"</span>
}

response = requests.post(url, json=payload, headers=headers)
print(<span class="k">"Capture Status Code:"</span>, response.status_code)
print(<span class="k">"Response:"</span>, response.json())</code></pre></div>
        </div>
      </article>

      <!-- STEP 4 -->
      <article class="step-article" id="step-4">
        <div class="step-head"><span class="step-num">Step 4</span><h3>Void / release remaining blocked funds</h3></div>
        <p class="step-desc">When fulfillment is complete, or if the order is canceled, call the Void API to release the balance lien back to the customer instantly.</p>
        <div class="endpoint"><span class="method">POST</span> /pg/orders/{order_id}/authorization/void</div>
        <div class="code-block" data-group="step4">
          <div class="code-tabs">
            <button class="code-tab active" data-tab="json">Request payload</button>
            <button class="code-tab" data-tab="curl">cURL</button>
            <button class="copy-btn" data-copy>Copy</button>
          </div>
          <div class="code-panel active" data-panel="json"><pre><code>{
  <span class="k">"action"</span>: <span class="k">"VOID"</span>,
  <span class="k">"remark"</span>: <span class="k">"Order processing completed, unblocking remaining balance."</span>
}</code></pre></div>
          <div class="code-panel" data-panel="curl"><pre><code>curl --request POST \
  --url https://api.cashfree.com/pg/orders/ORDER_SBMD_100293/authorization/void \
  --header <span class="k">'accept: application/json'</span> \
  --header <span class="k">'content-type: application/json'</span> \
  --header <span class="k">'x-api-version: 2023-08-01'</span> \
  --header <span class="k">'x-client-id: YOUR_APP_ID'</span> \
  --header <span class="k">'x-client-secret: YOUR_SECRET_KEY'</span> \
  --data <span class="k">'
{
  "action": "VOID",
  "remark": "Releasing remaining lien amount to customer"
}
'</span></code></pre></div>
        </div>
      </article>
    </section>

    <section id="webhooks">
      <h2><span class="num">&sect;</span> Webhook events</h2>
      <p class="section-intro">Configure webhooks in your Cashfree Merchant Dashboard to handle asynchronous mandate updates.</p>
      <table class="event-table">
        <tr><th>Event</th><th>Fired when</th></tr>
        <tr><td>MANDATE_CREATED</td><td>The issuing bank successfully liens customer funds.</td></tr>
        <tr><td>CAPTURE_SUCCESS</td><td>A partial or full debit against the lien succeeds.</td></tr>
        <tr><td>MANDATE_REVOKED / VOID_SUCCESS</td><td>The lien is removed and remaining funds are freed.</td></tr>
      </table>
      <div class="code-block" data-group="webhook">
        <div class="code-tabs">
          <span class="code-tab active" style="cursor:default;">MANDATE_CREATED_NOTIFICATION</span>
          <button class="copy-btn" data-copy>Copy</button>
        </div>
        <div class="code-panel active" data-panel="wh"><pre><code>{
  <span class="k">"type"</span>: <span class="k">"MANDATE_CREATED_NOTIFICATION"</span>,
  <span class="k">"raw_data"</span>: {
    <span class="k">"order_id"</span>: <span class="k">"ORDER_SBMD_100293"</span>,
    <span class="k">"umn"</span>: <span class="k">"123456789012@upi"</span>,
    <span class="k">"blocked_amount"</span>: 2000.00,
    <span class="k">"status"</span>: <span class="k">"SUCCESS"</span>,
    <span class="k">"purpose_code"</span>: <span class="k">"77"</span>
  }
}</code></pre></div>
      </div>
    </section>

    <section id="guardrails">
      <h2><span class="num">&sect;</span> Operational guardrails &amp; best practices</h2>
      <div class="callout">
        <span class="mark">!</span>
        <div>
          <p><strong>MCC alignment</strong> &mdash; Purpose Code 76 requires stockbroking MCC 6211. General retail e-commerce must use Purpose Code 77.</p>
        </div>
      </div>
      <ul class="guardrail-list">
        <li><strong>Refunds vs. voids.</strong> You cannot use the Refund API on uncaptured money. Use the Void API to unblock locked funds, and reserve the Refund API for funds that have already been debited/captured.</li>
        <li><strong>OMS tracking.</strong> Ensure your order management system can map multiple capture IDs against a single parent <code style="font-family:var(--font-mono);">order_id</code>.</li>
        <li><strong>TDR pricing.</strong> Gateway TDR applies upon successful mandate creation (block), regardless of whether you capture the full amount or subsequently void the mandate.</li>
      </ul>
    </section>

  </main>
</div>

<footer>Cashfree Payments &middot; Orders &amp; Pre-Authorization API &middot; SBMD for UPI</footer>

<script>
  // Tabbed code blocks
  document.querySelectorAll('.code-block').forEach(function(block){
    var tabs = block.querySelectorAll('.code-tab[data-tab]');
    var panels = block.querySelectorAll('.code-panel');
    tabs.forEach(function(tab){
      tab.addEventListener('click', function(){
        tabs.forEach(function(t){ t.classList.remove('active'); });
        panels.forEach(function(p){ p.classList.remove('active'); });
        tab.classList.add('active');
        var target = block.querySelector('.code-panel[data-panel="' + tab.dataset.tab + '"]');
        if(target){ target.classList.add('active'); }
      });
    });

    // Copy button copies the currently active panel's text
    var copyBtn = block.querySelector('[data-copy]');
    if(copyBtn){
      copyBtn.addEventListener('click', function(){
        var active = block.querySelector('.code-panel.active code');
        if(!active) return;
        var text = active.innerText;
        navigator.clipboard.writeText(text).then(function(){
          var original = copyBtn.textContent;
          copyBtn.textContent = 'Copied';
          setTimeout(function(){ copyBtn.textContent = original; }, 1400);
        }).catch(function(){
          copyBtn.textContent = 'Press Ctrl/Cmd+C';
          setTimeout(function(){ copyBtn.textContent = 'Copy'; }, 1400);
        });
      });
    }
  });
</script>

</body>
</html>