import pandas as pd
import sqlite3
import time

print("="*50)
print("🚀 STARTING FULL E-COMMERCE PIPELINE")
print("="*50)

start_time = time.time()
conn = sqlite3.connect('ecommerce.db')

# ============================================
# BRONZE LAYER
# ============================================
print("\n🥉 BRONZE LAYER STARTING...")

df = pd.read_csv('raw_data/Online Sales Data.csv')
df['ingested_at'] = pd.Timestamp.now()
df.to_sql('bronze_orders', conn, if_exists='replace', index=False)

print(f"✅ Bronze loaded: {len(df)} rows")

# ============================================
# SILVER LAYER
# ============================================
print("\n🥈 SILVER LAYER STARTING...")

df = pd.read_sql("SELECT * FROM bronze_orders", conn)

# Fill nulls
df['Total Revenue'] = df['Total Revenue'].fillna(df['Total Revenue'].median())
df['Unit Price'] = df['Unit Price'].fillna(df['Unit Price'].median())
df['Units Sold'] = df['Units Sold'].fillna(df['Units Sold'].median())
df['Product Category'] = df['Product Category'].fillna(df['Product Category'].mode()[0])
df['Product Name'] = df['Product Name'].fillna(df['Product Name'].mode()[0])
df['Region'] = df['Region'].fillna(df['Region'].mode()[0])
df['Payment Method'] = df['Payment Method'].fillna(df['Payment Method'].mode()[0])
df['Date'] = df['Date'].ffill()

# Aggregate duplicates
df = df.groupby('Transaction ID').agg({
    'Date': 'first', 'Product Category': 'first', 'Product Name': 'first',
    'Units Sold': 'sum', 'Unit Price': 'mean', 'Total Revenue': 'sum',
    'Region': 'first', 'Payment Method': 'first'
}).reset_index()

# Fix types
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Transaction ID'] = df['Transaction ID'].astype(str)
df['Total Revenue'] = pd.to_numeric(df['Total Revenue'], errors='coerce')
df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
df['Units Sold'] = pd.to_numeric(df['Units Sold'], errors='coerce').astype('Int64')
for col in ['Product Category','Product Name','Region','Payment Method']:
    df[col] = df[col].str.strip()

# Remove invalid
df = df[df['Total Revenue'] > 0]
df = df[df['Units Sold'] > 0]
df = df[df['Unit Price'] > 0]
df = df[df['Date'].notna()]

# Remove outliers
Q1 = df['Total Revenue'].quantile(0.25)
Q3 = df['Total Revenue'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['Total Revenue'] >= Q1 - 1.5*IQR) & (df['Total Revenue'] <= Q3 + 1.5*IQR)]

df['cleaned_at'] = pd.Timestamp.now()
df.to_sql('silver_orders', conn, if_exists='replace', index=False)

print(f"✅ Silver loaded: {len(df)} rows")

# ============================================
# GOLD LAYER
# ============================================
print("\n🥇 GOLD LAYER STARTING...")

df = pd.read_sql("SELECT * FROM silver_orders", conn)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')

gold = df.groupby([
    'Date','Year','Month','Month_Name','Product Name',
    'Product Category','Region','Payment Method'
]).agg(
    total_revenue=('Total Revenue','sum'),
    total_units=('Units Sold','sum'),
    order_count=('Transaction ID','count'),
    avg_unit_price=('Unit Price','mean'),
    min_price=('Unit Price','min'),
    max_price=('Unit Price','max')
).reset_index()

gold['revenue_per_unit'] = (gold['total_revenue']/gold['total_units']).round(2)
gold['avg_order_value'] = (gold['total_revenue']/gold['order_count']).round(2)
gold['revenue_contribution_%'] = (gold['total_revenue']/gold['total_revenue'].sum()*100).round(2)
gold['performance_tag'] = pd.cut(gold['total_revenue'], bins=[0,100,500,1000,float('inf')], labels=['Low','Medium','High','Top'])
gold['aggregated_at'] = pd.Timestamp.now()

gold.to_sql('gold_summary', conn, if_exists='replace', index=False)

print(f"✅ Gold loaded: {len(gold)} rows")

# ============================================
# SUMMARY
# ============================================
end_time = time.time()

print("\n" + "="*50)
print(f"Time taken  : {round(end_time-start_time, 2)} seconds")
print("="*50)
print("✅ PIPELINE COMPLETE!")
print("="*50)

conn.close()