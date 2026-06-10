import pandas as pd
import sqlite3

conn = sqlite3.connect('ecommerce.db')

# Always read from bronze never from CSV
df = pd.read_sql("SELECT * FROM bronze_orders", conn)

print("=== BRONZE DATA ===")
print("Total Rows:", len(df))
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)
print("\nFirst 5 Rows:")
print(df.head())


# verify the values
print("\n=== DATA QUALITY CHECK ===")

# Nulls
print("Null Values:")
print(df.isnull().sum())

# Duplicates
print("\nDuplicate Rows:", df.duplicated().sum())

# Revenue stats
print("\nRevenue Stats:")
print(df['Total Revenue'].describe())

# Units stats
print("\nUnits Sold Stats:")
print(df['Units Sold'].describe())

# Negative values
print("\nNegative Revenue Rows:", len(df[df['Total Revenue'] < 0]))
print("Zero Units Rows:", len(df[df['Units Sold'] <= 0]))


# fix the data values
print("\n=== FILLING NULLS ===")

# Fill number columns with median
df['Total Revenue'] = df['Total Revenue'].fillna(
    df['Total Revenue'].median()
)
df['Unit Price'] = df['Unit Price'].fillna(
    df['Unit Price'].median()
)
df['Units Sold'] = df['Units Sold'].fillna(
    df['Units Sold'].median()
)

# Fill text columns with mode
df['Product Category'] = df['Product Category'].fillna(
    df['Product Category'].mode()[0]
)
df['Product Name'] = df['Product Name'].fillna(
    df['Product Name'].mode()[0]
)
df['Region'] = df['Region'].fillna(
    df['Region'].mode()[0]
)
df['Payment Method'] = df['Payment Method'].fillna(
    df['Payment Method'].mode()[0]
)

# Fill date with forward fill
df['Date'] = df['Date'].ffill()

print("Nulls after filling:")
print(df.isnull().sum())

print("\n=== HANDLING DUPLICATES ===")
before = len(df)

df = df.groupby('Transaction ID').agg({
    'Date'            : 'first',
    'Product Category': 'first',
    'Product Name'    : 'first',
    'Units Sold'      : 'sum',
    'Unit Price'      : 'mean',
    'Total Revenue'   : 'sum',
    'Region'          : 'first',
    'Payment Method'  : 'first'
}).reset_index()

after = len(df)
print("Duplicates aggregated:", before - after)
print("Rows remaining:", after)

# fix the dataypes 
print("\n=== FIXING DATA TYPES ===")

# Date — text to proper datetime
df['Date'] = pd.to_datetime(
    df['Date'], errors='coerce'
)

# Transaction ID — make sure its text
df['Transaction ID'] = df['Transaction ID'].astype(str)

# Total Revenue — make sure its decimal number
df['Total Revenue'] = pd.to_numeric(
    df['Total Revenue'], errors='coerce'
)

# Unit Price — make sure its decimal number
df['Unit Price'] = pd.to_numeric(
    df['Unit Price'], errors='coerce'
)

# Units Sold — make sure its whole number
df['Units Sold'] = pd.to_numeric(
    df['Units Sold'], errors='coerce'
).astype('Int64')

# Text columns — clean extra spaces
df['Product Category'] = df['Product Category'].str.strip()
df['Product Name'] = df['Product Name'].str.strip()
df['Region'] = df['Region'].str.strip()
df['Payment Method'] = df['Payment Method'].str.strip()

print("After fixing data types:")
print(df.dtypes)



# Remove the invalid dataypes
print("\n=== REMOVING INVALID DATA ===")
before = len(df)

# Remove negative revenue
df = df[df['Total Revenue'] > 0]

# Remove zero or negative units
df = df[df['Units Sold'] > 0]

# Remove negative unit price
df = df[df['Unit Price'] > 0]

# Remove invalid dates
df = df[df['Date'].notna()]

after = len(df)
print("Invalid rows removed:", before - after)
print("Clean rows remaining:", after)


# outlier managment
print("\n=== HANDLING OUTLIERS ===")
before = len(df)

# Calculate IQR for Total Revenue
Q1 = df['Total Revenue'].quantile(0.25)
Q3 = df['Total Revenue'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print("Revenue lower bound:", round(lower, 2))
print("Revenue upper bound:", round(upper, 2))

# Remove outliers
df = df[
    (df['Total Revenue'] >= lower) & 
    (df['Total Revenue'] <= upper)
]

after = len(df)
print("Outlier rows removed:", before - after)
print("Rows remaining:", after)


# Add cleaned timestamp
df['cleaned_at'] = pd.Timestamp.now()

# Save to silver
df.to_sql('silver_orders', conn,
          if_exists='replace',
          index=False)

print("\n✅ Silver layer loaded!")
print("Rows inserted:", len(df))



# Check first 5 rows
silver_check = pd.read_sql(
    "SELECT * FROM silver_orders LIMIT 5",
    conn
)

print("\n=== SILVER TABLE CHECK ===")
print(silver_check)

# Count total rows
count = pd.read_sql(
    "SELECT COUNT(*) as total FROM silver_orders",
    conn
)
print("\nTotal rows in Silver:", count['total'][0])

# Final data types check
silver_df = pd.read_sql(
    "SELECT * FROM silver_orders",
    conn
)
print("\nFinal Data Types:")
print(silver_df.dtypes)

conn.close()



