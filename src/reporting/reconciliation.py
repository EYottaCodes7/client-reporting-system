import pandas as pd


def reconcile_sales_and_payments(
    sales: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Compare sales against aggregated payments and classify each order."""

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

    # One order can have multiple payment records.
    # Aggregate them so reconciliation remains one row per order.
    payments_data = (
        payments_data
        .groupby("order_id", as_index=False)
        .agg(
            paid_amount=("amount", "sum"),
        )
    )

    # Start with every sale.
    reconciled = sales_data.merge(
        payments_data,
        on="order_id",
        how="left",
    )

    # Track whether a payment record actually existed.
    reconciled["has_payment"] = (
        reconciled["paid_amount"].notna()
    )

    reconciled["paid_amount"] = (
        reconciled["paid_amount"].fillna(0)
    )

    reconciled["difference"] = (
        reconciled["sale_amount"]
        - reconciled["paid_amount"]
    )

    reconciled["reconciliation_status"] = "MATCH"

    # Cancelled orders that received payment.
    reconciled.loc[
        (
            (reconciled["status"] == "cancelled")
            & reconciled["has_payment"]
            & (reconciled["paid_amount"] > 0)
        ),
        "reconciliation_status",
    ] = "CANCELLED_WITH_PAYMENT"

    # Sales with no payment record.
    reconciled.loc[
        ~reconciled["has_payment"],
        "reconciliation_status",
    ] = "MISSING_PAYMENT"

    # Partially paid orders.
    reconciled.loc[
        (
            reconciled["has_payment"]
            & (reconciled["paid_amount"] > 0)
            & (reconciled["paid_amount"] < reconciled["sale_amount"])
            & (reconciled["status"] != "cancelled")
        ),
        "reconciliation_status",
    ] = "PARTIAL_PAYMENT"

    # Overpaid orders.
    reconciled.loc[
        (
            reconciled["has_payment"]
            & (reconciled["paid_amount"] > reconciled["sale_amount"])
            & (reconciled["status"] != "cancelled")
        ),
        "reconciliation_status",
    ] = "OVERPAYMENT"

    return reconciled


def find_unmatched_payments(
    sales: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Find payments that do not have a corresponding sale."""
    
    sales_orders = sales[
        ["order_id"]
    ].drop_duplicates()

    unmatched = payments.merge(
        sales_orders,
        on="order_id",
        how="left",
        indicator=True,
    )

    unmatched = unmatched[
        unmatched["_merge"] == "left_only"
    ].copy()

    unmatched = unmatched.drop(
        columns=["_merge"]
    )

    unmatched["reconciliation_status"] = (
        "UNMATCHED_PAYMENT"
    )

    return unmatched


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