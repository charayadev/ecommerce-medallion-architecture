import plotly.express as px
from utils.theme import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_GREEN, style_chart

def create_category_chart(df):
    cat_rev = df.groupby("Product Category")["total_revenue"].sum().reset_index()
    fig = px.bar(cat_rev, x="Product Category", y="total_revenue", title="Revenue by Category",
                 color_discrete_sequence=[COLOR_PRIMARY])
    return style_chart(fig)

def create_region_chart(df):
    reg_rev = df.groupby("Region")["total_revenue"].sum().reset_index().sort_values(by="total_revenue")
    fig = px.bar(reg_rev, x="total_revenue", y="Region", orientation='h', title="Revenue by Region",
                 color_discrete_sequence=[COLOR_GREEN])
    return style_chart(fig)

def create_trend_chart(df):
    monthly_rev = df.groupby(["Year", "Month", "Month_Name"])["total_revenue"].sum().reset_index()
    monthly_rev = monthly_rev.sort_values(by=["Year", "Month"])
    monthly_rev["Period"] = monthly_rev["Month_Name"] + " " + monthly_rev["Year"].astype(str)
    fig = px.line(monthly_rev, x="Period", y="total_revenue", title="Monthly Revenue Trend",
                   markers=True, color_discrete_sequence=[COLOR_SECONDARY])
    return style_chart(fig)

def create_payment_chart(df):
    pay_rev = df.groupby("Payment Method")["total_revenue"].sum().reset_index()
    fig = px.pie(pay_rev, names="Payment Method", values="total_revenue", title="Revenue by Payment Method",
                  hole=0.4, color_discrete_sequence=[COLOR_PRIMARY, COLOR_GREEN, COLOR_SECONDARY, "#8B5CF6"])
    return style_chart(fig)

def create_top_products_chart(df):
    top_products = df.groupby("Product Name")["total_revenue"].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x="Product Name", y="total_revenue", title="Top 10 Products by Revenue",
                  color_discrete_sequence=[COLOR_PRIMARY])
    fig.update_xaxes(tickangle=45)
    return style_chart(fig)

def create_performance_chart(df):
    perf_dist = df.groupby("performance_tag")["order_count"].sum().reset_index()
    fig = px.bar(perf_dist, x="performance_tag", y="order_count", title="Order Distribution by Performance Tag",
                  color="performance_tag", 
                  color_discrete_map={"Top": COLOR_GREEN, "High": COLOR_PRIMARY, "Medium": "#8B5CF6", "Low": COLOR_SECONDARY})
    return style_chart(fig)