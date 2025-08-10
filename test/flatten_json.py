"""Flatten json for readability in csv (2D table).

"""

def flatten_json(nested_json):
    """
    Flattens a nested JSON object into a single-level dictionary.
    """
    flattened = {}
    
    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            flattened[name[:-1]] = x
    
    flatten(nested_json)
    return flattened


def main() -> None:

    # Example usage:
    nested_data = {
        "user": {
            "name": "John Doe",
            "contact": {
                "email": "john.doe@example.com",
                "phone": "123-456-7890"
            },
            "addresses": [
                {"street": "123 Main St", "city": "Anytown"},
                {"street": "456 Oak Ave", "city": "Otherville"}
            ]
        },
        "order_id": "ABC12345"
    }
    print(nested_data)
    
    flattened_data = flatten_json(nested_data)
    print(flattened_data)
    
    
    # Test unflatten:
    print("\n\nTest Unflatten:\n")
    
    # pip install unflatten
    from unflatten import unflatten

    flat_dict = {"item.subitem.key": "value1", "item2.subitem.0": "value5"}
    unflattened_dict = unflatten(flat_dict)
    print(unflattened_dict)

    # Example usage
    
    flat_json = {
        "education.0.high_school.name": "St Johns",
        "education.0.high_school.year": "2018",
        "education.1.bachelors.name": "NYU",
        "education.1.bachelors.year": "2022"
    }
    print(flat_json)
    
    unflattened_json = unflatten(flat_json)
    print(f"\nunflattened_json:\n")
    print(unflattened_json)


if __name__ == "__main__":
    main()
    