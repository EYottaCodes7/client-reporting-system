from pathlib import Path
import pandas as pd
from src.reporting.cleaning import (
    clean_payments,
    clean_sales,
)
from src.reporting.ingestion import load_data
from src.reporting.reconciliation import (
    create_reconciliation_report,
    reconcile_sales_and_payments,
)


DATA_DIR = Path("data/raw")

data = load_data(DATA_DIR)

sales = clean_sales(data["sales"])
payments = clean_payments(data["payments"])

reconciled = reconcile_sales_and_payments(
    sales,
    payments,
)

report = create_reconciliation_report(
    reconciled,
)

print("\nRECONCILIATION REPORT")
print("-" * 60)
print(report.to_string(index=False))

from src.reporting.reconciliation import (
    find_unmatched_payments,
)

# Test payment without a corresponding sale.
unmatched_payment = pd.DataFrame(
    [
        {
            "payment_id": "P999",
            "order_id": 9999,
            "payment_date": "2026-08-06",
            "amount": 150.00,
            "payment_method": "bank",
        }
    ]
)

payments_with_unmatched = pd.concat(
    [payments, unmatched_payment],
    ignore_index=True,
)

unmatched = find_unmatched_payments(
    sales,
    payments_with_unmatched,
)

print("\nUNMATCHED PAYMENT TEST")
print("-" * 40)
print(unmatched.to_string(index=False))