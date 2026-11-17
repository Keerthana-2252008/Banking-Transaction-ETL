
import pandas as pd

# Extract customer data
customers = pd.read_csv("data/customers.csv")

# Extract account data
accounts = pd.read_csv("data/accounts.csv")

# Extract transaction data
transactions = pd.read_csv("data/transactions.csv")

print("DATA EXTRACTION SUCCESSFUL")

print("\nCUSTOMER DATA")
print(customers.head())

print("\nACCOUNT DATA")
print(accounts.head())

print("\nTRANSACTION DATA")
print(transactions.head())

print("\nDATASET SHAPES")
print("Customers:", customers.shape)
print("Accounts:", accounts.shape)
print("Transactions:", transactions.shape)
