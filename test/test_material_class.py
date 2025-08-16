import json
import thread_fast

input_dict = {
    'type': 'Material',
    'name': 'test_input_dict',
    'E_mpa': 200000.0,
    'nu': 0.3,
    'rho_gcc': 8.0,
    'cte_mm_mm_C': 2.0e-6,
    'tc_w_mK': 12.0,
    'hc_J_gC': 0.5,
    'Sty_mpa': 600.0,
    'Stu_mpa': 800.0,
    'Ssy_mpa': 340.0,
    'Ssu_mpa': 520.0,
    'Scy_mpa': 900.0,
    'Scu_mpa': 1200.0,
}

# test from dict:
test_input_dict_mat = thread_fast.Material.from_dict(input_dict)
print(test_input_dict_mat)

# test standard constructor:
a286 = thread_fast.Material(
    name='a286',
    E_mpa=200.0e3,
    nu=0.3,
    rho_gcc=7.93,
    cte_mm_mm_C=16.5e-6,
    tc_w_mK=15.1,
    hc_J_gC=420.0/1000.0,
    Sty_mpa=586.0,
    Stu_mpa=896.0,
)
print(a286)

# test to_dict:
output_dict = a286.to_dict()
print(output_dict)

a286.write_to_json('test_material.json')

# test load json:
file_path = 'test_material.json'

try:
    # Open the JSON file in read mode ('r')
    with open(file_path, 'r') as f:
        # Load the JSON data from the file
        data = json.load(f)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{file_path}'. Check file format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


print(data)

test_input_dict_mat = thread_fast.Material.from_dict(data)
print(test_input_dict_mat)
