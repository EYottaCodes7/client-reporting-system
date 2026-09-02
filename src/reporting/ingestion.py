from pathlib import Path

import pandas as pd


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(path)


def load_excel(path: Path) -> pd.DataFrame:
    """Load an Excel file into a pandas DataFrame."""
    return pd.read_excel(path)

def load_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all required client datasets."""

    sales = load_csv(data_dir / "sales.csv")
    payments = load_csv(data_dir / "payments.csv")
    customers = load_excel(data_dir / "customers.xlsx")

    return {
        "sales": sales,
        "payments": payments,
        "customers": customers,
    }