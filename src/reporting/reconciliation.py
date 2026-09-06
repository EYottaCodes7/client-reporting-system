import pandas as pd


def reconcile_sales_and_payments(
    sales: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Compare sales against payments and classify each order."""

    sales_data = sales[
        ["order_id", "customer_id", "order_date", "amount", "status"]
    ].copy()

    payments_data = payments[
        ["order_id", "amount"]
    ].copy()

    sales_data = sales_data.rename(
        columns={
            "amount": "sale_amount",
        }
    )

    payments_data = payments_data.rename(
        columns={
            "amount": "paid_amount",
        }
    )

    reconciled = sales_data.merge(
        payments_data,
        on="order_id",
        how="left",
    )

    reconciled["paid_amount"] = (
        reconciled["paid_amount"].fillna(0)
    )

    reconciled["difference"] = (
        reconciled["sale_amount"]
        - reconciled["paid_amount"]
    )

    reconciled["reconciliation_status"] = "MATCH"

    reconciled.loc[
        reconciled["paid_amount"] == 0,
        "reconciliation_status",
    ] = "MISSING_PAYMENT"

    reconciled.loc[
        (
            (reconciled["paid_amount"] > 0)
            & (reconciled["paid_amount"] < reconciled["sale_amount"])
        ),
        "reconciliation_status",
    ] = "PARTIAL_PAYMENT"

    reconciled.loc[
        reconciled["paid_amount"] > reconciled["sale_amount"],
        "reconciliation_status",
    ] = "OVERPAYMENT"

    reconciled.loc[
        reconciled["status"] == "cancelled",
        "reconciliation_status",
    ] = "CANCELLED_WITH_PAYMENT"

    return reconciled

def create_reconciliation_report(
    reconciled: pd.DataFrame,
) -> pd.DataFrame:
    """Return the columns needed for the reconciliation report."""

    columns = [
        "order_id",
        "customer_id",
        "order_date",
        "sale_amount",
        "paid_amount",
        "difference",
        "reconciliation_status",
    ]

    return reconciled[columns].copy()