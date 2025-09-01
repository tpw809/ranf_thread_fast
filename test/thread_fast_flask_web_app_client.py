import requests


def run_black_box():
    print("Starting client request to black_box web app...")
    # Define the URL of the web API
    # api_url = "https://example.com/api/app_entry_point"
    api_url = "http://localhost:5000/material"

    # Create a dictionary with the input data:
    data = {
        "type": "Material",
        "name": "a286",
        "E_mpa": 200000.0,
        "nu": 0.3,
        "cte_mm_mm_C": 1.65e-05,
        "rho_gcc": 7.93,
        "tc_w_mK": 15.1,
        "hc_J_gC": 0.42,
        "Sty_mpa": 586.0,
        "Stu_mpa": 896.0,
        "Ssy_mpa": 338.32725774512073,
        "Ssu_mpa": 517.3058411939047,
        "Scy_mpa": 879.0,
        "Scu_mpa": 1344.0
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
    print("Starting client request to thread_fast.thread web app...")
    # Define the URL of the web API
    # api_url = "https://example.com/api/rectangle_area"
    api_url = "http://localhost:5000/rectangle"

    # Create a dictionary with the input data (side lengths)
    data = {
        "length": length, 
        "width": width,
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


if __name__ == "__main__":
    # Example usage

    # test black box app:
    result = run_black_box()
    print(result)
