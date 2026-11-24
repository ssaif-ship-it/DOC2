Besides a standard UPI payment from a bank account, your customers can also pay through UPI with UPI Lite, with a prepaid wallet, or with a RuPay credit card converted into EMI. This page explains what each one is and what you need to do, if anything.

| Payment type | What it is | What you need to do |
|---|---|---|
| UPI Lite | A small balance the customer keeps inside their UPI app for low value payments | Nothing. The customer turns it on in their own UPI app. |
| Prepaid wallets (PPI) | An eligible full KYC prepaid wallet the customer has linked to a UPI app | Nothing. These payments are accepted along with your other UPI payments. |
| EMI on UPI | A RuPay credit card payment on UPI that the customer converts into EMI | It is enabled per merchant account. Contact your account manager, then follow the setup guide below. |

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

EMI on UPI lets a customer who pays with a RuPay credit card through UPI convert the payment into EMI at the time of payment. It uses NPCI's Contextual Payments framework: your UPI intent link or QR carries a code that tells the customer's UPI app to show EMI options. The customer confirms with their UPI PIN, with no card number, CVV or bank redirect.

**Availability:** EMI on UPI is enabled per merchant account. Contact your Cashfree account manager to confirm whether it is available for you, which issuing banks and UPI apps are supported, and which EMI types apply.

**Where it works:** UPI intent links and QR codes, with RuPay credit cards. It does not work for UPI Collect requests. Cashfree adds the EMI code to the intent link or QR it generates for the order.

#### Types of EMI

You choose which of these to offer when you create an offer on your dashboard.

*   **Standard EMI:** the customer pays the amount plus interest.
*   **No cost EMI:** you give a discount equal to the interest, so the customer repays only the product price.
*   **Low cost EMI:** you bear part of the interest and the customer pays the rest.

#### How the customer picks a plan

| | Customer selects the plan | You pre select the plan |
|---|---|---|
| Where the customer chooses | Inside their UPI app, after scanning your QR | On your checkout, where they pick the tenure and the bank |
| What you show | The available EMI options, with a message to scan using the UPI app where their RuPay credit card is linked | The plans for the order amount |
| What the customer sees in the UPI app | All EMI plans available for their card | Only the plan they chose on your checkout, which they cannot change |
| If the customer does not use an EMI plan | The payment still goes through as a regular UPI payment | The payment is declined |

#### What it costs you

No cost EMI works through a discount. You give the customer a discount equal to the interest the bank charges, and the customer repays only the product price over the tenure. You are settled the product price minus that discount. The interest rate depends on the issuing bank.

Example, using an illustrative rate of 16% a year for 3 months:

| Item | Amount |
|---|---|
| Product price | ₹10,000 |
| Customer repays in total | ₹10,000, as 3 EMIs of about ₹3,333 |
| Discount you give (equal to the interest) | ₹261 |
| Amount settled to you | ₹9,739 |

The issuing bank can also charge the customer a processing fee, which depends on the bank.

### Setting up EMI on UPI

This guide is for business teams. Your developer handles the steps marked for them.

1. **Get it enabled.** Ask your account manager to enable EMI on UPI for your account. Cashfree switches it on in your account configuration.
2. **Create an offer.** On your Cashfree dashboard, create an EMI offer. Choose the eligible issuing banks, the EMI types you want to offer and any discount. Cashfree gives the offer an offer ID automatically. Your developer can also create offers through the API.
3. **Show EMI at checkout.** Your checkout shows the available EMI plans, with the bank, tenure, monthly instalment and total cost, and a message such as "Scan using the UPI app where your RuPay Credit Card is linked." Your developer fetches the available offers from Cashfree to show them.
4. **Create the order with the offer (developer).** Your developer passes the offer ID when creating the order. If the customer picks the tenure and bank on your checkout, the developer passes those too. Cashfree then returns the intent link or QR.
5. **The customer pays.** The customer scans the QR or opens the intent link in a UPI app where their RuPay credit card is linked, picks or confirms the plan, and enters their UPI PIN.
6. **Track the result.** After the payment succeeds, EMI booking is processed with the bank that issued the card. Payment success and EMI booking are separate outcomes, so the booking can be successful, pending or failed. Your payment success webhook carries the EMI details, including the booking status.

### Quick answers

*   **Can customers still pay without EMI?** Yes, when they select the plan inside their UPI app. They can pay from their bank account or choose a RuPay credit card with EMI.
*   **Who sees the EMI options?** Customers whose UPI app supports the EMI code and who have an eligible RuPay credit card.
*   **Does it work with UPI Collect?** No. It works only with UPI intent links and QR codes.
*   **Do I need to change my UPI integration?** Yes. When creating the order, your developer passes the offer ID, and the tenure and bank if the customer picks them on your checkout.
