
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import text
import sys
import os

# Import database connection
sys.path.append(os.path.abspath("src"))
from database import engine

# Page configuration
st.set_page_config(
    page_title="Banking Transaction Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Transaction ETL Dashboard")
st.markdown("### Banking Data Analytics and Reporting")

# Load data from PostgreSQL
@st.cache_data(ttl=60)
def load_data():
    customers = pd.read_sql(
        "SELECT * FROM customers", engine
    )
    accounts = pd.read_sql(
        "SELECT * FROM accounts", engine
    )
    transactions = pd.read_sql(
        "SELECT * FROM transactions", engine
    )
    return customers, accounts, transactions

try:
    customers, accounts, transactions = load_data()

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    # Sidebar filters
    st.sidebar.header("Dashboard Filters")

    transaction_types = st.sidebar.multiselect(
        "Transaction Type",
        options=transactions["transaction_type"].unique(),
        default=transactions["transaction_type"].unique()
    )

    filtered = transactions[
        transactions["transaction_type"].isin(
            transaction_types
        )
    ].copy()

    # KPI calculations
    total_customers = len(customers)
    total_accounts = len(accounts)
    total_transactions = len(filtered)
    total_amount = filtered["amount"].sum()

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Total Accounts", total_accounts)
    col3.metric("Total Transactions", total_transactions)
    col4.metric("Transaction Volume", f"₹{total_amount:,.2f}")

    st.divider()

    # Transaction type chart
    st.subheader("Transaction Type Analysis")

    type_summary = filtered.groupby(
        "transaction_type"
    )["amount"].sum()

    fig1, ax1 = plt.subplots()
    type_summary.plot(kind="bar", ax=ax1)

    ax1.set_xlabel("Transaction Type")
    ax1.set_ylabel("Amount (₹)")
    ax1.set_title("Transaction Amount by Type")

    st.pyplot(fig1)
    plt.close(fig1)

    # Monthly transaction chart
    st.subheader("Monthly Transaction Analysis")

    filtered["month"] = (
        filtered["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = filtered.groupby("month")["amount"].sum()

    fig2, ax2 = plt.subplots()
    monthly.plot(kind="line", marker="o", ax=ax2)

    ax2.set_xlabel("Month")
    ax2.set_ylabel("Amount (₹)")
    ax2.set_title("Monthly Transaction Volume")

    plt.xticks(rotation=45)

    st.pyplot(fig2)
    plt.close(fig2)

    # Transaction records
    st.subheader("Transaction Records")

    st.dataframe(
        filtered.sort_values(
            "transaction_date",
            ascending=False
        ),
        width="stretch"
    )

    st.success("Dashboard loaded successfully!")

except Exception as error:
    st.error(f"Dashboard error: {error}")
