import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
LOCATIONS_FILE = os.path.join(current_dir, "locations.json")
PATCH_FILE = os.path.join(current_dir, "patch_locations.json")
info_directory = os.path.join(current_dir, "dump/info")
monsters_file = os.path.join(info_directory, "monsters.json")

# Add your lookup dictionary here
name_change_lookup = {
    "nidoran♀": "nidoran-f",
    "nidoran♂": "nidoran-m",
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr",
    # Add more name mappings as needed
}


def apply_patch(locations_data, patch_data):
    """Applies additions and removals from the patch file to the locations data."""
    # Add locations
    for pokemon, new_locations in patch_data.get("add", {}).items():
        if pokemon not in locations_data:
            locations_data[pokemon] = {"locations": []}
        locations_data[pokemon]["locations"].extend(new_locations)

    # Remove locations
    for pokemon, locations_to_remove in patch_data.get("remove", {}).items():
        if pokemon in locations_data:
            locations_data[pokemon]["locations"] = [
                loc
                for loc in locations_data[pokemon]["locations"]
                if loc["location"] not in locations_to_remove
            ]
            # Remove the Pokémon entry if no locations remain
            if not locations_data[pokemon]["locations"]:
                del locations_data[pokemon]


def generate_locations_json(filepath):
    """Generates the locations.json file."""
    # Dictionary to hold all location data
    locations_data = {}

    # Open the monsters.json file
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

        for pokemon in data:
            # Using the Pokémon's name in lowercase as the key
            pokemon_name = pokemon["name"].lower()

            # Check if the Pokémon's name needs to be changed
            if pokemon_name in name_change_lookup:
                pokemon_name = name_change_lookup[pokemon_name]

            # Extracting the location information
            locations_data[pokemon_name] = {"locations": pokemon.get("locations", [])}

    # Read and apply the patch file
    if os.path.exists(PATCH_FILE):
        with open(PATCH_FILE, "r", encoding="utf-8") as patch_file:
            patch_data = json.load(patch_file)
            apply_patch(locations_data, patch_data)

    # Write the compiled data to locations.json
    with open(LOCATIONS_FILE, "w", encoding="utf-8") as outfile:
        json.dump(locations_data, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_locations_json(monsters_file)
