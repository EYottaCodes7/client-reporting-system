from pathlib import Path

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