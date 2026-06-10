import sqlite3

conn = sqlite3.connect('ecommerce.db')

# BRONZE — exact raw copy of your kaggle data
conn.execute("""
CREATE TABLE IF NOT EXISTS bronze_orders (
    transaction_id TEXT,
    date TEXT,
    product_category TEXT,
    product_name TEXT,
    units_sold INTEGER,
    unit_price REAL,
    total_revenue REAL,
    region TEXT,
    payment_method TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# SILVER — same but cleaned
conn.execute("""
CREATE TABLE IF NOT EXISTS silver_orders (
    transaction_id TEXT,
    date TEXT,
    product_category TEXT,
    product_name TEXT,
    units_sold INTEGER,
    unit_price REAL,
    total_revenue REAL,
    region TEXT,
    payment_method TEXT,
    cleaned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.execute("DROP TABLE IF EXISTS gold_daily_sales")
conn.execute("DROP TABLE IF EXISTS gold_product_performance")
conn.execute("DROP TABLE IF EXISTS gold_regional_analysis")
conn.execute("DROP TABLE IF EXISTS gold_payment_analysis")

# Create new single gold table
conn.execute("""
CREATE TABLE IF NOT EXISTS gold_summary (
    sale_date TEXT,
    product_name TEXT,
    product_category TEXT,
    region TEXT,
    payment_method TEXT,
    total_revenue REAL,
    total_units_sold INTEGER,
    order_count INTEGER
)
""")
conn.commit()
print("✅ All 3 tables created!")