
import sqlite3
import pandas as pd

conn = sqlite3.connect("traces.db")
query = "SELECT * FROM spans"

df = pd.read_sql_query(query, conn)
conn.close()
print(df)