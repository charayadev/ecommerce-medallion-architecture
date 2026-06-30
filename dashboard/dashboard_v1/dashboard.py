import streamlit as st

# Import our custom modules
from utils.database import load_data
from utils.filters import apply_filters
from utils.helpers import load_css, draw_kpi
import utils.charts as charts

# -----------------------------------------------------------------------------
# 1. Page Configuration & Theme
# -----------------------------------------------------------------------------
st.set_page_config(page_title="E-Commerce Gold Dashboard", page_icon="📊", layout="wide")
load_css("dashboard/dashboard_v1/assets/style.css")

# -----------------------------------------------------------------------------
# 2. Data Loading
# -----------------------------------------------------------------------------
# Adjust this path if your db is located elsewhere
DB_PATH = r"C:\Users\HP\OneDrive\Desktop\ecommerce_pipeline\ecommerce.db" 
df = load_data(DB_PATH)

if df.empty:
    st.error(f"⚠️ Database not found at {DB_PATH}. Please ensure your pipeline has populated it.")
    st.stop()

# -----------------------------------------------------------------------------
# 3. Sidebar Filters
# -----------------------------------------------------------------------------
filtered_df = apply_filters(df)

# -----------------------------------------------------------------------------
# 4. KPI Cards
# -----------------------------------------------------------------------------
st.title("📊 Executive Sales Dashboard")
st.markdown("---")

total_revenue = filtered_df["total_revenue"].sum()
total_orders = filtered_df["order_count"].sum()
total_units = filtered_df["total_units"].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
draw_kpi(col1, "Total Revenue", f"{total_revenue:,.2f}", "$")
draw_kpi(col2, "Total Orders", f"{total_orders:,}")
draw_kpi(col3, "Total Units", f"{total_units:,}")
draw_kpi(col4, "Avg Order Value", f"{avg_order_value:,.2f}", "$")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Charts
# -----------------------------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.plotly_chart(charts.create_category_chart(filtered_df), width="stretch")
with row1_col2:
    st.plotly_chart(charts.create_region_chart(filtered_df), width="stretch")


row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.plotly_chart(charts.create_trend_chart(filtered_df), width="stretch")
with row2_col2:
    st.plotly_chart(charts.create_payment_chart(filtered_df), width="stretch")


row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    st.plotly_chart(charts.create_top_products_chart(filtered_df), width="stretch")
with row3_col2:
    st.plotly_chart(charts.create_performance_chart(filtered_df), width="stretch")

# -----------------------------------------------------------------------------
# 6. Raw Data Table
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("Gold Layer Data Table")
st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True,
    height=300
)