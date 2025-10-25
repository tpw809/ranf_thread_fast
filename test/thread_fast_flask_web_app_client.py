import requests


def test_material_api():
    print("\nStarting client request to thread_fast web app Material api...\n")
    # Define the URL of the web API
    # api_url = "https://example.com/api/app_entry_point"
    api_url = "http://localhost:5000/material"

    # Create a dictionary with the input data:
    data = {
        "type": "Material",
        "name": "a286",
        "E": 200000.0,
        "nu": 0.3,
        "cte": 1.65e-05,
        # "rho_gcc": 7.93,
        # "tc_w_mK": 15.1,
        # "hc_J_gC": 0.42,
        "Sty": 586.0,
        "Stu": 896.0,
        # "Ssy": 338.32725774512073,
        # "Ssu": 517.3058411939047,
        "Ssy": None,
        "Ssu": None,
        # "Scy": 879.0,
        # "Scu": 1344.0,
    }

    try:
        # Send a POST request to the API
        response = requests.post(api_url, json=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            print(result)
            print("...finished client request, returning result.")
            return result
        else:
            print(f"Error: API returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def test_fastener_api():
    print("\nStarting client request to thread_fast web app Fastener api...\n")
    # Define the URL of the web API
    # api_url = "https://example.com/api/app_entry_point"
    api_url = "http://localhost:5000/fastener"

    # Create a dictionary with the input data:
    data = {
        'type': 'Fastener', 
        'name': 'fastener_test_input_dict', 
        'material': {
            'type': 'Material', 
            'name': 'test_input_dict', 
            'E': 200000.0, 
            'nu': 0.3, 
            'cte': 2e-06, 
            'Sty': 600.0, 
            'Stu': 800.0, 
            'Scy': 900.0, 
            'Scu': 1200.0, 
            'Ssy': 346.4101615137755, 
            'Ssu': 461.88021535170066,
        }, 
        'thread': {
            'type': 'Metric_Thread', 
            'name': 'test_input_dict', 
            'basic_major_diameter': 6.0, 
            'pitch': 1.0, 
            'beta_deg': 30.0, 
            'external': True, 
            'internal': False, 
            'profile': 'MJ', 
            'tolerance_grade': 6, 
            'allowance_class': 'h', 
            'beta_rad': 0.5235987755982988, 
            # 'H': 0.8660254037844386, 
            # 'LE_min': 3.2053707416757726, 
            # 'LE_max': 9.587492843405213, 
            'basic_pitch_diameter': 5.350480947161671, 
            # 'basic_minor_diameter': 5.0257214207425065, 
            'r_m': 2.6752404735808355, 
            'psi_rad': 0.05942178951229949, 
            # 'es': 0.0, 
            # 'd3': 4.773130677972045, 
            # 'Td': 0.17685, 
            # 'Td2': 0.10766080789661839, 
            # 'd_max': 6.0, 
            # 'd_min': 5.82315, 
            # 'd2_max': 5.350481, 
            # 'd2_min': 5.242820192103382, 
            # 'd3_max': 4.773130677972045, 
            # 'd3_min': 4.677020192103382, 
            # 'A_t': 19.83732016056229, 
            # 'A_mean': 22.48410087820095,
        }, 
        'Do_head': 8.5, 
        'Do_shank': 5.0, 
        'L_shank': 10.0, 
        'L_thread': 10.0,
    }

    try:
        # Send a POST request to the API
        response = requests.post(api_url, json=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            print(result)
            print("...finished client request, returning result.")
            return result
        else:
            print(f"Error: API returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


def test_thread_api():
    print("\nStarting client request to thread_fast.thread web app...\n")
    # Define the URL of the web API
    # api_url = "https://example.com/api/rectangle_area"
    api_url = "http://localhost:5000/thread"

    # Create a dictionary with the input data (side lengths)
    data = {
        'type': 'Metric_Thread', 
        'name': 'test_input_dict', 
        'basic_major_diameter': 6.0, 
        'pitch': 1.0, 
        'beta_deg': 30.0, 
        'external': True, 
        'internal': False, 
        'profile': 'MJ', 
        'tolerance_grade': 6, 
        'allowance_class': 'h', 
        'beta_rad': 0.5235987755982988, 
        # 'H': 0.8660254037844386, 
        # 'LE_min': 3.2053707416757726, 
        # 'LE_max': 9.587492843405213, 
        'basic_pitch_diameter': 5.350480947161671, 
        # 'basic_minor_diameter': 5.0257214207425065, 
        'r_m': 2.6752404735808355, 
        'psi_rad': 0.05942178951229949, 
        # 'es': 0.0, 
        # 'd3': 4.773130677972045, 
        # 'Td': 0.17685, 
        # 'Td2': 0.10766080789661839, 
        # 'd_max': 6.0, 
        # 'd_min': 5.82315, 
        # 'd2_max': 5.350481, 
        # 'd2_min': 5.242820192103382, 
        # 'd3_max': 4.773130677972045, 
        # 'd3_min': 4.677020192103382, 
        # 'A_t': 19.83732016056229, 
        # 'A_mean': 22.48410087820095,
    }

    try:
        # Send a POST request to the API
        response = requests.post(api_url, json=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            area = result.get("area")
            return area
        else:
            print(f"Error: API returned status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None



def test_bolted_joint_api():
    print("\nStarting client request to thread_fast web app BoltedJoint api...\n")
    # Define the URL of the web API
    # api_url = "https://example.com/api/app_entry_point"
    api_url = "http://localhost:5000/bolted_joint_analysis"

    # Create a dictionary with the input data:
    data = {
        "type": "BoltedJoint",
        "name": "bolted_joint_input_test",
        "fastener": {
            "type": "Fastener",
            "name": "fastener_dict",
            "material": {
                "type": "Material",
                "name": "fastener_material_dict",
                "E": 200000.0,
                "nu": 0.3,
                "cte": 2e-06,
                "Sty": 600.0,
                "Stu": 800.0
            },
            "thread": {
                "type": "Metric_Thread",
                "name": "fastener_thread_dict",
                "basic_major_diameter": 6.0,
                "pitch": 1.0,
                "beta_deg": 30.0,
                "external": True,
                "internal": False,
                "profile": "MJ",
                "tolerance_grade": 6,
                "allowance_class": "h"
            },
            "Do_head": 8.5,
            "Do_shank": 5.0,
            "L_shank": 10.0,
            "L_thread": 20.0
        },
        "clamped_parts": [
            {
                "type": "Washer",
                "name": "washer_test_input_dict",
                "material": {
                    "type": "Material",
                    "name": "washer_material_dict",
                    "E": 200000.0,
                    "nu": 0.3,
                    "cte": 2e-06,
                    "Sty": 600.0,
                    "Stu": 800.0
                },
                "D_hole": 6.1,
                "D_outer": 8.5,
                "thickness": 2.0
            },
            {
                "type": "ClampedPart",
                "name": "clamped_part1",
                "material": {
                    "type": "Material",
                    "name": "ti6al4v",
                    "E": 114000.0,
                    "nu": 0.342,
                    "cte": 8.6e-06,
                    "Sty": 880.0,
                    "Stu": 950.0
                },
                "D_hole": 6.1,
                "D_outer": 12.5,
                "thickness": 5.0
            },
            {
                "type": "ClampedPart",
                "name": "clamped_part2",
                "material": {
                    "type": "Material",
                    "name": "ti6al4v",
                    "E": 114000.0,
                    "nu": 0.342,
                    "cte": 8.6e-06,
                    "Sty": 880.0,
                    "Stu": 950.0
                },
                "D_hole": 6.1,
                "D_outer": 12.5,
                "thickness": 10.0
            },
            {
                "type": "Washer",
                "name": "washer_test_input_dict",
                "material": {
                    "type": "Material",
                    "name": "washer_material_dict",
                    "E": 200000.0,
                    "nu": 0.3,
                    "cte": 2e-06,
                    "Sty": 600.0,
                    "Stu": 800.0
                },
                "D_hole": 6.1,
                "D_outer": 8.5,
                "thickness": 2.0
            }
        ],
        "nut": {
            "type": "Nut",
            "name": "nut_dict",
            "material": {
                "type": "Material",
                "name": "nut_material_dict",
                "E": 200000.0,
                "nu": 0.3,
                "cte": 2e-06,
                "Sty": 600.0,
                "Stu": 800.0
            },
            "thread": {
                "type": "Metric_Thread",
                "name": "test_input_dict",
                "basic_major_diameter": 6.0,
                "pitch": 1.0,
                "beta_deg": 30.0,
                "external": False,
                "internal": True,
                "profile": "MJ",
                "tolerance_grade": 6,
                "allowance_class": "H"
            },
            "Do": 8.5,
            "length": 5.0
        },
        "mu_thread": 0.15,
        "mu_abutment": 0.1,
        "separation_safety_factor": 1.2,
        "yield_safety_factor": 1.1,
        "ultimate_safety_factor": 1.4,
        "fitting_factor": 1.15,
        "preload_stress_ratio": 0.65,
        "preload_uncertainty_factor": 0.25,
        "lower_preload_tolerance_factor": 0.9,
        "upper_preload_tolerance_factor": 1.1,
        "relaxation_ratio": 0.05,
        "preload_loss_due_to_material_creep": 0.0,
        "ambient_temperature": 20.0,
        "max_temperature": 40.0,
        "min_temperature": 10.0,
        "applied_tensile_load": 100.0,
        "applied_shear_load": 100.0,
        "loaded_part_index": [
            1,
            2
        ],
        "nut_torqued": False,
        "distance_between_loading_planes": None,
        "material_creep_preload_loss": 0.0,
        "nut_factor": None,
        "applied_preload_torque": None,
        "applied_preload": None,
        "phi": None
    }

    try:
        # Send a POST request to the API
        response = requests.post(api_url, json=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            print(result)
            print("...finished client request, returning result.")
            return result
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)
            return None
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Example usage

    # test black box app:
    result = test_material_api()
    print(result)
    
    result = test_thread_api()
    print(result)
    
    result = test_fastener_api()
    print(result)

    result = test_bolted_joint_api()
    print(result)
    