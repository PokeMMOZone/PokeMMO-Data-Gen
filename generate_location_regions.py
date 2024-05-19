import json
import os

def read_location_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_region_data(location_data):
    region_data = {}
    for location, data in location_data.items():
        for encounter in data.get("encounters", []):
            region = encounter.get("region_name")
            if region not in region_data:
                region_data[region] = []
            region_data[region].append(encounter)
    return region_data

def save_region_data(region_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(region_data, file, ensure_ascii=False, indent=4)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    location_file = "location-data.json"
    region_file = "location-regions.json"

    # Read the existing location data
    location_data_path = os.path.join(data_save_path, location_file)
    location_data = read_location_data(location_data_path)

    # Generate Region data
    region_data = generate_region_data(location_data)

    # Save the Region data to a JSON file
    region_data_path = os.path.join(data_save_path, region_file)
    save_region_data(region_data, region_data_path)

    print(f"Region data saved to {region_data_path}")

if __name__ == "__main__":
    main()
