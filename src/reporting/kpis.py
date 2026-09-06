import pandas as pd


def calculate_kpis(
    sales: pd.DataFrame,
    reconciled: pd.DataFrame,
) -> dict:
    """Calculate business KPIs from sales and reconciliation data."""

    total_revenue = sales["amount"].sum()

    total_payments = reconciled["paid_amount"].sum()

    outstanding_amount = reconciled["difference"].clip(
        lower=0
    ).sum()

    total_orders = len(sales)

    matched_orders = (
        reconciled["reconciliation_status"] == "MATCH"
    ).sum()

    problem_orders = (
        reconciled["reconciliation_status"] != "MATCH"
    ).sum()

    payment_rate = (
        total_payments / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_revenue": total_revenue,
        "total_payments": total_payments,
        "outstanding_amount": outstanding_amount,
        "payment_rate": payment_rate,
        "total_orders": total_orders,
        "matched_orders": matched_orders,
        "problem_orders": problem_orders,
        "average_order_value": average_order_value,
    }