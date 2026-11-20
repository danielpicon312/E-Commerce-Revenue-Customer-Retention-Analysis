import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'online_retail_II.csv'
DB_PATH = BASE_DIR / 'online_retail.db'

# Load data file
print("Loading dataset...", flush=True)
df = pd.read_csv(CSV_PATH)

# Data clean up
print("Cleaning dataset...", flush=True)
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Typecasting Customer ID to Integer (Dropping ".0")
df['Customer ID'] = df['Customer ID'].replace([float('inf'), float('-inf')], pd.NA).astype('Int64')

# Create/connect to SQLite database
print("Creating SQLite database...", flush=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load raw data file to SQLite
df.to_sql('raw_invoices', conn, if_exists='replace', index=False)

# Creating Replacement Table, Typecasting Customer ID to Strings, Leading and Trailing Spaces in Description Column and Correcting Country labels
print("Applying SQL transformations...", flush=True)
cursor.execute("DROP TABLE IF EXISTS invoices")
cursor.execute("""
    CREATE TABLE invoices AS
        SELECT DISTINCT
        Invoice,
        InvoiceDate,
        StockCode,
        TRIM(Description) AS Description,
        Quantity,
        Price,
        CAST([Customer ID] AS TEXT) AS [Customer ID],
        CASE TRIM(Country)
            WHEN 'EIRE' THEN 'Ireland'
            WHEN 'RSA' THEN 'South Africa'
            WHEN 'Unspecified' THEN 'Unknown'
        ELSE TRIM(Country)
        END AS Country
        FROM raw_invoices;
""")

cursor.execute('DROP TABLE raw_invoices')
conn.commit()
cursor.execute("VACUUM")
conn.close()

print("Database successfully created.", flush=True)