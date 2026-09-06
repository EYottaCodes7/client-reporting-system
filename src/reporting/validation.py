import pandas as pd


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> list[str]:
    """Return required columns that are missing."""

    return [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]


def validate_unique_column(
    dataframe: pd.DataFrame,
    column: str,
) -> bool:
    """Return True when all values in the column are unique."""

    return dataframe[column].is_unique


def validate_no_missing_values(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> list[str]:
    """Return columns containing missing values."""

    return [
        column
        for column in columns
        if dataframe[column].isna().any()
    ]


def validate_non_negative_column(
    dataframe: pd.DataFrame,
    column: str,
) -> bool:
    """Return True when all values in the column are non-negative."""

    return (dataframe[column] >= 0).all()


def validate_allowed_values(
    dataframe: pd.DataFrame,
    column: str,
    allowed_values: set,
) -> set:
    """Return values that are not part of the allowed set."""

    actual_values = set(dataframe[column].dropna())

    return actual_values - allowed_values


def validate_dataframe(
    dataframe: pd.DataFrame,
    contract: dict,
) -> dict:
    """Validate a DataFrame against a data contract."""

    errors = []

    # 1. Required columns
    required_columns = contract.get("required_columns", [])

    missing_columns = validate_required_columns(
        dataframe,
        required_columns,
    )

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )

    # 2. Unique columns
    unique_columns = contract.get("unique_columns", [])

    for column in unique_columns:
        if column not in dataframe.columns:
            continue

        if not validate_unique_column(dataframe, column):
            errors.append(
                f"{column} contains duplicates."
            )

    # 3. Non-negative columns
    non_negative_columns = contract.get(
        "non_negative_columns",
        [],
    )

    for column in non_negative_columns:
        if column not in dataframe.columns:
            continue

        if not validate_non_negative_column(dataframe, column):
            errors.append(
                f"{column} contains negative values."
            )

    # 4. Allowed values
    allowed_values = contract.get(
        "allowed_values",
        {},
    )

    for column, allowed in allowed_values.items():
        if column not in dataframe.columns:
            continue

        invalid_values = validate_allowed_values(
            dataframe,
            column,
            allowed,
        )

        if invalid_values:
            errors.append(
                f"Invalid values in {column}: {invalid_values}"
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }