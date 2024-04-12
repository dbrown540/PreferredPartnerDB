from configparser import ConfigParser

def config(filename="src\database\scripts\config\database.ini", section="postgresql"):
    # Create parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        print(f'The parameters are... {params}')
        for param in params:
            print(f'param[0] = {param[0]}, and param[1] = {param[1]}')
            db[param[0]] = param[1]

    else:
        raise Exception(f'Section {section} is not found in the {filename} file.')
    print(f'This is the db dictionary... {db}')
    return db
