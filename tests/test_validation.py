from pathlib import Path

from src.reporting.contracts import (
    SALES_CONTRACT,
    PAYMENTS_CONTRACT,
    CUSTOMERS_CONTRACT,
)
from src.reporting.ingestion import load_data
from src.reporting.validation import validate_dataframe
from src.reporting.cleaning import (
    clean_sales,
    clean_payments,
    clean_customers,
)


DATA_DIR = Path("data/raw")

data = load_data(DATA_DIR)


cleaned_data = {
    "sales": clean_sales(data["sales"]),
    "payments": clean_payments(data["payments"]),
    "customers": clean_customers(data["customers"]),
}


datasets = {
    "sales": (cleaned_data["sales"], SALES_CONTRACT),
    "payments": (cleaned_data["payments"], PAYMENTS_CONTRACT),
    "customers": (cleaned_data["customers"], CUSTOMERS_CONTRACT),
}


for name, (dataframe, contract) in datasets.items():
    print(f"\n{name.upper()} AFTER CLEANING")
    print("-" * 40)

    print(dataframe)
    print()

    result = validate_dataframe(
        dataframe,
        contract,
    )

    print("Validation:")
    print(result)