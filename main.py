from src.scout.scout import Scout
from src.database.scripts.insert import Insert

if __name__ == '__main__':
    # Create Scout object
    scout = Scout()
    scout.navigate_to_google()
    parsed_names_list, parsed_links = scout.scroll_and_fetch_data()
    scout.export_to_csv(parsed_names_list, parsed_links)

    # Insert Scout's data into the database
    insert_object = Insert()
    insert_object.insert_scout()