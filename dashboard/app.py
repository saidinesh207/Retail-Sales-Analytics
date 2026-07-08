
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    layout="wide"
)

st.title("🛒 Retail Sales Analytics Dashboard")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sales = pd.read_csv(BASE_DIR / "data" / "processed" / "final_sales_data.csv")

st.subheader("Dataset Preview")

st.dataframe(sales.head())
st.subheader("📊 Key Metrics")

total_orders = sales["order_id"].nunique()
total_revenue = sales["revenue"].sum()
total_customers = sales["customer_unique_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"R$ {total_revenue:,.2f}")
col3.metric("Total Customers", f"{total_customers:,}")

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"]
)

sales["purchase_month"] = sales["order_purchase_timestamp"].dt.to_period("M")

monthly_sales = sales.groupby("purchase_month")["revenue"].sum()

monthly_sales.index = monthly_sales.index.astype(str)

st.subheader("📈 Monthly Revenue Trend")

fig, ax = plt.subplots(figsize=(12,5))

monthly_sales.plot(
    ax=ax,
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue")
ax.set_title("Monthly Revenue")

plt.xticks(rotation=45)

st.pyplot(fig)


category_revenue = (
    sales.groupby("product_category_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("🏆 Top 10 Product Categories by Revenue")

fig, ax = plt.subplots(figsize=(12,5))

category_revenue.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Product Category")
ax.set_ylabel("Revenue")
ax.set_title("Top 10 Product Categories")

plt.xticks(rotation=45)

st.pyplot(fig)
state_revenue = (
    sales.groupby("customer_state")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.subheader("🌍 Revenue by State")

fig, ax = plt.subplots(figsize=(12,6))

state_revenue.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("State")
ax.set_ylabel("Revenue")
ax.set_title("Revenue by State")

plt.xticks(rotation=90)

st.pyplot(fig)



reviews = pd.read_csv(
    BASE_DIR / "data" / "raw" / "olist_order_reviews_dataset.csv"
)

sales = sales.merge(
    reviews[["order_id", "review_score"]],
    on="order_id",
    how="left"
)

average_rating = sales["review_score"].mean()

st.subheader("⭐ Average Customer Rating")

st.metric(
    label="Average Rating",
    value=f"{average_rating:.2f} / 5"
)

top_customers = (
    sales.groupby("customer_unique_id")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("👑 Top 10 Customers")

fig, ax = plt.subplots(figsize=(12,5))

top_customers.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Customer ID")
ax.set_ylabel("Number of Orders")
ax.set_title("Top 10 Customers")

plt.xticks(rotation=90)

st.pyplot(fig)

top_products = (
    sales.groupby("product_category_name")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("📦 Top 10 Selling Product Categories")

fig, ax = plt.subplots(figsize=(12,5))

top_products.plot(
    kind="bar",
    ax=ax,
    color="green"
)

ax.set_title("Top Selling Product Categories")
ax.set_xlabel("Category")
ax.set_ylabel("Number of Orders")

plt.xticks(rotation=45)

st.pyplot(fig)


st.sidebar.header("🔍 Filters")

sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"]
)

sales["Year"] = sales["order_purchase_timestamp"].dt.year

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + sorted(sales["Year"].unique().tolist())
)


selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(sales["customer_state"].dropna().unique().tolist())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(
        sales["product_category_name"]
        .dropna()
        .unique()
        .tolist()
    )
)

filtered_sales = sales.copy()

if selected_year != "All":
    filtered_sales = filtered_sales[
        filtered_sales["Year"] == selected_year
    ]

if selected_state != "All":
    filtered_sales = filtered_sales[
        filtered_sales["customer_state"] == selected_state
    ]

if selected_category != "All":
    filtered_sales = filtered_sales[
        filtered_sales["product_category_name"] == selected_category
    ]


st.markdown("---")

st.subheader("📥 Download Filtered Data")

csv = filtered_sales.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)
    
st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_sales.groupby("customer_unique_id")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_customers)

st.subheader("🛒 Top Selling Products")

top_products = (
    filtered_sales.groupby("product_category_name")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)


st.subheader("📦 Revenue by Order Status")

status = (
    filtered_sales.groupby("order_status")["revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(8,5))

status.plot(
    kind="bar",
    ax=ax,
    color="skyblue"
)

ax.set_title("Revenue by Order Status")
ax.set_xlabel("Order Status")
ax.set_ylabel("Revenue")
plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")

st.subheader("ℹ️ Dataset Information")

st.write(f"Rows : {filtered_sales.shape[0]:,}")
st.write(f"Columns : {filtered_sales.shape[1]}")



