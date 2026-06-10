import pandas as pd
import sqlite3

conn = sqlite3.connect('ecommerce.db')

# Always read from silver
df = pd.read_sql("SELECT * FROM silver_orders", conn)

print("=== SILVER DATA ===")
print("Total Rows:", len(df))
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)
print("\nFirst 5 Rows:")
print(df.head())



print("\n=== FIXING DATE ===")

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Extract extra date parts for business use
df['Year']  = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day']   = df['Date'].dt.day
df['Month_Name'] = df['Date'].dt.strftime('%B')

print("Date fixed and extracted ✅")
print(df[['Date','Year','Month','Day','Month_Name']].head())


# gold summary begins

print("\n=== BUILDING GOLD SUMMARY ===")

gold = df.groupby([
    'Date',
    'Year',
    'Month',
    'Month_Name',
    'Product Name',
    'Product Category',
    'Region',
    'Payment Method'
]).agg(
    total_revenue  = ('Total Revenue', 'sum'),
    total_units    = ('Units Sold',    'sum'),
    order_count    = ('Transaction ID','count'),
    avg_unit_price = ('Unit Price',    'mean'),
    min_price      = ('Unit Price',    'min'),
    max_price      = ('Unit Price',    'max')
).reset_index()

print("Gold rows created:", len(gold))
print("\nFirst 5 rows:")
print(gold.head())


# Kpi Creation 
print("\n=== ADDING BUSINESS KPIs ===")

# Revenue per unit sold
gold['revenue_per_unit'] = (
    gold['total_revenue'] / gold['total_units']
).round(2)

# Average order value
gold['avg_order_value'] = (
    gold['total_revenue'] / gold['order_count']
).round(2)

# Revenue contribution percentage
gold['revenue_contribution_%'] = (
    gold['total_revenue'] / 
    gold['total_revenue'].sum() * 100
).round(2)

# Performance tag based on revenue
gold['performance_tag'] = pd.cut(
    gold['total_revenue'],
    bins=[0, 100, 500, 1000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Top']
)

print("KPI columns added ✅")
print(gold.columns.tolist())


# check once them
print("\n=== GOLD QUALITY CHECK ===")
print("Nulls:\n", gold.isnull().sum())
print("\nTotal Revenue Sum:", round(gold['total_revenue'].sum(), 2))
print("Total Units Sum:", gold['total_units'].sum())
print("Total Orders:", gold['order_count'].sum())
print("\nRevenue by Category:")
print(gold.groupby('Product Category')['total_revenue'].sum().sort_values(ascending=False))
print("\nRevenue by Region:")
print(gold.groupby('Region')['total_revenue'].sum().sort_values(ascending=False))


# save the data
# Add aggregated timestamp
gold['aggregated_at'] = pd.Timestamp.now()

# Save to gold
gold.to_sql('gold_summary', conn,
            if_exists='replace',
            index=False)

print("\n✅ Gold layer loaded!")
print("Rows inserted:", len(gold))

# verify the gold
gold_check = pd.read_sql(
    "SELECT * FROM gold_summary LIMIT 5",
    conn
)

print("\n=== GOLD TABLE CHECK ===")
print(gold_check)

count = pd.read_sql(
    "SELECT COUNT(*) as total FROM gold_summary",
    conn
)
print("\nTotal rows in Gold:", count['total'][0])

print("\nGold Columns:")
print(gold.columns.tolist())

print("\nFinal Data Types:")
print(gold.dtypes)

conn.close()