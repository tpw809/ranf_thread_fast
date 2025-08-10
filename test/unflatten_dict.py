"""NOT WORKING

Code from ai response to google search for "flatten json python"
"""

def unflatten_dict(flat_dict, separator='.'):
    result = {}
    print("\nstarting for loop:")
    for key, value in flat_dict.items():
        print(f"\nkey = {key}")
        print(f"value={value}")
        parts = key.split(separator)
        print(f"parts = {parts}")
        current = result
        print(f"current={current}")
        for i, part in enumerate(parts):
            print(f"\ni = {i}")
            print(f"part = {part}")
            if i == len(parts) - 1:
                current[part] = value
            else:
                if part.isdigit():  # Handle list indices
                    part = int(part)
                    if not isinstance(current, list):
                        # Convert dict to list if needed
                        temp_list = [None] * (part + 1)
                        if isinstance(current, dict) and current:
                            # If dict has other keys, merge them
                            for k, v in current.items():
                                if k.isdigit():
                                    temp_list[int(k)] = v
                                else:
                                    # Handle cases where non-numeric keys exist
                                    # This scenario might require more complex logic
                                    pass
                        current = temp_list

                    while len(current) <= part:
                        current.append(None) # Fill with None if index out of bounds
                    if current[part] is None:
                        current[part] = {} if not parts[i+1].isdigit() else []
                    current = current[part]

                else: # Handle dictionary keys
                    if part not in current:
                        current[part] = {}
                    current = current[part]
    return result


def main() -> None:

    # Example usage
    print("\n\nTest Unflatten:\n")
    flat_json = {
        "education.0.high_school.name": "St Johns",
        "education.0.high_school.year": "2018",
        "education.1.bachelors.name": "NYU",
        "education.1.bachelors.year": "2022"
    }
    print(flat_json)
    
    unflattened_json = unflatten_dict(flat_json)
    print(unflattened_json)


if __name__ == "__main__":
    main()
    