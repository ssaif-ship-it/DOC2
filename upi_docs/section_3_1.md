To maintain the security of the payment ecosystem and mitigate fraud, the National Payments Corporation of India (NPCI) and participating banks enforce strict transaction and velocity limits on the UPI network.

As a merchant, it is crucial to understand both the baseline network limits and your specific Merchant Category Code (MCC) limits. Attempting to collect amounts above these thresholds—or using restricted payment flows—will result in immediate technical declines.

### 1. The 24-Hour New User Velocity Rule (Anti-Fraud)

One of the most common reasons for unexpected payment failures on high-value orders is the NPCI's 24-hour cooling-off period. To prevent account takeover fraud, the NPCI heavily restricts transaction capabilities when a user's UPI profile undergoes a major state change (e.g., first-time registration, device binding/new phone, or UPI PIN reset).

**The Restriction:** For the first **24 hours** following any of these triggers, the user's UPI transaction limit is strictly capped at **₹5,000**. Normal limits are automatically restored after the 24-hour window expires.

### 2. Standard & MCC-Specific Limits

By default, the standard retail limit for a P2M (Person-to-Merchant) transaction is **₹1 Lakh**. However, the NPCI recognizes that certain critical industries require higher ceilings, while high-risk categories face strict flow limitations (such as completely blocking "pull"/Collect requests).

The table below acts as your master reference for daily transaction limits and flow blocks enforced by the NPCI switch, based on your merchant category:


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UPI Transaction Limits & Category Dashboard</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-green: #10b981;
            --accent-blue: #38bdf8;
            --accent-amber: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
        }

        .upi-dashboard {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 30px 20px;
            border-radius: 12px;
            margin: 20px 0;
        }

        .upi-dashboard .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .upi-dashboard .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .upi-dashboard .stat-icon {
            width: 42px;
            height: 42px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            flex-shrink: 0;
        }

        .upi-dashboard .stat-icon.green { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
        .upi-dashboard .stat-icon.amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); }
        .upi-dashboard .stat-icon.blue { background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); }

        .upi-dashboard .stat-info h3 {
            margin: 0;
            font-size: 18px;
            font-weight: 700;
        }

        .upi-dashboard .stat-info p {
            margin: 2px 0 0 0;
            font-size: 12px;
            color: var(--text-muted);
        }

        .upi-dashboard .category-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .upi-dashboard .category-card.default-tier {
            border: 1px solid rgba(56, 189, 248, 0.4);
            background: linear-gradient(180deg, rgba(30, 41, 59, 1) 0%, rgba(15, 23, 42, 0.8) 100%);
        }

        .upi-dashboard .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 14px;
        }

        .upi-dashboard .card-title {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .upi-dashboard .card-title h2 {
            margin: 0;
            font-size: 16px;
            color: var(--text-main);
        }

        .upi-dashboard .badge-count {
            background: #334155;
            color: var(--text-muted);
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
        }

        .upi-dashboard .limit-badge {
            font-size: 14px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 16px;
        }

        .upi-dashboard .limit-500k {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .upi-dashboard .limit-200k {
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .upi-dashboard .limit-100k {
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .upi-dashboard .mcc-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .upi-dashboard .mcc-tag {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 12px;
            color: #cbd5e1;
        }

        .upi-dashboard .mcc-tag span {
            color: #64748b;
            font-weight: 600;
            margin-right: 4px;
        }

        .upi-dashboard .rule-note {
            margin-top: 10px;
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }
    </style>
</head>
<body>

<div class="upi-dashboard">
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon blue">₹</div>
            <div class="stat-info">
                <h3>₹100,000</h3>
                <p>Standard Baseline Cap</p>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon amber">₹</div>
            <div class="stat-info">
                <h3>₹200,000</h3>
                <p>Capped Specialty Tier</p>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon green">₹</div>
            <div class="stat-info">
                <h3>₹500,000</h3>
                <p>High-Value Exempt Tier</p>
            </div>
        </div>
    </div>

    <!-- Default Tier -->
    <div class="category-card default-tier">
        <div class="card-header">
            <div class="card-title">
                <h2>Standard Default Tier (Every Other Payment)</h2>
                <span class="badge-count" style="background: rgba(56,189,248,0.2); color: var(--accent-blue);">Standard Baseline</span>
            </div>
            <span class="limit-badge limit-100k">₹100,000 / day</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>P2P</span> Person-to-Person Transfers</div>
            <div class="mcc-tag"><span>RETAIL</span> Local Merchant & Grocery Stores</div>
            <div class="mcc-tag"><span>ECOM</span> E-Commerce & Online Spends</div>
            <div class="mcc-tag"><span>FOOD</span> Restaurants & Dining</div>
            <div class="mcc-tag"><span>UTIL</span> Utility Bills & Recharges</div>
            <div class="mcc-tag"><span>ALL</span> All Other Unspecified MCC Codes</div>
        </div>
        <div class="rule-note">
            ⚡ <strong>Note:</strong> Subject to a 20-transaction daily limit per rolling 24 hours. Individual bank caps or new account 24-hr restrictions (₹5,000) apply.
        </div>
    </div>

    <!-- Medical & Healthcare -->
    <div class="category-card">
        <div class="card-header">
            <div class="card-title">
                <h2>Medical & Healthcare</h2>
                <span class="badge-count">11 MCCs</span>
            </div>
            <span class="limit-badge limit-500k">₹500,000</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>8062</span> Hospitals</div>
            <div class="mcc-tag"><span>8011</span> Doctors & Physicians</div>
            <div class="mcc-tag"><span>8021</span> Dentists</div>
            <div class="mcc-tag"><span>8071</span> Medical & Dental Labs</div>
            <div class="mcc-tag"><span>8050</span> Nursing Care</div>
            <div class="mcc-tag"><span>8042</span> Optometrists</div>
            <div class="mcc-tag"><span>8031</span> Osteopaths</div>
            <div class="mcc-tag"><span>8041</span> Chiropractors</div>
            <div class="mcc-tag"><span>8049</span> Podiatrists</div>
            <div class="mcc-tag"><span>8099</span> Other Medical Services</div>
            <div class="mcc-tag"><span>0742</span> Veterinary Services</div>
        </div>
    </div>

    <!-- Education -->
    <div class="category-card">
        <div class="card-header">
            <div class="card-title">
                <h2>Education & Academic Institutions</h2>
                <span class="badge-count">6 MCCs</span>
            </div>
            <span class="limit-badge limit-500k">₹500,000</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>8211</span> Schools (Elementary & Secondary)</div>
            <div class="mcc-tag"><span>8220</span> Colleges & Universities</div>
            <div class="mcc-tag"><span>8249</span> Vocational & Trade Schools</div>
            <div class="mcc-tag"><span>8244</span> Business Schools</div>
            <div class="mcc-tag"><span>8241</span> Correspondence Schools</div>
            <div class="mcc-tag"><span>8299</span> Educational Services</div>
        </div>
    </div>

    <!-- Financial & Insurance -->
    <div class="category-card">
        <div class="card-header">
            <div class="card-title">
                <h2>Financial Services, Credit & Insurance</h2>
                <span class="badge-count">8 MCCs</span>
            </div>
            <span class="limit-badge limit-500k">₹500,000</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>5413</span> Credit Card Bill Payments</div>
            <div class="mcc-tag"><span>6300</span> Insurance Underwriting & Premiums</div>
            <div class="mcc-tag"><span>6529</span> LIC Payments</div>
            <div class="mcc-tag"><span>6211</span> Securities Brokers & Dealers</div>
            <div class="mcc-tag"><span>6012</span> Financial Institutions</div>
            <div class="mcc-tag"><span>5960</span> Direct Marketing Insurance</div>
            <div class="mcc-tag"><span>7322</span> Debt Collection Agencies</div>
            <div class="mcc-tag"><span>7410</span> Digital Banking Services</div>
        </div>
    </div>

    <!-- Government & Travel -->
    <div class="category-card">
        <div class="card-header">
            <div class="card-title">
                <h2>Government, Travel & Public Services</h2>
                <span class="badge-count">2 MCCs</span>
            </div>
            <span class="limit-badge limit-500k">₹500,000</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>9311</span> Tax Payments</div>
            <div class="mcc-tag"><span>4722</span> Travel Agencies & Tour Operators</div>
        </div>
    </div>

    <!-- Retail Luxury & Digital KYC -->
    <div class="category-card">
        <div class="card-header">
            <div class="card-title">
                <h2>Retail Luxury & Digital KYC</h2>
                <span class="badge-count">2 MCCs</span>
            </div>
            <span class="limit-badge limit-200k">₹200,000</span>
        </div>
        <div class="mcc-tags">
            <div class="mcc-tag"><span>5944</span> Jewellery, Watch & Silverware Shops</div>
            <div class="mcc-tag"><span>7409</span> Digital Account Opening</div>
        </div>
    </div>

</div>

</body>
</html>





> **Note:** While the NPCI sets the maximum ceilings above, individual **Remitter Banks** reserve the right to set *lower* internal limits based on their own risk policies (e.g., a specific bank might cap daily UPI spends at ₹50,000 regardless of your MCC).
