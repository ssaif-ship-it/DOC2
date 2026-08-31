Cashfree SoftPOS converts any standard Android smartphone into a digital payment terminal. It enables businesses to accept in-person payments, in-store or at the doorstep, without expensive hardware terminals.

---

## 1. Collection Models

Which of the three models below fits you depends on where your business actually happens: at a fixed counter, out in the field with your own staff, or with the same customer paying you again and again.

### Storefront Collection

*   **What it is:** Static QR codes for physical store or counter locations, with every payment credited directly to your account.
*   **How it works:** You generate a QR code per store or counter and display it there. Customers scan it with any UPI app and pay. If you run multiple locations, each one keeps its own QR for separate tracking, while every payment still settles into a single registered bank account.
*   **Best for:** Retail shops, restaurants, clinics and salons, and any multi-outlet business that wants one settlement account across many locations without needing a dedicated POS terminal.

<!-- Claude, confirmed for Saif: rewritten to match Cashfree's own public softPOS docs (cashfree.com/docs/payments/softpos/introduction#storefront), including the per-location QR with single settlement account detail that was missing before. -->

### Agent Collection (SoftPOS App)

*   **What it is:** On-the-go collections using field staff or delivery executives' Android smartphones.
*   **How it works:** Agents open the Cashfree SoftPOS mobile app, enter the order details, and display a QR code or send a payment link directly to the customer's phone.
*   **Best for:** Cash-on-delivery (COD) digitization, logistics, field collections, and doorstep services.

### Customer VPA (Specialized Model)

*   **What it is:** Assigning a dedicated, permanent UPI ID or static QR code to a specific recurring customer.
*   **How it works:** Cashfree issues a unique UPI ID or QR code tied to just that one customer. Every payment they make against it arrives already tagged with their identity, so lending and subscription businesses in particular can match repayments automatically instead of reconciling by hand.
*   **Best for:** EMI repayments, school fees, and recurring utility payments requiring strict customer-level reconciliation.

<!-- Claude, confirmed for Saif: verified this model against Cashfree's own public softPOS docs (cashfree.com/docs/payments/softpos/introduction), which describe it the same way, a unique UPI ID or QR per customer, with lending named as the leading use case. Added the How it works bullet on that basis. -->

---

## 2. QR Code Types

| Feature | Static QR | Dynamic QR |
| :-- | :-- | :-- |
| **Amount Handling** | Customer manually types the payment amount. | Amount is pre-set and locked by the merchant/agent. |
| **Reusability** | Permanent (one code printed for infinite scans). | Single-use (unique per transaction). |
| **Generation** | Generated via Merchant Dashboard. | Generated on-the-fly via SoftPOS App or Backend APIs. |
| **Order Context** | Basic transaction details. | Supports attached metadata (Invoice #, Phone #, Notes). |
| **Error Risk** | Risk of customer underpaying or overpaying. | Zero amount errors (locked bill value). |

---

## 3. Key Merchant Benefits

*   **Platform Requirements:** SoftPOS app is supported on Android 6.0 and above (iOS is not supported).
*   **Multiple Payment Options:** Beyond QR codes, agents can collect payments via SMS Links, Tap to Pay (NFC cards), and EMI on UPI.
*   **Cash Ledger Tracking:** Field agents can log cash payments inside the app to maintain a single settlement report for both cash and digital collections.
*   **Centralized Dashboard:** Real-time visibility into individual agent collections, store transactions, and automated settlements from a single Merchant Dashboard.

---

# Activation Guide

If you are just weighing whether offline payments fits your business, here is the shape of it: you request activation from the Merchant Dashboard, pick the collection point type that matches how you collect payments (see Collection Models above), Cashfree verifies it, and you start collecting. No hardware or lengthy integration is needed for Storefront or Customer VPA, and Agent just needs an app install.

## Step 1: Activate Offline Payments

Make sure you have an active Cashfree Payment Gateway account, then request Offline Payments activation from the Merchant Dashboard.

1.  **Navigate to Offline Payments** Log in to the **Merchant Dashboard**, then go to **Offline Payments**.

2.  **Request Activation** Click **Request Activation**. This sends an activation request to your Cashfree account manager.

3.  **Wait for Email Confirmation** You will receive an email confirmation once your account manager activates Offline Payments.


---

## Step 2: Select a Collection Point

To add a collection point, open **Offline Payments** in the Merchant Dashboard, then navigate to **Collection Point Management** and click **Add a Collection Point**.

Select the collection point type that matches your business needs:

*   **Storefront:** Use this model if you operate one or more physical store locations and want customers to scan a static QR code to pay at the counter, with funds credited directly to your account.
*   **Agent (softPOS):** Use this model if your staff or agents collect payments on your behalf at the point of service, such as at a customer's doorstep or table, with funds credited directly to your account.
*   **Customer VPA:** Use this model if you bill the same customer repeatedly, for EMI, school fees, or a recurring utility charge, and want every payment automatically tagged to that one customer for reconciliation.

---

## Step 3: Get It Verified and Start Collecting

Cashfree verifies each collection point before it can start accepting payments, and it must reach **Active** status first.

Once active, agents collect through the **softPOS application** (Android), using QR codes, payment links, or Tap to Pay, while Storefront and Customer VPA collection points work directly through their own QR code or UPI ID, with no app needed.

All transactions, both cash and digital, are visible in a single dashboard. See [5.1 Settlements](#doc-5-1) to understand how and when funds are transferred to your bank account.

---

**Setting this up from scratch?** This guide assumes you already have a Cashfree account. If you are starting from zero, including creating your account, completing KYC, and deciding how the rest of your payments are integrated, see the complete [3.2 Onboarding Guide](#doc-3-2). Step 6 there covers exactly where offline acceptance fits into that journey.
