import pandas as pd
import sqlite3
from datetime import datetime

conn = sqlite3.connect('ecommerce.db')

bronze = pd.read_sql("SELECT * FROM bronze_orders", conn)
silver = pd.read_sql("SELECT * FROM silver_orders", conn)
gold = pd.read_sql("SELECT * FROM gold_summary", conn)

print("="*60)
print("📋 DATA QUALITY REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

# Bronze stats
print("\n🥉 BRONZE LAYER")
print(f"Total rows ingested    : {len(bronze)}")
print(f"Total columns          : {bronze.shape[1]}")
print(f"Nulls found            : {bronze.isnull().sum().sum()}")
print(f"Duplicates found       : {bronze.duplicated().sum()}")

# Silver stats
print("\n🥈 SILVER LAYER")
print(f"Total rows after clean : {len(silver)}")
rows_removed = len(bronze) - len(silver)
print(f"Rows removed/merged    : {rows_removed}")
print(f"Removal rate           : {round(rows_removed/len(bronze)*100, 2)}%")
print(f"Nulls remaining        : {silver.isnull().sum().sum()}")
print(f"Duplicates remaining   : {silver.duplicated().sum()}")

# Gold stats
print("\n🥇 GOLD LAYER")
print(f"Total aggregated rows  : {len(gold)}")
print(f"Total revenue          : ${gold['total_revenue'].sum():,.2f}")
print(f"Total orders           : {gold['order_count'].sum():,}")
print(f"Total units sold       : {gold['total_units'].sum():,}")

# Pass rate
pass_rate = round((len(silver)/len(bronze))*100, 2)
print("\n" + "="*60)
print(f"✅ OVERALL DATA QUALITY PASS RATE: {pass_rate}%")
print("="*60)

# Save report to file
with open('data_quality_report.txt', 'w') as f:
    f.write(f"DATA QUALITY REPORT - {datetime.now()}\n")
    f.write(f"Bronze rows: {len(bronze)}\n")
    f.write(f"Silver rows: {len(silver)}\n")
    f.write(f"Gold rows: {len(gold)}\n")
    f.write(f"Pass rate: {pass_rate}%\n")

print("\n✅ Report saved to data_quality_report.txt")
conn.close()