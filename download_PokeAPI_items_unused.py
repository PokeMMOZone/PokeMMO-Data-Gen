import requests
import json

# Constants
BASE_URL = "https://pokeapi.co/api/v2/item/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "item-data.json"
INCLUDED_ITEMS = ["assault-vest", "ability-capsule", "exp-candy-xs", "exp-candy-s", "exp-candy-m", "exp-candy-l", "exp-candy-xl"]  # List of items to include regardless of generation
EXCLUDED_ITEMS = ["tm01", "tm02"]  # List of items to exclude

def get_all_items():
    items = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = requests.get(next_url)
        if response.status_code == 200:
            data = response.json()
            items.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch items list: HTTP {response.status_code}")
            break

    return [item["name"] for item in items]

def get_item_data(item_name):
    response = requests.get(f"{BASE_URL}{item_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for item {item_name}")
        return None

def is_item_in_generations_1_to_5(item_data):
    game_indices = item_data.get("game_indices", [])
    for index in game_indices:
        generation_name = index.get("generation", {}).get("name", "")
        if generation_name in ["generation-i", "generation-ii", "generation-iii", "generation-iv", "generation-v"]:
            return True
    return False


def process_item_data(raw_data):
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "attributes": [attr["name"] for attr in raw_data.get("attributes", [])],
        "category": raw_data.get("category", {}).get("name"),
        "effect": raw_data.get("effect_entries")[0].get("short_effect") if raw_data.get("effect_entries") else None,
        "sprite": raw_data.get("sprites", {}).get("default")
    }
    return processed_data

def save_items_to_file(items, filename):
    with open(DATA_SAVE_PATH + filename, 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def main():
    all_item_names = get_all_items()
    all_items = {}

    for item_name in all_item_names:
        if item_name in EXCLUDED_ITEMS:
            continue  # Skip excluded items

        item_data = get_item_data(item_name)
        if item_data and (is_item_in_generations_1_to_5(item_data) or item_name in INCLUDED_ITEMS):
            processed_data = process_item_data(item_data)
            all_items[processed_data["name"]] = processed_data

    save_items_to_file(all_items, OUTPUT_FILE)

if __name__ == "__main__":
    main()
