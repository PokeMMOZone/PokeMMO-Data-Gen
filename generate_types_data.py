import json
import os
import requests
import time
from requests.exceptions import SSLError

# Constants
BASE_URL = "https://pokeapi.co/api/v2/type/"
DATA_SAVE_PATH = "./data/"
ALL_POKEMON_FILE = "pokemon-data.json"
ALL_MOVES_FILE = "moves-data.json"
TYPES_FILE = "types-data.json"

# Ensure the data directory exists
if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)


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


def read_pokemon_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_moves_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_type_translations():
    response = request_with_retry(BASE_URL)
    if response.status_code != 200:
        print("Failed to retrieve types data")
        return {}

    types_data = response.json()["results"]
    translations = {}

    for type_info in types_data:
        type_name = type_info["name"]
        type_url = type_info["url"]
        type_response = request_with_retry(type_url)
        if type_response.status_code == 200:
            type_data = type_response.json()
            type_translations = {}
            for name_entry in type_data.get("names", []):
                language_name = name_entry["language"]["name"]
                type_translations[language_name] = {"name": name_entry["name"]}
            translations[type_name] = type_translations
        else:
            print(f"Failed to fetch data for type {type_name}")

    return translations


def generate_types_data(pokemon_data, moves_data, translations):
    types_data = {}
    for pokemon, data in pokemon_data.items():
        for poke_type in data.get("types", []):
            if poke_type not in types_data:
                types_data[poke_type] = {"pokemon": [], "moves": [], "name_translations": translations.get(poke_type, {})}
            types_data[poke_type]["pokemon"].append({"name": pokemon, "id": data["id"]})

    for move, data in moves_data.items():
        move_type = data.get("type")
        if move_type and move_type in types_data:
            types_data[move_type]["moves"].append({"name": move, "id": data["id"]})

    return types_data


def save_types_data(types_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(types_data, file, ensure_ascii=False, indent=4)


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Read the existing Pokémon and Moves data
    pokemon_data_path = os.path.join(DATA_SAVE_PATH, ALL_POKEMON_FILE)
    pokemon_data = read_pokemon_data(pokemon_data_path)

    moves_data_path = os.path.join(DATA_SAVE_PATH, ALL_MOVES_FILE)
    moves_data = read_moves_data(moves_data_path)

    # Fetch type translations from PokeAPI
    translations = fetch_type_translations()

    # Generate Types data
    types_data = generate_types_data(pokemon_data, moves_data, translations)

    # Save the Types data to a JSON file
    types_data_path = os.path.join(DATA_SAVE_PATH, TYPES_FILE)
    save_types_data(types_data, types_data_path)

    print(f"Types data saved to {types_data_path}")


if __name__ == "__main__":
    main()
