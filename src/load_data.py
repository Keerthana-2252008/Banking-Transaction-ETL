
import pandas as pd
from database import engine
from sqlalchemy import text

print("Starting data loading...")

# Read cleaned CSV files
customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
accounts = pd.read_csv("data/cleaned/accounts_cleaned.csv")
transactions = pd.read_csv(
    "data/cleaned/transactions_cleaned.csv",
    parse_dates=["transaction_date"]
)

# Load data into PostgreSQL
# Clear existing project data to allow safe reruns
with engine.begin() as connection:

    connection.execute(text("""
        TRUNCATE TABLE transactions, accounts, customers
        CASCADE
    """))

    customers.to_sql(
        "customers",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    accounts.to_sql(
        "accounts",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

    transactions.to_sql(
        "transactions",
        con=connection,
        if_exists="append",
        index=False,
        method="multi"
    )

print("\nDATA LOADING SUCCESSFUL!")
print("Customers loaded:", len(customers))
print("Accounts loaded:", len(accounts))
print("Transactions loaded:", len(transactions))
