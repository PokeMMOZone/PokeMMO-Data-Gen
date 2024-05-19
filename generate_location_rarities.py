import json
import os

def read_location_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_rarity_data(location_data):
    rarity_data = {}
    for location, data in location_data.items():
        for encounter in data.get("encounters", []):
            rarity = encounter.get("rarity")
            if rarity not in rarity_data:
                rarity_data[rarity] = []
            rarity_data[rarity].append(encounter)
    return rarity_data

def save_rarity_data(rarity_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(rarity_data, file, ensure_ascii=False, indent=4)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    location_file = "location-data.json"
    rarity_file = "location-rarities.json"

    # Read the existing location data
    location_data_path = os.path.join(data_save_path, location_file)
    location_data = read_location_data(location_data_path)

    # Generate Rarity data
    rarity_data = generate_rarity_data(location_data)

    # Save the Rarity data to a JSON file
    rarity_data_path = os.path.join(data_save_path, rarity_file)
    save_rarity_data(rarity_data, rarity_data_path)

    print(f"Rarity data saved to {rarity_data_path}")

if __name__ == "__main__":
    main()
