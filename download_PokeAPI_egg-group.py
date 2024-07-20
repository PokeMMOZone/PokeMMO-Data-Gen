import requests
import json
import time
from requests.exceptions import SSLError

# Base URLs for the PokeAPI
EGG_GROUP_BASE_URL = "https://pokeapi.co/api/v2/egg-group/"
POKEMON_SPECIES_BASE_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
ALL_EGG_GROUPS_FILE = "egg-groups-data.json"

# Lookup table to map API egg group names to PokéMMO egg group names
EGG_GROUP_NAME_LOOKUP = {
    "monster": "monster",
    "water1": "watera",
    "water2": "waterb",
    "water3": "waterc",
    "bug": "bug",
    "flying": "flying",
    "ground": "field",
    "fairy": "fairy",
    "plant": "plant",
    "humanshape": "humanoid",
    "mineral": "mineral",
    "ditto": "ditto",
    "dragon": "dragon",
    "no-eggs": "cannot-breed",
    "indeterminate": "chaos",
    # Add any other egg groups that PokéMMO uses which aren't listed in the PokeAPI
}

species_egg_group_updates = {
    292: {"name": "shedinja", "egg_groups": [15]},  # Shedinja
    30: {"name": "nidorina", "egg_groups": [1, 5]},  # Nidorina
    31: {"name": "nidoqueen", "egg_groups": [1, 5]},  # Nidoqueen
    # Add more species and their new egg group IDs here
}


def request_with_retry(url):
    while True:
        try:
            response = requests.get(url)
            return response
        except (SSLError, requests.exceptions.ReadTimeout) as e:
            if "[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol" in str(
                e
            ) or isinstance(
                e, requests.exceptions.ReadTimeout
            ):
                print(f"Encountered error: {e}. Retrying in 60 seconds...")
                time.sleep(60)
            else:
                raise


def save_data(data, file_name):
    with open(DATA_SAVE_PATH + file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def is_in_first_five_generations(species_id):
    response = request_with_retry(POKEMON_SPECIES_BASE_URL + str(species_id))
    if response.status_code == 200:
        species_data = response.json()
        generation_number = int(species_data["generation"]["url"].split("/")[-2])
        return generation_number <= 5
    return False


def process_pokemon_species(pokemon_species_list):
    filtered_species = []
    for species in pokemon_species_list:
        species_id = species["url"].split("/")[-2]
        if is_in_first_five_generations(species_id):
            species_data = {"name": species["name"], "id": int(species_id)}
            filtered_species.append(species_data)
    return filtered_species


def process_name_translations(names):
    translations = {}
    for name_entry in names:
        language_name = name_entry["language"]["name"]
        translations[language_name] = {"name": name_entry["name"]}
    return translations


def update_species_egg_groups(all_egg_groups, species_egg_group_updates):
    # Remove species from all egg groups first
    for egg_group in all_egg_groups.values():
        egg_group["pokemon_species"] = [
            species
            for species in egg_group["pokemon_species"]
            if species["id"] not in species_egg_group_updates
        ]

    # Add species to the specified egg groups
    for species_id, new_egg_group_info in species_egg_group_updates.items():
        new_egg_groups = new_egg_group_info["egg_groups"]
        species_name = new_egg_group_info["name"]
        for new_egg_group in new_egg_groups:
            if f"egg_group_{new_egg_group}" in all_egg_groups:
                all_egg_groups[f"egg_group_{new_egg_group}"]["pokemon_species"].append(
                    {"name": species_name, "id": species_id}
                )


def get_egg_group_data():
    all_egg_groups = {}

    # Get the total count of egg groups
    response = request_with_retry(EGG_GROUP_BASE_URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return

    total_egg_groups = response.json()["count"]

    # Loop through all egg groups
    for i in range(1, total_egg_groups + 1):
        egg_group_response = request_with_retry(EGG_GROUP_BASE_URL + str(i))
        if egg_group_response.status_code == 200:
            egg_group_data = egg_group_response.json()

            # Initialize processed_egg_group_data
            processed_egg_group_data = {"id": i, "name": egg_group_data["name"]}

            # Replace the egg group name using the lookup table
            if processed_egg_group_data["name"] in EGG_GROUP_NAME_LOOKUP:
                processed_egg_group_data["name"] = EGG_GROUP_NAME_LOOKUP[
                    processed_egg_group_data["name"]
                ]
            else:
                print(
                    f"Warning: Egg group name '{processed_egg_group_data['name']}' not found in lookup table"
                )

            # Process and filter pokemon_species for generations 1-5
            if "pokemon_species" in egg_group_data:
                processed_egg_group_data["pokemon_species"] = process_pokemon_species(
                    egg_group_data["pokemon_species"]
                )

            # Process name translations
            processed_egg_group_data["name_translations"] = process_name_translations(
                egg_group_data.get("names", [])
            )

            # Add modified egg group data to all egg groups
            all_egg_groups[f"egg_group_{i}"] = processed_egg_group_data

    return all_egg_groups


def main():
    all_egg_groups_data = get_egg_group_data()

    update_species_egg_groups(all_egg_groups_data, species_egg_group_updates)

    save_data(all_egg_groups_data, ALL_EGG_GROUPS_FILE)


if __name__ == "__main__":
    main()
