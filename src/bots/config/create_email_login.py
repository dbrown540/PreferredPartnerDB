from src.database.scripts.connect_to_db import connect
import random
import string
import secrets
import csv

class BotCredentialsManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn, self.crsr = connect()

    def create_names_lists(self):
        """Reads a file and creates lists of first names and last names.
        
            Returns:
                tuple: A tuple containing two lists - first names list and last names list.
        """
        first_names_list = []
        last_names_list = []
        with open(self.filepath, "r") as f:
            for name in f:
                first_name = name.split()[0]
                last_name = name.split()[1]
                first_names_list.append(first_name)
                last_names_list.append(last_name)

        return first_names_list, last_names_list

    def create_email(self):
        """Generates a fake email address for the bots

        Returns:
            list: list of emails for the bots
        """
        email_list = []
        with open(self.filepath, "r") as f:
            for name in f:
                separated_name = name.lower().split()
                joined_name = "_".join(separated_name)
                trailing_digits = str(random.randint(10000, 99999))
                email = joined_name + trailing_digits
                email_list.append(email)
        return email_list

    def generate_strong_password(self, length=12):
        """Generate a strong password.
        
        Args:
            length (int): The length of the password to be generated. Default is 12.
        
        Returns:
            list: A list of strong passwords generated based on the specified length.
        """
        password_list = []
        with open(self.filepath, "r") as f:
            lines = len(f.readlines())
        for _ in range(lines):
            alphabet = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(secrets.choice(alphabet) for _ in range(length))
            password_list.append(password)
        return password_list
    
    def export_to_csv(self, first_names_list, last_names_list, email_list, password_list):
        """Export email and password lists to a CSV file.
        
            Args:
                email_list (list): List of email addresses.
                password_list (list): List of passwords corresponding to the email addresses.
        
            Returns:
                list: A zipped list of email and password pairs.
        
            Example:
                export_to_csv(['example1@gmail.com', 'example2@yahoo.com'], ['password1', 'password2'])
        """
        zipped_list = list(zip(first_names_list, last_names_list, email_list, password_list))
        with open('csv/email_credentials.csv', 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(['bot_first_name', 'bot_last_name', 'bot_email', 'bot_email_password'])
            write.writerows(zipped_list)

        return zipped_list

    def check_if_credentials_exist_in_db(self):
        """Check if credentials exist in the database.
        
            This function connects to the database, executes a query to count the number of credentials in the 'bots' table,
            prints the count, commits the transaction, and then closes the cursor and connection.
        
            Args:
                self: The object instance.
        
            Returns:
                None
        """

        self.crsr.execute("SELECT COUNT(*) FROM bots")
        count = self.crsr.fetchone()[0]
        print("Count of credentials: ", count)
        # Commit the transaction
        self.conn.commit()
        

        if count == 0:
            return False
        
        return True

    def insert_bot_email_credentials(self):
        # Insert data from the CSV file into the table
        with open('csv/email_credentials.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                self.crsr.execute(
                    f"INSERT INTO bots (bot_first_name, bot_last_name, bot_email, bot_email_password) VALUES (%s, %s, %s, %s)",
                    (row[0], row[1], row[2], row[3])
                )

        # Commit the transaction
        self.conn.commit()
        print("data inserted")
        # Close the cursor and connection
        self.crsr.close()