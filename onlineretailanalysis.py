import sqlite3
import pandas as pd

# Load data file
df = pd.read_csv('OnlineRetailIIUCI/online_retail_II.csv')

# Data clean up
df.columns = df.columns.str.strip()

# Create/connect to SQLite database
connection = sqlite3.connect('online_retail.db')

# Load data file to SQLite
df.to_sql('invoices', connection, if_exists='replace', index=False)
connection.close()