SALES_CONTRACT = {
    "required_columns": [
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "status",
    ],
    "unique_columns": [
        "order_id",
    ],
    "non_negative_columns": [
        "amount",
    ],
    "allowed_values": {
        "status": {
            "completed",
            "cancelled",
        }
    },
}


PAYMENTS_CONTRACT = {
    "required_columns": [
        "payment_id",
        "order_id",
        "payment_date",
        "amount",
        "payment_method",
    ],
    "unique_columns": [
        "payment_id",
    ],
    "non_negative_columns": [
        "amount",
    ],
}


CUSTOMERS_CONTRACT = {
    "required_columns": [
        "customer_id",
        "name",
        "email",
        "city",
    ],
    "unique_columns": [
        "customer_id",
    ],
}