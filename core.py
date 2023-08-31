import json

def get_key():
    # Open the file for reading
    with open('data/keys.json', 'r') as f:
        data = json.load(f)

    # Now `data` is a Python dictionary containing the data from the JSON file
    return data

