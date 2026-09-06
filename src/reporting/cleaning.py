import pandas as pd


def clean_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names."""

    dataframe = dataframe.copy()

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return dataframe


def clean_text_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from text columns."""

    dataframe = dataframe.copy()

    text_columns = dataframe.select_dtypes(
        include=["object"]
    ).columns

    for column in text_columns:
        dataframe[column] = dataframe[column].str.strip()

    return dataframe


def normalize_dates(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert specified columns to datetime."""

    dataframe = dataframe.copy()

    for column in columns:
        if column in dataframe.columns:
            dataframe[column] = pd.to_datetime(
                dataframe[column],
                errors="coerce",
            )

    return dataframe


def normalize_numeric_columns(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert specified columns to numeric values."""

    dataframe = dataframe.copy()

    for column in columns:
        if column in dataframe.columns:
            dataframe[column] = pd.to_numeric(
                dataframe[column],
                errors="coerce",
            )

    return dataframe

def clean_sales(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the sales dataset."""

    dataframe = clean_column_names(dataframe)
    dataframe = clean_text_columns(dataframe)

    dataframe = normalize_dates(
        dataframe,
        ["order_date"],
    )

    dataframe = normalize_numeric_columns(
        dataframe,
        ["amount"],
    )

    return dataframe


def clean_payments(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the payments dataset."""

    dataframe = clean_column_names(dataframe)
    dataframe = clean_text_columns(dataframe)

    dataframe = normalize_dates(
        dataframe,
        ["payment_date"],
    )

    dataframe = normalize_numeric_columns(
        dataframe,
        ["amount"],
    )

    return dataframe


def clean_customers(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the customers dataset."""

    dataframe = clean_column_names(dataframe)
    dataframe = clean_text_columns(dataframe)

    return dataframe