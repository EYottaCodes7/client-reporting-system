import pandas as pd

from src.reporting.reconciliation import (
    find_unmatched_payments,
    reconcile_sales_and_payments,
)

def test_multiple_payments_are_aggregated():
    sales = pd.DataFrame(
        [
            {
                "order_id": 1002,
                "customer_id": "C002",
                "order_date": "2026-08-01",
                "amount": 125.50,
                "status": "completed",
            }
        ]
    )

    payments = pd.DataFrame(
        [
            {
                "payment_id": "P001",
                "order_id": 1002,
                "payment_date": "2026-08-02",
                "amount": 50.00,
                "payment_method": "bank",
            },
            {
                "payment_id": "P002",
                "order_id": 1002,
                "payment_date": "2026-08-02",
                "amount": 50.00,
                "payment_method": "telebirr",
            },
            {
                "payment_id": "P003",
                "order_id": 1002,
                "payment_date": "2026-08-03",
                "amount": 25.50,
                "payment_method": "bank",
            },
        ]
    )

    result = reconcile_sales_and_payments(
        sales,
        payments,
    )

    order = result.iloc[0]

    assert order["paid_amount"] == 125.50
    assert order["reconciliation_status"] == "MATCH"


def test_missing_payment_is_detected():
    sales = pd.DataFrame(
        [
            {
                "order_id": 1001,
                "customer_id": "C001",
                "order_date": "2026-08-01",
                "amount": 250.00,
                "status": "completed",
            }
        ]
    )

    payments = pd.DataFrame(
        columns=[
            "payment_id",
            "order_id",
            "payment_date",
            "amount",
            "payment_method",
        ]
    )

    result = reconcile_sales_and_payments(
        sales,
        payments,
    )

    assert result.iloc[0]["reconciliation_status"] == "MISSING_PAYMENT"


def test_partial_payment_is_detected():
    sales = pd.DataFrame(
        [
            {
                "order_id": 1002,
                "customer_id": "C002",
                "order_date": "2026-08-01",
                "amount": 125.50,
                "status": "completed",
            }
        ]
    )

    payments = pd.DataFrame(
        [
            {
                "payment_id": "P001",
                "order_id": 1002,
                "payment_date": "2026-08-02",
                "amount": 100.00,
                "payment_method": "telebirr",
            }
        ]
    )

    result = reconcile_sales_and_payments(
        sales,
        payments,
    )

    order = result.iloc[0]

    assert order["paid_amount"] == 100.00
    assert order["difference"] == 25.50
    assert order["reconciliation_status"] == "PARTIAL_PAYMENT"


def test_cancelled_order_with_payment_is_detected():
    sales = pd.DataFrame(
        [
            {
                "order_id": 1008,
                "customer_id": "C007",
                "order_date": "2026-08-04",
                "amount": 210.00,
                "status": "cancelled",
            }
        ]
    )

    payments = pd.DataFrame(
        [
            {
                "payment_id": "P008",
                "order_id": 1008,
                "payment_date": "2026-08-04",
                "amount": 210.00,
                "payment_method": "bank",
            }
        ]
    )

    result = reconcile_sales_and_payments(
        sales,
        payments,
    )

    assert (
        result.iloc[0]["reconciliation_status"]
        == "CANCELLED_WITH_PAYMENT"
    )


def test_unmatched_payment_is_detected():
    sales = pd.DataFrame(
        [
            {
                "order_id": 1001,
                "customer_id": "C001",
                "order_date": "2026-08-01",
                "amount": 250.00,
                "status": "completed",
            }
        ]
    )

    payments = pd.DataFrame(
        [
            {
                "payment_id": "P999",
                "order_id": 9999,
                "payment_date": "2026-08-06",
                "amount": 150.00,
                "payment_method": "bank",
            }
        ]
    )

    result = find_unmatched_payments(
        sales,
        payments,
    )

    assert len(result) == 1
    assert result.iloc[0]["order_id"] == 9999
    assert (
        result.iloc[0]["reconciliation_status"]
        == "UNMATCHED_PAYMENT"
    )