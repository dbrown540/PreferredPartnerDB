import csv
import psycopg2

# Database connection parameters
dbname = "psycotest"
user = "postgres"
password = "postgres"
host = "localhost"  # or your database host address
port = "5432"  # or your database port

# CSV file path
csv_file = "output.csv"

# PostgreSQL table name
table_name = "users"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Create the table if it doesn't exist
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    users_name TEXT,
    profile_url TEXT
)
"""
cur.execute(create_table_query)

# Insert data from the CSV file into the table
with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cur.execute(
            f"INSERT INTO {table_name} (users_name, profile_url) VALUES (%s, %s)",
            (row[0], row[1])
        )

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()


list = ['https://www.linkedin.com/in/keri-rantin-pmp-4232b57', 'Benjamin Cohen', 'https://www.linkedin.com/in/renee-martinez-57906973', 'Lina Rashid', 'https://www.linkedin.com/in/markanewsom', 'ELIZABETH JONES', 'https://www.linkedin.com/in/kristimartin', 'Cms Room', 'https://www.linkedin.com/in/mrbobamos', 'Angela Katsakis, PMP']