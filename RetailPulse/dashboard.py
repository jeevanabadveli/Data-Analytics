import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="RetailPulse Dashboard", layout="wide")

# Load Data
sales = pd.read_excel("sales_data.xlsx")
customers = pd.read_excel("customers.xlsx")
inventory = pd.read_excel("inventory.xlsx")

# Title
st.title("📊 RetailPulse Dashboard")

# ---------------- KPI SECTION ----------------

total_revenue = sales["Revenue"].sum()
total_orders = len(sales)
total_customers = len(customers)
total_products = inventory["Product_ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    st.metric("🛒 Total Orders", total_orders)

with col3:
    st.metric("👥 Customers", total_customers)

with col4:
    st.metric("📦 Products", total_products)

st.divider()

# ---------------- SALES TREND ----------------

sales["Date"] = pd.to_datetime(sales["Date"])
sales["Month"] = sales["Date"].dt.strftime("%Y-%m")

monthly_sales = sales.groupby("Month")["Revenue"].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- PRODUCT PERFORMANCE ----------------

product_sales = sales.groupby("Product_ID")["Revenue"].sum().reset_index()

fig2 = px.bar(
    product_sales,
    x="Product_ID",
    y="Revenue",
    title="Revenue by Product"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- CUSTOMER ANALYTICS ----------------

col1, col2 = st.columns(2)

with col1:

    gender_counts = customers["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    fig3 = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        title="Customer Gender Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col2:

    location_counts = customers["Location"].value_counts().reset_index()
    location_counts.columns = ["Location", "Count"]

    fig4 = px.bar(
        location_counts,
        x="Location",
        y="Count",
        title="Customers by Location"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------------- CHURN ANALYSIS ----------------

st.subheader("Customer Churn Analysis")

churn_counts = customers["Churn"].value_counts().reset_index()
churn_counts.columns = ["Churn", "Count"]

fig5 = px.pie(
    churn_counts,
    names="Churn",
    values="Count",
    title="Churn Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- INVENTORY ANALYSIS ----------------

st.subheader("Inventory Analysis")

fig6 = px.bar(
    inventory,
    x="Product_ID",
    y="Stock_Level",
    color="Category",
    title="Current Stock Levels"
)

st.plotly_chart(fig6, use_container_width=True)

# ---------------- LOW STOCK ALERT ----------------

st.subheader("⚠ Low Stock Products")

low_stock = inventory[
    inventory["Stock_Level"] <= inventory["Reorder_Point"]
]

st.dataframe(low_stock)

# ---------------- RAW DATA ----------------

with st.expander("View Sales Data"):
    st.dataframe(sales)

with st.expander("View Customer Data"):
    st.dataframe(customers)

with st.expander("View Inventory Data"):
    st.dataframe(inventory)