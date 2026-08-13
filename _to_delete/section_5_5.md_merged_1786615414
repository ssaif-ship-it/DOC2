Payment checkout flows involve multiple external dependencies, including acquiring bank APIs, issuing bank Core Banking Systems (CBS), and national switches like NPCI. A technical downtime or network spike at any of these points can directly impact checkout conversion if traffic is statically routed down a single channel.

Smart Routing continuously measures real-time performance across all acquiring channels, detects network degradation within seconds, and dynamically shifts traffic to healthy payment paths to protect your checkout Success Rate (SR).

## 1. Understanding Transaction Success Rate (SR)

Transaction Success Rate (SR) measures the operational efficiency of your payment flow. It is defined as:

> **Success Rate (SR) = (Successful Transactions / Total Attempted Transactions) x 100**

In standard ecosystem conditions on UPI, overall baseline SR runs in the 92% to 97% range across major PSPs and direct NPCI integrations. Non-successful attempts fall into two distinct categories:

*   **User Drops:** Customer-initiated actions, such as closing the app, abandoning the payment page, or allowing the payment collect request to time out. This accounts for most of the remaining gap.
*   **Technical Failures:** Infrastructure-level issues, including issuing bank CBS downtime, gateway API timeouts, or network congestion. NPCI's own ecosystem data shows this share falling from roughly 8 to 10% around 2016 to under 1% by 2024 to 2025.

<!-- Claude, fact-check note for Saif: replaced the old "~80% baseline SR, User Drops ~13%, Technical Failures ~7%" figures. Every current source I could find (NPCI's own ecosystem stats, and PSP-published figures from Razorpay, PayU, and Cashfree's own blog) puts blended UPI success rates today at roughly 92 to 97%, with technical/ecosystem failures down near 1%, not 7. The old ~80% figure matches where UPI was around 2016 to 2018, not now. I did not find a precise verified split for User Drops specifically, so I described it as "most of the remaining gap" rather than inventing a percentage. If you have a specific current SR or drop-rate figure from Cashfree's own dashboards, use that instead of my range, it would be more precise than public industry data. -->

## 2. UPI Failure Modes & Mitigation Matrix

To maintain high availability, the Smart Routing engine categorizes payment failure factors based on controllable mitigation capabilities:

<table style="border-collapse: collapse; width: 100%;">
  <thead>
    <tr>
      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f2f2f2; text-align: left;">Failure Factor</th>
      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f2f2f2; text-align: left;">Ecosystem Impact</th>
      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f2f2f2; text-align: left;">Controllable via Smart Routing?</th>
      <th style="border: 1px solid #ccc; padding: 8px 12px; background-color: #f2f2f2; text-align: left;">Automated Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Acquiring Gateway Health</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Aggregator/Gateway API timeouts or infrastructure failure.</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Yes</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Shifts traffic instantly to secondary healthy acquiring paths.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Issuing Bank CBS Health</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Remitter bank maintenance or sudden downtime (e.g., SBI, HDFC).</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Partial</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Warns customers prior to payment or deprioritizes impacted issuers.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">PSP App Outages</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Application degradation (e.g., Google Pay, PhonePe, Paytm).</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Partial</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Reorders or deprioritizes degraded UPI apps on hosted checkout.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">NPCI Switch Congestion</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Core network queueing across the entire UPI network.</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">No</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Recommends non-UPI rails (Cards or NetBanking) on checkout UI.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Checkout UI / User Input</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Invalid VPA inputs or manual entry typos.</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Yes</td>
      <td style="border: 1px solid #ccc; padding: 8px 12px;">Replaces manual VPA entry with seamless UPI Intent or Dynamic QR flows.</td>
    </tr>
  </tbody>
</table>

## 3. How Smart Routing Works

The Smart Routing engine operates as an automated traffic orchestrator operating between your checkout session and acquiring channels.

<div style="margin:1.75rem 0;display:flex;flex-direction:column;align-items:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">

  <div style="width:100%;max-width:340px;background:#ffffff;border:1px solid #E5E7EB;border-radius:10px;padding:14px 18px;text-align:center;box-shadow:0 1px 2px rgba(16,24,40,0.05);">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Step 1</div>
    <div style="font-size:15px;font-weight:600;color:#111827;">Customer initiates payment</div>
  </div>

  <div style="width:2px;height:26px;background:#D1D5DB;"></div>

  <div style="width:100%;max-width:340px;background:#ffffff;border:1px solid #E5E7EB;border-radius:10px;padding:14px 18px;text-align:center;box-shadow:0 1px 2px rgba(16,24,40,0.05);">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#9CA3AF;margin-bottom:4px;">Step 2</div>
    <div style="font-size:15px;font-weight:600;color:#111827;">Live health check</div>
    <div style="font-size:13px;color:#6B7280;margin-top:2px;">Gateway and bank status</div>
  </div>

  <div style="width:2px;height:26px;background:#D1D5DB;"></div>

  <div style="width:100%;max-width:340px;background:#F4F0FA;border:1px solid #D8CCEC;border-radius:10px;padding:14px 18px;text-align:center;box-shadow:0 1px 2px rgba(16,24,40,0.05);">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#7C5BB5;margin-bottom:4px;">Step 3</div>
    <div style="font-size:15px;font-weight:600;color:#5A28A3;">Dynamic route selection</div>
    <div style="font-size:13px;color:#6B5B87;margin-top:2px;">Highest success rate wins</div>
  </div>

  <div style="width:2px;height:26px;background:#D1D5DB;"></div>

  <div style="width:100%;max-width:340px;background:#ECFDF5;border:1px solid #A7F3D0;border-radius:10px;padding:14px 18px;text-align:center;box-shadow:0 1px 2px rgba(16,24,40,0.05);">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#059669;margin-bottom:4px;">Step 4</div>
    <div style="font-size:15px;font-weight:600;color:#065F46;">Execute transaction</div>
  </div>

</div>

*   **Real-Time Telemetry:** Aggregates health data across gateways, issuing banks, and payment modes in rolling sub-minute windows.
*   **Automated Anomaly Detection:** Automatically flags an acquiring route as degraded when performance drops below operational thresholds.
*   **Dynamic Path Selection:** Evaluates active health metrics for every API call and routes the transaction to the optimal acquiring terminal.
*   **Context-Aware Retries:** Tracks multi-attempt customer sessions. If a user retries a failed payment, the system automatically redirects the request over an alternate gateway behind the scenes.

## 4. Expected Impact & Value

*   **Performance Metric:** Merchants utilizing dynamic multi-gateway routing achieve a +2.0% to +5.0% improvement in overall Success Rate compared to static routing configurations during ecosystem downtime.

<!-- Claude, flagging for Saif, not confirmed: I could not find one independent benchmark agreeing on this specific 2 to 5% range. Cashfree's own published smart-routing case study cites about 2%, a third-party fintech benchmark says 1 to 2%, and Razorpay's marketing claims around 10% for a comparable feature. Nothing isolates the "during ecosystem downtime" scenario specifically the way this line implies. Left the number as-is since I don't have a more precise internal figure to replace it with, posted a comment on this line too. If your own routing-engine data backs a specific number, use that instead. -->
*   **Revenue Protection:** Recovers lost transactions automatically during partner bank and gateway outages.
*   **Zero Operational Overhead:** Eliminates the need for manual gateway flipping or active health monitoring.
*   **Unified Telemetry:** Access real-time downtime webhooks and status alerts directly from your merchant dashboard or API.
