## 1. Overview & Error Architecture

When a UPI transaction or recurring debit fails, the failure signal originates at one of three layers before being reported back to your application:

```text
[ Customer / UPI App ] ---> [ NPCI Switch / Remitter Bank ] ---> [ Gateway / Switch ] ---> [ Merchant Backend ]
       (User Error)                 (Bank/Network Error)             (Normalized API)            (Handled Code)
```

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

The table below maps standard NPCI error codes, raw bank responses, root causes, and recommended user/checkout actions:

# error codes table

<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-left:4px solid #1E40AF;border-radius:8px;padding:14px 16px;margin:1.25rem 0;">
  <strong style="color:#1E40AF;">Note:</strong> https://ssaif-ship-it.github.io/Error_codes/
</div>



  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 2rem;
      background-color: #f8f9fa;
      color: #333;
    }
    .table-container {
      max-width: 1200px;
      margin: 0 auto;
      background: #ffffff;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    /* Style for column search inputs */
    thead input {
      width: 100%;
      padding: 6px;
      box-sizing: border-box;
      font-size: 13px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
  </style>

<div class="table-container">
  <h2>Data Directory</h2>
  <table id="csv-table" class="display" style="width:100%">
    <thead></thead>
    <tbody></tbody>
  </table>
</div>

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>

<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>

<script>
  const CSV_FILE_PATH = 'data.csv';

  // Load and parse CSV file
  Papa.parse(CSV_FILE_PATH, {
    download: true,
    skipEmptyLines: true,
    complete: function (results) {
      const data = results.data;

      if (!data || data.length === 0) {
        console.error("CSV file is empty.");
        return;
      }

      // First row contains header titles
      const headers = data[0];
      // Remaining rows contain table data
      const rows = data.slice(1);

      // Build header HTML (Row 1: Column Titles, Row 2: Search Inputs)
      let titleRow = '<tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr>';
      let searchRow = '<tr>' + headers.map(h => `<th><input type="text" placeholder="Filter ${h}..." /></th>`).join('') + '</tr>';

      $('#csv-table thead').html(titleRow + searchRow);

      // Initialize DataTable
      const table = $('#csv-table').DataTable({
        data: rows,
        pageLength: 20,               // Default to 20 rows per page
        lengthMenu: [10, 20, 50, 100],  // Pagination dropdown options
        orderCellsTop: true,          // Sorting applies to title row, not input row
        responsive: true
      });

      // Attach per-column filtering logic
      $('#csv-table thead tr:eq(1) th').each(function (index) {
        $('input', this).on('keyup change clear', function () {
          if (table.column(index).search() !== this.value) {
            table
              .column(index)
              .search(this.value)
              .draw();
          }
        });
      });
    },
    error: function (err) {
      console.error("Error reading CSV:", err);
    }
  });
</script>

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
