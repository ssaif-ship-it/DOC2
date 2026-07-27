During checkout, multiple points of failure exist outside a merchant's direct control — a bank's Core Banking System (CBS) may go offline, an acquiring partner's API might time out, or the NPCI switch could experience network congestion. If traffic is statically routed down a single gateway pipe during these events, conversion rates fluctuate heavily.

Cashfree's Smart Routing engine continuously measures real-time performance across all acquiring channels, detects degradation within seconds, and automatically redirects traffic to healthy payment paths to protect checkout conversion.

## 1. Deconstructing Transaction Success Rate (SR)

Success Rate (SR) measures the efficiency of your payment checkout and is defined as:

```text
Success Rate (SR) = (Successful Transactions / Total Attempted Transactions) × 100
```

In a standard steady state on UPI, overall ecosystem SR averages ~80%. Non-successful attempts split into two primary categories:

```text
[ Total Attempted Transactions ]
       ├── Successful Payments (~80%)
       ├── User Drops (~13%)        --> User closed app, abandoned checkout, or collect timed out.
       └── Technical Failures (~7%) --> Bank CBS downtime, network timeouts, routing drops.
```

### Factors Influencing Success Rate

| Factor | Controllable via Smart Routing? | Impact Mitigation |
| :--- | :--- | :--- |
| Acquiring Bank / Gateway Health | **Yes** | Dynamic Routing shifts traffic away from failing acquirers instantly. |
| Issuing Bank (Remitter) CBS Health | Partial | Warn customer before PIN entry; route card flows to higher-performing issuer pipes. |
| PSP App Outages (Google Pay, PhonePe) | Partial | Reorder or deprioritize degraded PSP app options on hosted checkout. |
| NPCI Switch Congestion | **No** | System-wide queueing; fallback to non-UPI rails (Cards / NetBanking). |
| Merchant Checkout UX / Expiry | **Yes** | Eliminate VPA entry typos (Intent/QR); optimize collect timeouts. |

## 2. Real-Time Transaction Health Engine

Cashfree's dedicated Transaction Health Engine continuously monitors telemetry across all acquiring channels and issuing banks.

### 2.1 Multi-Granular Monitoring

Success and failure counts are aggregated from system metrics across multiple layers:

```text
                                [ Health Engine ]
                                       |
     +-------------------+-------------+-------------+------------------+
     v                   v                           v                  v
Cashfree-Wide       Per Merchant                Per Issuer         Per Payment Mode
(Overall Switch)   (Your Traffic)              (HDFC, SBI, ICICI)   (Intent, QR, CC)
 15-60s Window      15-60s Window               60s Window          60s Window
```

- **UPI data lookback:** Evaluates metrics across rolling 15-second to 5-minute windows for merchant-level traffic, and 15-to-60-minute windows for network-wide baseline health.
- **Card data lookback:** Evaluates metrics across rolling 15-minute windows for merchant-level traffic and up to 240 minutes for broader gateway health.

### 2.2 Minimum Statistical Thresholds

To prevent routing decisions based on statistical noise (e.g., a single failed transaction dropping an acquirer's rate to 0%), the algorithm enforces minimum sample volume thresholds:

| Level | Minimum Required Sample | Fallback Behavior |
| :--- | :--- | :--- |
| Merchant + Issuer Level | 5 txns in 15 mins | Falls back to Merchant Overall. |
| Merchant Overall | 5 txns in 15 mins | Falls back to Cashfree + Issuer Level. |
| Cashfree + Issuer Level | 50 txns in 15 mins | Falls back to Cashfree Overall. |
| Cashfree Overall | Default Baseline | System safety net. |

### 2.3 Automated Incident Flagging

An acquiring route is automatically marked as degraded/incident when:

- Real-time stream processing flags anomalous failure spikes.
- The route's Success Rate drops below 5% for the active evaluation window.

> **Exploratory traffic throttling:** When an incident is flagged, traffic to that gateway is throttled to a maximum of 5 txns/merchant (and 20 txns Cashfree-wide). This limits customer risk while maintaining enough probe traffic to detect when the gateway recovers.

## 3. Dynamic Routing (DR) Mechanics

### 3.1 The Routing Algorithm (Thompson Sampling)

When an Order Pay API request is initiated, the decision engine evaluates all eligible acquiring pipelines using a probabilistic Thompson Sampling (Beta Distribution) model. This balances exploitation (routing to the current best-performing gateway) with exploration (probing recovered gateways).

```text
Sampled Probability ~ Beta(Successes + 1, Failures + 1)
```

```text
Customer Initiates Payment
         |
         v
Identify Eligible Gateway Terminals (MID, MCC, Payment Method)
         |
         v
Fetch Live Success/Failure Telemetry (Merchant -> Network Fallback)
         |
         v
Draw Probabilistic Sample from Beta Distribution per Gateway
         |
         v
Select Gateway with Highest Sampled Value & Execute
         |
         v
Log Terminal Response (Success/Failure) --> Update Model
```

- **Fast recovery detection:** As soon as probe transactions succeed on a recovering gateway, its distribution shifts positive, and the system scales traffic back up within minutes.
- **Multi-terminal failover:** Traffic is distributed across multiple acquiring MIDs. If two acquirers suffer concurrent downtime, traffic automatically falls through to tertiary and quaternary routes.

### 3.2 Routing Evolution

```text
[ DR V1.1 (Merchant Mean SR) ] --> [ Optiwise Pro (SR + Cost) ] --> [ Issuer-Level DR ] --> [ ML Supervised DR ]
   Current UPI Default              Current Card Engine              Top-4 Bank Pipes        Advanced Feature
```

- **Optiwise Pro (Cards):** Factors in acquiring costs (interchange + MDR buy price) alongside SR, selecting the most cost-effective gateway among those meeting health thresholds.
- **Issuer-Level DR:** Evaluates issuing bank performance per acquirer (e.g., routing SBI RuPay cards via Acquirer A, but HDFC Visa cards via Acquirer B).

## 4. Intelligent Retry Routing & Orchestration

### 4.1 User-Context Retry Routing

If a payment fails, repeating the retry attempt over the exact same failing gateway route increases drop-off risk. Cashfree tracks state within a customer's session window (~10 minutes):

```text
[ Attempt 1 ] --> Route to Gateway A --> FAILED (Saved to Session Context)
                        |
                        v  (User clicks 'Try Again')
[ Attempt 2 ] --> Route to Gateway B (Next Best Route) --> SUCCESS
```

- Session context is maintained per payment method (switching from UPI to Card resets context).
- Fully transparent to the customer; backend handles route rotation automatically.

### 4.2 Multi-Gateway Orchestration (Flowwise)

For enterprise merchants operating independent merchant IDs across multiple payment aggregators, Flowwise acts as an orchestration layer above individual gateways:

| Orchestration Rule | Operational Logic | Primary Benefit |
| :--- | :--- | :--- |
| **Smart Routing** | Dynamic ML selection across all configured PAs. | Maximize SR across gateways. |
| **Smart Routing with Weights** | Optimizes SR within fixed volume allocations (e.g., 60% PA1, 40% PA2). | Honor commercial commitments while optimizing SR. |
| **Threshold Routing** | Routes 100% to Primary PA; switches to Backup PA if SR drops below threshold (e.g., <75%). | Automated failover with a single preferred vendor. |

## 5. Issuing Bank Downtime Detection

A major cause of sudden checkout failures is issuing bank CBS downtime (e.g., a customer's bank undergoing maintenance). Cashfree tracks remitter bank health across 15-minute rolling windows for the top issuing banks.

```text
[ Prometheus Telemetry ] --> [ Time-Series Anomaly Detection ] --> [ Remitter Bank Issue Flagged ]
                                                                              |
                                                                              v
                                                                   [ Auto-Trigger Options ]
                                                                     +-- Merchant Webhooks
                                                                     +-- Checkout Alerts
                                                                     +-- Mode Deprioritization
```

When an issuer downtime is detected:

1. An automated incident is generated.
2. Subscribed merchants receive real-time webhook/email alerts.
3. Hosted checkouts present contextual guidance to the customer (*"SBI UPI servers are currently experiencing low success rates. Try using another account or Card."*).

## 6. Merchant Visibility & Controls

### 6.1 Programmatic Incident APIs & Webhooks

Merchants with custom checkout UIs can consume incident telemetry programmatically using the Incidents API:

**API endpoint:**

```http
GET /pg/incidents?type=UNSCHEDULED&status=OPEN&payment_method=upi
```

**Real-time incident webhook schema:**

```json
{
  "type": "DOWNTIME_INCIDENT",
  "data": {
    "incident": {
      "id": "INCIDENT_UPI_HDFCBANK_882",
      "severity": "HIGH",
      "message": "HDFC Bank UPI network is experiencing degraded response times.",
      "start_time": "2026-07-27T18:30:00+05:30",
      "status": "OPEN",
      "type": "UNSCHEDULED",
      "payment_method": "upi",
      "instrument": {
        "bank": "HDFC",
        "psp": null
      }
    }
  }
}
```

### 6.2 Custom Success Rate Threshold Alerts

In the Cashfree Merchant Dashboard (**Incidents & Outages > Alerts**), merchants can configure custom operational thresholds:

- **Threshold condition:** Trigger an alert when Payment Method SR drops below X% (e.g., UPI SR < 70%).
- **Minimum volume filter:** Evaluate the rule only after a minimum of N transactions (e.g., ≥ 50 txns) to avoid false positives.
- **Notification channels:** Slack, Webhooks, Email, WhatsApp.

## 7. Quantified Success Rate Impact

Combining dynamic routing, user retry tracking, and downtime mitigation yields measurable SR improvements over static routing:

<div class="cf-sr-waterfall" style="border:1px solid #E5E7EB; border-radius:0.75rem; padding:1.25rem 1.5rem; margin:1.5rem 0;">
<style>
.cf-sr-waterfall .cf-step { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px dashed #E5E7EB; font-size:14px; gap:16px; }
.cf-sr-waterfall .cf-step:last-child { border-bottom:none; }
.cf-sr-waterfall .cf-label { color:#374151; }
.cf-sr-waterfall .cf-value { color:#059669; font-weight:600; white-space:nowrap; }
.cf-sr-waterfall .cf-value.cf-neutral { color:#6B7280; font-weight:500; }
.cf-sr-waterfall .cf-total { font-weight:700; color:#5A28A3; background:#F4F0FA; border-radius:0.5rem; padding:12px 14px; margin-top:8px; }
</style>
  <div class="cf-step"><span class="cf-label">Static / Single Gateway Routing</span><span class="cf-value cf-neutral">Baseline SR (~75%–78%)</span></div>
  <div class="cf-step"><span class="cf-label">+ Dynamic Routing (Normal)</span><span class="cf-value">+0.5% to +1.0% SR</span></div>
  <div class="cf-step"><span class="cf-label">+ Dynamic Routing (Outages)</span><span class="cf-value">+2.0% or higher SR recovery</span></div>
  <div class="cf-step"><span class="cf-label">+ Issuer-Level Routing (Cards)</span><span class="cf-value">+0.3% to +0.5% SR</span></div>
  <div class="cf-step"><span class="cf-label">+ Native OTP & Retry Context</span><span class="cf-value">+0.5% to +0.7% SR</span></div>
  <div class="cf-step cf-total"><span class="cf-label" style="color:#5A28A3;">Cashfree Optimized Routing</span><span class="cf-value" style="color:#5A28A3;">Net Gain: +2.0% to +5.0% SR</span></div>
</div>

## 8. Go-Live Optimization Checklist for Merchants

- [ ] **Multiple Terminals Configured:** Verify with your account manager that your account has secondary acquiring terminals configured for UPI and Cards.
- [ ] **Dynamic Routing Enabled:** Confirm DR is enabled on your merchant account (default ON for UPI; configurable for Cards).
- [ ] **Subscribe to Incident Webhooks:** Integrate `DOWNTIME_INCIDENT` webhooks to update custom checkout UI banners during bank downtime.
- [ ] **Set Up SR Alerts:** Configure Slack/Email alerts for SR dips in Dashboard.
- [ ] **Leverage Hosted Checkout Automations:** If using Cashfree Hosted Checkout, verify that automated downtime reordering and warning banners are active.