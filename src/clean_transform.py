
import pandas as pd
import os

# Create folder for cleaned datasets
os.makedirs("data/cleaned", exist_ok=True)

# Load datasets
customers = pd.read_csv("data/customers.csv")
accounts = pd.read_csv("data/accounts.csv")
transactions = pd.read_csv("data/transactions.csv")

print("STARTING DATA CLEANING...")

# =====================================
# 1. CLEAN CUSTOMER DATA
# =====================================

customers = customers.drop_duplicates(subset=["customer_id"])

customers["age"] = pd.to_numeric(
    customers["age"], errors="coerce"
)

customers.loc[
    ~customers["age"].between(18, 100), "age"
] = pd.NA

customers["age"] = customers["age"].fillna(
    customers["age"].median()
)

customers["city"] = customers["city"].fillna(
    customers["city"].mode()[0]
)

customers = customers.dropna(
    subset=["customer_id", "customer_name"]
)

# =====================================
# 2. CLEAN ACCOUNT DATA
# =====================================

accounts = accounts.drop_duplicates(subset=["account_id"])

accounts["balance"] = pd.to_numeric(
    accounts["balance"], errors="coerce"
)

accounts.loc[accounts["balance"] < 0, "balance"] = pd.NA

accounts["balance"] = accounts["balance"].fillna(
    accounts["balance"].median()
)

accounts = accounts.dropna(
    subset=["account_id", "customer_id"]
)

accounts = accounts[
    accounts["customer_id"].isin(customers["customer_id"])
]

# =====================================
# 3. CLEAN TRANSACTION DATA
# =====================================

transactions = transactions.drop_duplicates(
    subset=["transaction_id"]
)

transactions["amount"] = pd.to_numeric(
    transactions["amount"], errors="coerce"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"], errors="coerce"
)

# Remove invalid amounts and dates
transactions = transactions.dropna(
    subset=[
        "transaction_id",
        "account_id",
        "amount",
        "transaction_date"
    ]
)

transactions = transactions[transactions["amount"] > 0]

# Keep valid transaction types
valid_types = ["Deposit", "Withdrawal", "Transfer"]

transactions = transactions[
    transactions["transaction_type"].isin(valid_types)
]

# Keep transactions belonging to existing accounts
transactions = transactions[
    transactions["account_id"].isin(accounts["account_id"])
]

# =====================================
# 4. SAVE CLEANED DATASETS
# =====================================

customers.to_csv(
    "data/cleaned/customers_cleaned.csv", index=False
)

accounts.to_csv(
    "data/cleaned/accounts_cleaned.csv", index=False
)

transactions.to_csv(
    "data/cleaned/transactions_cleaned.csv", index=False
)

# =====================================
# 5. DISPLAY RESULTS
# =====================================

print("\nDATA CLEANING COMPLETED!")

print("Customers:", len(customers))
print("Accounts:", len(accounts))
print("Transactions:", len(transactions))

print("\nCleaned datasets saved successfully!")
