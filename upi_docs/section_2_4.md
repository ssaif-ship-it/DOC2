Cashfree SoftPOS converts any standard Android smartphone into a digital payment terminal. It enables businesses to accept in-person payments, in-store or at the doorstep, without expensive hardware terminals.

---

## 1. Collection Models

### Storefront Collection

*   **What it is:** Fixed-location payments at physical retail or billing counters.
*   **How it works:** A static QR code standee or display is placed at the counter. Customers scan using any UPI app (Google Pay, PhonePe, Paytm, etc.) and enter the bill amount.
*   **Best for:** Retail stores, pharmacies, supermarkets, and service counters.

### Agent Collection (SoftPOS App)

*   **What it is:** On-the-go collections using field staff or delivery executives' Android smartphones.
*   **How it works:** Agents open the Cashfree SoftPOS mobile app, enter the order details, and display a QR code or send a payment link directly to the customer's phone.
*   **Best for:** Cash-on-delivery (COD) digitization, logistics, field collections, and doorstep services.

### Customer VPA (Specialized Model)

*   **What it is:** Assigning a dedicated, permanent UPI ID or static QR code to a specific recurring customer.
*   **Best for:** EMI repayments, school fees, and recurring utility payments requiring strict customer-level reconciliation.

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
*   **Customer VPA**

---

## Step 3: Set Up Your Collection Points

Cashfree must verify each collection point before you can start collecting payments. Follow the respective setup steps according to your selected collection point type:

*   Storefront setup
*   Agent setup
*   Customer VPA setup

> **Note:** Each collection point must reach **Active** status before you can start collecting payments.

---

## Step 4: Start Collecting Payments via Agents

Agents can begin accepting payments through the **softPOS application**, a mobile app for Android devices that supports QR codes, payment links, and more.

For instructions on setting up static and dynamic QR codes, payment links, and payment limits, see **agent collection point**.

All transactions, both cash and digital, are visible in a single dashboard. See **settlements and reports** to understand how and when funds are transferred to your bank account.
