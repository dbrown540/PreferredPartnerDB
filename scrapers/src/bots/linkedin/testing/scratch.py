def convert_text_to_sql_query(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Clean up the lines and remove any extra whitespace or newlines
        urls = [line.strip() for line in lines if line.strip()]

        # Create multiple SQL INSERT statements
        sql_queries = [f"INSERT INTO users (profile_url) VALUES ('{url}');" for url in urls]

        return sql_queries

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
file_path = 'C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//houseurls.txt'  # Replace with your file path
sql_query = convert_text_to_sql_query(file_path)
if sql_query:
    for query in sql_query:
        print(query)
