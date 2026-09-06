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
from src.reporting.reporting import generate_excel_report


DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

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

output_path = OUTPUT_DIR / "client_report.xlsx"

generate_excel_report(
    kpis,
    reconciled,
    output_path,
)

print(f"Report generated: {output_path}")