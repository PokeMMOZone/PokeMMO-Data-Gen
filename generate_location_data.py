import json
import os


def read_pokemon_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_location_data(pokemon_data):
    location_data = {}
    for pokemon, data in pokemon_data.items():
        pokemon_id = data["id"]  # Extract the Pokémon ID
        for encounter in data.get("location_area_encounters", []):
            region = encounter.get("region_name", "").upper()
            location_name = encounter["location"].replace(" ", "_").upper()
            location_key = f"{region}_{location_name}"  # Combine region and location

            if location_key not in location_data:
                location_data[location_key] = {
                    "name": encounter["location"],
                    "region": region,  # Add region field
                    "encounters": [],
                }
            encounter_info = {
                "pokemon": pokemon,
                "pokemon_id": pokemon_id,  # Include the Pokémon ID
                "type": encounter.get("type"),
                "region_id": encounter.get("region_id"),
                "region_name": encounter.get("region_name"),
                "location": encounter.get("location"),
                "min_level": encounter.get("min_level"),
                "max_level": encounter.get("max_level"),
                "rarity": encounter.get("rarity"),
            }
            location_data[location_key]["encounters"].append(encounter_info)
    return location_data


def save_location_data(location_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(location_data, file, ensure_ascii=False, indent=4)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    all_pokemon_file = "pokemon-data.json"
    location_file = "location-data.json"

    # Read the existing Pokémon data
    pokemon_data_path = os.path.join(data_save_path, all_pokemon_file)
    pokemon_data = read_pokemon_data(pokemon_data_path)

    # Generate Location data
    location_data = generate_location_data(pokemon_data)

    # Save the Location data to a JSON file
    location_data_path = os.path.join(data_save_path, location_file)
    save_location_data(location_data, location_data_path)

    print(f"Location data saved to {location_data_path}")


if __name__ == "__main__":
    main()
