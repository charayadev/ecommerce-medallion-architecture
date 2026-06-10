import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect('ecommerce.db')
# Read raw kaggle file
df = pd.read_csv('raw_data/Online Sales Data.csv')

# Data in the file
print("RAW DATA CHECK : ")
print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])
# columns names
print("Columns in the data\n",df.columns.tolist())
# first 5 rows
print("1 five rows of the data\n")
print(df.head())


print("Lets have look to the values")
print("Null Vlaues in the data\n")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nData types:")
print(df.dtypes)


# Add timestamp we have that data
df['ingested_at'] = pd.Timestamp.now()

# Load into bronze — no cleaning and if already there than replace data
df.to_sql('bronze_orders', conn, 
          if_exists='replace', 
          index=False)

print("\n✅ Bronze layer loaded!")
print("Rows inserted:", len(df))



# Read back from database
bronze_check = pd.read_sql(
    "SELECT * FROM bronze_orders LIMIT 5", 
    conn
)


print(bronze_check)

# Count total rows again in the data
count = pd.read_sql(
    "SELECT COUNT(*) as total FROM bronze_orders", 
    conn
)
print("\nTotal rows in Bronze:", count['total'][0])