import json
import pandas as pd
from pathlib import Path


input_dict = {
    'param1': 1.0,
    'param2': 2.0,
    'param3': 3.0,
}
print(input_dict)

input_dict_multi = {
    'param1': 1.0,
    'param2': 2.0,
    'param3': 3.0,
    'param4': None,
    'sub_system': {
        'subparam1': 1.1,
        'subparam2': 2.2,
        'subparam3': 3.3,
    },
    'sub_system2': None,
}
print(input_dict_multi)

# df = pd.DataFrame.from_dict(input_dict)
# print(df)

# Convert to CSV and save to a file
# index=False prevents pandas from writing the DataFrame index as a column in the CSV
# df.to_csv('develop_output.csv', index=False)


def parse_input_dict(input_dict):
    param1 = input_dict['param1']
    param2 = input_dict['param2']
    param3 = input_dict['param3']
    param4 = input_dict['param4']
    
    print(f"param1: {param1}")
    print(f"param2: {param2}")
    print(f"param3: {param3}")
    print(f"param4: {param4}")
    
    if 'sub_system' in input_dict:
        subsystem = input_dict['sub_system']
        print(subsystem)
    
    subsystem2 = input_dict['sub_system2']
    print(subsystem2)

    if 'sub_system3' in input_dict:
        pass
    else:
        print("sub_system3 not in input_dict")


def to_json(input_dict):
    """Returns json object from dictionary."""
    return json.dumps(input_dict)


def write_to_json(input_json, filename: str or Path):
    """Save json data to a file."""
    with open(filename, "w") as f:
        f.write(input_json)


parse_input_dict(input_dict_multi)

######################################
# convert dict object to json object:
######################################
input_json = to_json(input_dict_multi)
print(input_json)

######################################
# Write to json file:
######################################
write_to_json(
    input_json=input_json, 
    filename='test_to_json.json',
)

######################################
# Load json input file:
######################################

file_path = 'test_to_json.json'

try:
    # Open the JSON file in read mode ('r')
    with open(file_path, 'r') as f:
        # Load the JSON data from the file
        data = json.load(f)

    # Now 'data' contains the Python representation of your JSON
    print("JSON data loaded successfully:")
    print(data)

    # You can access elements like a dictionary if the JSON represents an object
    # For example, if data.json contains {"name": "Alice", "age": 30}
    # print(data["name"])

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{file_path}'. Check file format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


