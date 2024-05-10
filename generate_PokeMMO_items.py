import json
import os

# Constants
current_dir = os.path.dirname(os.path.abspath(__file__))
info_directory = os.path.join(current_dir, "dump", "info")
DATA_SOURCE_PATH = os.path.join(info_directory, "items.json")  # Path to your items.json file
DATA_SAVE_PATH = "./data/"  # Adjust this path as necessary
OUTPUT_FILE = "item-data.json"  # The output file name

def read_items_from_file(filepath):
    """Reads items from a given JSON file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        items = json.load(file)
    return items

def process_item_data(raw_data):
    """Processes and structures item data."""
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        # "attributes": [attr["name"] for attr in raw_data.get("attributes", [])],
        # "category": raw_data.get("category", {}).get("name"),
        "effect": raw_data.get("desc"),
        "sprite": raw_data.get("icon_id")
    }
    return processed_data

def save_items_to_file(items, filename):
    """Saves items to a JSON file."""
    with open(os.path.join(DATA_SAVE_PATH, filename), 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def main():
    items = read_items_from_file(DATA_SOURCE_PATH)
    all_items = {}

    for item in items:
        processed_data = process_item_data(item)
        item_name_key = processed_data["name"].replace(" ", "-").lower()
        all_items[item_name_key] = processed_data

    save_items_to_file(all_items, OUTPUT_FILE)

if __name__ == "__main__":
    main()
