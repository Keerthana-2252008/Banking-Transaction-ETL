
import pandas as pd
import numpy as np
import os

# Create data folder
os.makedirs("data", exist_ok=True)

# 1. CUSTOMERS DATA
customers = pd.DataFrame({
    "customer_id": range(1, 101),
    "customer_name": [
        f"Customer_{i}" for i in range(1, 101)
    ],
    "city": np.random.choice(
        ["Chennai", "Bangalore", "Hyderabad", "Mumbai"],
        100
    ),
    "age": np.random.randint(18, 70, 100)
})

customers.to_csv("data/customers.csv", index=False)

# 2. ACCOUNTS DATA
accounts = pd.DataFrame({
    "account_id": range(1001, 1101),
    "customer_id": range(1, 101),
    "account_type": np.random.choice(
        ["Savings", "Current"], 100
    ),
    "balance": np.random.randint(1000, 100000, 100)
})

accounts.to_csv("data/accounts.csv", index=False)

# 3. TRANSACTIONS DATA
transactions = pd.DataFrame({
    "transaction_id": range(5001, 6001),
    "account_id": np.random.choice(
        range(1001, 1101), 1000
    ),
    "transaction_type": np.random.choice(
        ["Deposit", "Withdrawal", "Transfer"], 1000
    ),
    "amount": np.random.randint(100, 20000, 1000),
    "transaction_date": pd.date_range(
        start="2026-01-01",
        periods=1000,
        freq="h"
    )
})

transactions.to_csv("data/transactions.csv", index=False)

print("All three datasets created successfully!")
print("Customers:", len(customers))
print("Accounts:", len(accounts))
print("Transactions:", len(transactions))
