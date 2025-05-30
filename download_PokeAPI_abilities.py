import requests
import json
import time
from requests.exceptions import SSLError

# Constants
BASE_URL = "https://pokeapi.co/api/v2/ability/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "abilities-data.json"
INCLUDED_ABILITIES = [
    "competitive",
    "neutralizing-gas",
    "protean",
    "sharpness",
    "slush-rush",
    "wind-rider",
]  # List of abilities to include regardless of generation
EXCLUDED_ABILITIES = []  # List of abilities to exclude


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


def get_all_abilities():
    abilities = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = request_with_retry(next_url)
        if response.status_code == 200:
            data = response.json()
            abilities.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch abilities list: HTTP {response.status_code}")
            break

    return [ability["name"] for ability in abilities]


def get_ability_data(ability_name):
    response = request_with_retry(f"{BASE_URL}{ability_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for ability {ability_name}")
        return None


def is_ability_in_generations_1_to_5(ability_data):
    generation_name = ability_data.get("generation", {}).get("name", "")
    return generation_name in [
        "generation-i",
        "generation-ii",
        "generation-iii",
        "generation-iv",
        "generation-v",
    ]


def process_ability_data(raw_data):
    if not raw_data.get("is_main_series"):
        return None  # Skip if the ability is not part of the main series
    effect_text = None
    effect_translations = {}
    
    # Process effect entries
    for effect_entry in raw_data.get("effect_entries", []):
        language_name = effect_entry.get("language", {}).get("name")
        short_effect = effect_entry.get("short_effect")
        effect = effect_entry.get("effect")
        if language_name == "en":
            effect_text = short_effect or effect
        effect_translations[language_name] = {"effect": short_effect or effect}
    
    # Process effect changes
    for effect_change in raw_data.get("effect_changes", []):
        for effect_entry in effect_change.get("effect_entries", []):
            language_name = effect_entry.get("language", {}).get("name")
            if language_name not in effect_translations:
                effect_translations[language_name] = {"effect": effect_entry.get("effect")}
    
    # Process flavor text entries
    for flavor_text in raw_data.get("flavor_text_entries", []):
        language_name = flavor_text.get("language", {}).get("name")
        if language_name not in effect_translations:
            effect_translations[language_name] = {"effect": flavor_text.get("flavor_text")}
    
    name_translations = {}
    for translation in raw_data.get("names", []):
        language_name = translation.get("language", {}).get("name")
        name_translations[language_name] = {"name": translation.get("name")}

    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "effect": effect_text,
        "effect_translations": effect_translations,
        "name_translations": name_translations,
    }
    return processed_data


def save_abilities_to_file(abilities, filename):
    with open(DATA_SAVE_PATH + filename, "w", encoding="utf-8") as file:
        json.dump(abilities, file, ensure_ascii=False, indent=4)


def main():
    all_ability_names = get_all_abilities()
    all_abilities = {}

    for ability_name in all_ability_names:
        if ability_name in EXCLUDED_ABILITIES:
            continue  # Skip excluded abilities

        ability_data = get_ability_data(ability_name)
        if ability_data and (
            is_ability_in_generations_1_to_5(ability_data)
            or ability_name in INCLUDED_ABILITIES
        ):
            processed_data = process_ability_data(ability_data)
            if processed_data:  # Add only if processed_data is not None
                all_abilities[processed_data["name"]] = processed_data

    save_abilities_to_file(all_abilities, OUTPUT_FILE)


if __name__ == "__main__":
    main()
