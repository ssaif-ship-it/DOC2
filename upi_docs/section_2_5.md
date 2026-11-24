Besides a standard UPI payment from a bank account, your customers can also pay through UPI with UPI Lite, with a prepaid wallet, or with a RuPay credit card converted into EMI. This page explains what each one is and what you need to do, if anything.

| Payment type | What it is | What you need to do |
|---|---|---|
| UPI Lite | A small balance the customer keeps inside their UPI app for low value payments | Nothing. The customer turns it on in their own UPI app. |
| Prepaid wallets (PPI) | An eligible full KYC prepaid wallet the customer has linked to a UPI app | Nothing. These payments are accepted along with your other UPI payments. |
| EMI on UPI | A RuPay credit card payment on UPI that the customer converts into EMI | Contact your account manager to check whether it is available for your account. |

### UPI Lite

UPI Lite is an on-device wallet inside the customer's UPI app, introduced by NPCI for small value payments. The customer switches it on in their own app and tops it up from their bank account, and small payments are then paid from that balance.

Each UPI Lite payment can be up to ₹1,000, and the balance can be up to ₹5,000 at any time. NPCI raised these from ₹500 and ₹2,000 in 2025, following an RBI change of 4 December 2024.

What this means for you:

*   **Nothing to enable.** UPI Lite is a customer side feature, and you do not need to integrate anything for it.
*   **Refunds.** NPCI's UPI Lite rules credit refunds to the customer's bank account.
*   **Disputes.** The customer's UPI app must let them raise a dispute for a UPI Lite payment.

### Prepaid wallets (PPI)

Eligible full KYC prepaid wallets (PPIs) can be linked to a UPI app, so the customer pays you from the wallet balance instead of a bank account. On 27 December 2024, RBI announced that full KYC wallets can also be linked to third party UPI apps, not only to the wallet issuer's own app.

What this means for you:

*   **Accepted by default.** Wallet payments are accepted along with your other UPI payments. You do not need to enable anything, and you create the order the same way.
*   **Identified after processing.** Cashfree identifies wallet funded UPI payments from gateway payment notifications or reconciliation, not from the order creation request.
*   **Pricing.** Cashfree records wallet payments as a separate payment mode, so your rate for them can differ from bank account UPI payments.
*   **Switching off.** If you do not want to accept wallet payments, or RuPay credit card payments, on UPI, contact your account manager to have them switched off.

### EMI on UPI

EMI on UPI lets a customer who pays with a RuPay credit card through UPI convert the payment into EMI at the time of payment. It uses NPCI's Contextual Payments framework, in which your UPI intent link or QR carries a code that tells the customer's UPI app to show EMI options.

How it works for the customer:

1. The customer scans your QR or opens your UPI intent link in a UPI app where their RuPay credit card is linked.
2. The UPI app shows the EMI plans available for that card. NPCI defines two modes. In one, the customer picks the plan inside the UPI app. In the other, you show the plans on your checkout, the customer picks the tenure and bank there, and the QR is fixed to that plan.
3. The customer confirms with their UPI PIN. No card number, CVV or bank redirect is involved.
4. After the payment succeeds, EMI booking is processed with the bank that issued the card. Payment success and EMI booking are separate outcomes, so the booking can be successful, pending or failed.

NPCI defines three types of EMI:

*   **Standard EMI:** the customer pays the amount plus interest.
*   **No cost EMI:** you bear the interest instead of the customer.
*   **Low cost EMI:** you bear part of the interest, and the customer pays the rest.

**Where it works:** UPI intent links and QR codes, with RuPay credit cards. It does not work for UPI Collect requests.

**Availability:** Contact your Cashfree account manager to confirm whether EMI on UPI is available for your account, which issuing banks and UPI apps are supported, and which EMI types and setup apply. Eligibility also depends on the customer's card and its issuing bank.
