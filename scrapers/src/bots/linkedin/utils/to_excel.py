import psycopg2
import pandas as pd
from openpyxl import Workbook

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "house2"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Function to fetch data from a table and return as a DataFrame
def fetch_table_to_df(table_name, order_by=None):
    if order_by:
        query = f"SELECT * FROM {table_name} ORDER BY {order_by};"
    else:
        query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    return df

# List of tables to export and their order by column (if applicable)
tables = [
    ("users", "user_id"), 
    ("education", "user_id"), 
    ("work_experience", "user_id"), 
    ("skills", "user_id"), 
    ("bots", None), 
    ("phone_numbers", None), 
    ("cookies", "bot_id"), 
    ("salaries", None)
]

# Create a Pandas Excel writer using openpyxl as the engine
with pd.ExcelWriter("database_export.xlsx", engine="openpyxl") as writer:
    for table, order_by in tables:
        df = fetch_table_to_df(table, order_by)
        df.to_excel(writer, sheet_name=table, index=False)

# Close the database connection
conn.close()

print("Database has been exported to database_export.xlsx")
