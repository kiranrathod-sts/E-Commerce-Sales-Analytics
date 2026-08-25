import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, #172033, #111827);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        margin-bottom: 15px;
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 15px;
        font-weight: 600;
    }

    .kpi-value {
        color: white;
        font-size: 27px;
        font-weight: 700;
        margin-top: 7px;
    }

    .section-title {
        color: white;
        font-size: 23px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
FILE_PATH = "data/Ecommerce_Sales_Data_Analytics-3.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(FILE_PATH)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Discount",
        "Sales",
        "Profit"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


try:
    df = load_data()
except Exception as e:
    st.error("Excel file could not be loaded.")
    st.code(str(e))
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🛒 E-Commerce Sales Analytics")
st.subheader("Sales & Business Intelligence Dashboard")

st.caption(
    "Interactive dashboard for analysing e-commerce sales, profit, "
    "orders, products and sales channels."
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.title("🔎 Dashboard Filters")

# Category
categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)

# Sales Channel
channels = sorted(df["Sales_Channel"].dropna().unique())

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    channels,
    default=channels
)

# City
cities = sorted(df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities
)

# Date
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
filtered_df = df.copy()

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

if selected_channels:
    filtered_df = filtered_df[
        filtered_df["Sales_Channel"].isin(selected_channels)
    ]

if selected_cities:
    filtered_df = filtered_df[
        filtered_df["City"].isin(selected_cities)
    ]

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
total_customers = filtered_df["Customer"].nunique()

if total_sales != 0:
    profit_margin = (total_profit / total_sales) * 100
else:
    profit_margin = 0

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
cols = st.columns(4)

with cols[0]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Sales</div>
            <div class="kpi-value">₹{total_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with cols[1]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Total Profit</div>
            <div class="kpi-value">₹{total_profit:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with cols[2]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛒 Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with cols[3]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Total Quantity</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

cols2 = st.columns(3)

with cols2[0]:
    st.metric("💵 Average Order Value", f"₹{average_order_value:,.2f}")

with cols2[1]:
    st.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

with cols2[2]:
    st.metric("👥 Customers", f"{total_customers:,}")

st.divider()

# --------------------------------------------------
# SALES TREND
# --------------------------------------------------
st.markdown(
    '<div class="section-title">📈 Sales Trend</div>',
    unsafe_allow_html=True
)

daily_sales = (
    filtered_df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

if not daily_sales.empty:

    fig_trend = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title="Daily Sales"
    )

    fig_trend.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )

# --------------------------------------------------
# SALES ANALYSIS
# --------------------------------------------------
st.markdown(
    '<div class="section-title">📊 Sales Analysis</div>',
    unsafe_allow_html=True
)

chart1, chart2 = st.columns(2)

# Sales by Category
with chart1:

    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s"
    )

    fig_category.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# Sales by Channel
with chart2:

    channel_sales = (
        filtered_df.groupby("Sales_Channel", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_channel = px.bar(
        channel_sales,
        x="Sales_Channel",
        y="Sales",
        title="Sales by Channel",
        text_auto=".2s"
    )

    fig_channel.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )

# --------------------------------------------------
# PROFIT ANALYSIS
# --------------------------------------------------
profit1, profit2 = st.columns(2)

with profit1:

    category_profit = (
        filtered_df.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig_profit = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        title="Profit by Category",
        text_auto=".2s"
    )

    fig_profit.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

with profit2:

    channel_profit = (
        filtered_df.groupby("Sales_Channel", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig_channel_profit = px.bar(
        channel_profit,
        x="Sales_Channel",
        y="Profit",
        title="Profit by Sales Channel",
        text_auto=".2s"
    )

    fig_channel_profit.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(
        fig_channel_profit,
        use_container_width=True
    )

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------
st.markdown(
    '<div class="section-title">🏆 Top Products</div>',
    unsafe_allow_html=True
)

top_products = (
    filtered_df.groupby("Product", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
    .head(10)
)

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------
with st.expander("📋 View Filtered Sales Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption(
    f"Showing {len(filtered_df):,} records | "
    f"E-Commerce Sales Analytics Dashboard"
)