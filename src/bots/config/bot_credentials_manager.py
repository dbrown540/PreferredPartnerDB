from src.database.scripts.connect_to_db import connect
import random
import string
import secrets
import csv

class BotCredentialsManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn, self.crsr = connect()

    def create_one_email_header(self, first: str, last: str):
        first = first.lower()
        last = last.lower()
        name_list = [first, last]
        joined_name = "_".join(name_list)
        trailing_digits = str(random.randint(10000, 99999))
        bot_email = joined_name + trailing_digits
        return bot_email

    def generate_one_strong_password(self, length):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def update_database(self, first, last, email_header, password):
        try:
            self.crsr.execute(
                        f"INSERT INTO bots (bot_first_name, bot_last_name, bot_email_header, bot_email_password) VALUES (%s, %s, %s, %s)",
                        (first, last, email_header, password)
                    )
            self.conn.commit()
            
            print(f"Added {first} {last} to database")

        except:
            print("Failed to update database")

    def execute(self):
        self.crsr = self.conn.cursor()
        with open("src/bots/config/names.txt", "r") as file:
            reader = csv.reader(file, delimiter=' ')
            # Iterate through every row in the .csv
            for row in reader:
                # Parse the first and last names
                first, last = row[0], row[1]
                # Execute sql query
                self.crsr.execute('SELECT * FROM bots WHERE bot_first_name = %s AND bot_last_name = %s', (first, last))
                # Fetch the result
                result = self.crsr.fetchone()
                print(result)
                if result is None:
                    # Run the function that creates emails and passwords
                    # Create an email
                    bot_email_header = self.create_one_email_header(first, last)
                    print(bot_email_header)
                    # Create a password
                    password = self.generate_one_strong_password(length=12)
                    print(password)
                    # Update database
                    self.update_database(first, last, bot_email_header, password)

                else:
                    # Do nothing because the emails already exist
                    print(f"{first} {last} is already in the database.")
