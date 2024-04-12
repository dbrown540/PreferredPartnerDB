from src.database.scripts.connect_to_db import connect
import csv

class Insert():
    def __init__(self):
        self.conn, self.crsr = connect()

    def insert_scout(self):
        # Insert data from the CSV file into the table
        with open('output.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                self.crsr.execute(
                    f"INSERT INTO users (users_name, profile_url) VALUES (%s, %s)",
                    (row[0], row[1])
                )

        # Commit the transaction
        self.conn.commit()
        print("data inserted")
        # Close the cursor and connection
        self.crsr.close()
