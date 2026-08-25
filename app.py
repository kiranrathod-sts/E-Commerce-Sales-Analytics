import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.dashboard-subtitle {
    font-size: 20px;
    color: #9aa4b2;
    margin-bottom: 25px;
}

.kpi-card {
    background: linear-gradient(135deg, #172033, #202c44);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #34445f;
    text-align: center;
    min-height: 130px;
}

.kpi-title {
    font-size: 16px;
    color: #aeb8c7;
}

.kpi-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 10px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    color: #788397;
    padding: 30px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD EXCEL DATA
# =========================================================

FILE_PATH = "data/Ecommerce_Sales_Data_Analytics-3.xlsx"

try:
    df = pd.read_excel(FILE_PATH)

except Exception as e:
    st.error("❌ Excel file could not be loaded.")
    st.code(str(e))
    st.stop()

# =========================================================
# DATA CLEANING
# =========================================================

df.columns = df.columns.str.strip()

required_columns = [
    "Order_ID",
    "Date",
    "Customer",
    "City",
    "Category",
    "Product",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Profit",
    "Sales_Channel"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error("❌ Some required columns are missing from Excel.")
    st.write("Missing columns:", missing_columns)
    st.stop()

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

numeric_columns = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(subset=["Date"])

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">🛒 E-Commerce Sales Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Sales & Business Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown("---")

# Category
category_options = sorted(
    df["Category"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "📦 Category",
    options=category_options,
    default=category_options
)

# Sales Channel
channel_options = sorted(
    df["Sales_Channel"].dropna().unique().tolist()
)

selected_channels = st.sidebar.multiselect(
    "🛒 Sales Channel",
    options=channel_options,
    default=channel_options
)

# City
city_options = sorted(
    df["City"].dropna().unique().tolist()
)

selected_cities = st.sidebar.multiselect(
    "🏙️ City",
    options=city_options,
    default=city_options
)

# Date Range
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# =========================================================
# APPLY FILTERS
# =========================================================

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

if len(selected_dates) == 2:

    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date)
        &
        (filtered_df["Date"] <= end_date)
    ]

# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data found for the selected filters."
    )

    st.stop()

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)

# =========================================================
# KPI CARDS
# =========================================================

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Sales</div>
            <div class="kpi-value">₹{total_sales:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Total Profit</div>
            <div class="kpi-value">₹{total_profit:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛍️ Total Quantity</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# SECONDARY KPIs
# =========================================================

st.write("")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric(
        "💵 Average Order Value",
        f"₹{average_order_value:,.2f}"
    )

with info2:
    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

with info3:
    st.metric(
        "👥 Customers",
        f"{filtered_df['Customer'].nunique():,}"
    )

st.divider()

# =========================================================
# SALES BY CATEGORY
# =========================================================

st.markdown(
    '<div class="section-title">📊 Sales Analysis</div>',
    unsafe_allow_html=True
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    st.subheader("📦 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

with chart_col2:

    st.subheader("🛒 Sales by Channel")

    channel_sales = (
        filtered_df
        .groupby("Sales_Channel")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(channel_sales)

# =========================================================
# SALES TREND
# =========================================================

st.subheader("📈 Sales Trend")

daily_sales = (
    filtered_df
    .groupby("Date")["Sales"]
    .sum()
    .sort_index()
)

st.line_chart(daily_sales)

# =========================================================
# PROFIT ANALYSIS
# =========================================================

profit_col1, profit_col2 = st.columns(2)

with profit_col1:

    st.subheader("💹 Profit by Category")

    category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)

with profit_col2:

    st.subheader("🏙️ Sales by City")

    city_sales = (
        filtered_df
        .groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(city_sales)

# =========================================================
# TOP PRODUCTS
# =========================================================

st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# =========================================================
# TOP CUSTOMERS
# =========================================================

st.subheader("👑 Top 10 Customers")

top_customers = (
    filtered_df
    .groupby("Customer")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_customers)

# =========================================================
# DATA TABLE
# =========================================================

st.divider()

st.subheader("📋 Filtered Sales Data")

st.write(
    f"Showing **{len(filtered_df):,} records**"
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_ecommerce_sales.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🛒 E-Commerce Sales Analytics |
        Sales & Business Intelligence Dashboard
        <br>
        Built with Python, Pandas & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)