from pathlib import Path

from src.reporting.cleaning import (
    clean_payments,
    clean_sales,
)
from src.reporting.ingestion import load_data
from src.reporting.kpis import calculate_kpis
from src.reporting.reconciliation import (
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

kpis = calculate_kpis(
    sales,
    reconciled,
)

print("\nBUSINESS KPIs")
print("-" * 40)

for name, value in kpis.items():
    print(f"{name}: {value}")