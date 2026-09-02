import pandas as pd

customers = pd.DataFrame(
    [
        ["C001", "Abebe Kebede", "abebe@example.com", "Addis Ababa"],
        ["C002", "Marta Tesfaye", "marta@example.com", "Adama"],
        ["C003", "John Doe", "john@example.com", "Addis Ababa"],
        ["C004", "Sara Ahmed", "sara@example.com", "Dire Dawa"],
        ["C005", "Daniel Bekele", "daniel@example.com", "Bahir Dar"],
        ["C006", "Hana Tadesse", "hana@example.com", "Hawassa"],
        ["C007", "Michael Samuel", "michael@example.com", "Addis Ababa"],
        ["C008", "Liya Worku", "liya@example.com", "Mekelle"],
        ["C009", "Yonas Girma", "yonas@example.com", "Addis Ababa"],
    ],
    columns=["customer_id", "name", "email", "city"],
)

customers.to_excel("data/raw/customers.xlsx", index=False)

print("Customer data created successfully.")