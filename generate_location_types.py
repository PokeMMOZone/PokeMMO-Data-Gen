import json
import os

def read_location_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_type_data(location_data):
    type_data = {}
    for location, data in location_data.items():
        for encounter in data.get("encounters", []):
            encounter_type = encounter.get("type")
            if encounter_type not in type_data:
                type_data[encounter_type] = []
            type_data[encounter_type].append(encounter)
    return type_data

def save_type_data(type_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(type_data, file, ensure_ascii=False, indent=4)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    location_file = "location-data.json"
    type_file = "location-types.json"

    # Read the existing location data
    location_data_path = os.path.join(data_save_path, location_file)
    location_data = read_location_data(location_data_path)

    # Generate Type data
    type_data = generate_type_data(location_data)

    # Save the Type data to a JSON file
    type_data_path = os.path.join(data_save_path, type_file)
    save_type_data(type_data, type_data_path)

    print(f"Type data saved to {type_data_path}")

if __name__ == "__main__":
    main()
