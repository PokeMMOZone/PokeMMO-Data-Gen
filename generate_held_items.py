import json
import os

# Constants
current_dir = os.path.dirname(os.path.abspath(__file__))
info_directory = os.path.join(current_dir, "dump", "info")
data_directory = os.path.join(current_dir, "..", "data")
POKEMON_DATA_FILE = os.path.join(data_directory, 'pokemon-data.json')
ITEM_DATA_FILE = os.path.join(data_directory, 'item-data.json')
MONSTERS_FILE = os.path.join(info_directory, 'monsters.json')
ITEMS_FILE = os.path.join(info_directory, "items.json")

# Add your lookup dictionary here for renaming pokemon if needed
name_change_lookup = {
    "nidoran♀": "nidoran-f",
    "nidoran♂": "nidoran-m",
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr",
    # Add more name mappings as needed
}

def read_json_file(file_path):
    """ Reads a JSON file and returns its content. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(data, file_path):
    """ Saves data to a JSON file. """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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

def process_items(items):
    """Process raw items to match the names and structure in item-data.json"""
    processed_items = {}
    for item in items:
        processed_data = process_item_data(item)
        item_name_key = processed_data["name"].replace(" ", "-").lower()
        processed_items[item_name_key] = processed_data
    return processed_items

def update_pokemon_with_held_items(pokemon_data, monsters_data):
    """ Updates pokemon data with the held items information. """
    for pokemon in monsters_data:
        pokemon_name = pokemon["name"].lower()
        if pokemon_name in name_change_lookup:
            pokemon_name = name_change_lookup[pokemon_name]

        if pokemon_name in pokemon_data:
            pokemon_data[pokemon_name]["held_items"] = []
            for item in pokemon.get("held_items", []):
                item_name_key = item["name"].replace(" ", "-").lower()
                pokemon_data[pokemon_name]["held_items"].append({
                    "id": item["id"],
                    "item_name": item_name_key
                })

    return pokemon_data

def update_items_with_pokemon(monsters_data, item_data):
    """ Updates item data with the Pokémon that can hold each item. """
    for pokemon in monsters_data:
        pokemon_name = pokemon["name"].lower()
        if pokemon_name in name_change_lookup:
            pokemon_name = name_change_lookup[pokemon_name]

        for item in pokemon.get("held_items", []):
            item_name = item["name"].replace(" ", "-").lower()
            if item_name in item_data:
                if 'pokemon_with_item' not in item_data[item_name]:
                    item_data[item_name]['pokemon_with_item'] = []
                item_data[item_name]['pokemon_with_item'].append({
                    'name': pokemon_name,
                    'id': pokemon['id']
                })
            else:
                item_data[item_name] = {
                    'id': item['id'],
                    'name': item_name,
                    'pokemon_with_item': [
                        {
                            'name': pokemon_name,
                            'id': pokemon['id']
                        }
                    ]
                }

    return item_data

def main():
    # Load data from files
    pokemon_data = read_json_file(POKEMON_DATA_FILE)
    item_data = read_json_file(ITEM_DATA_FILE)
    monsters_data = read_json_file(MONSTERS_FILE)
    raw_items = read_json_file(ITEMS_FILE)

    # Process raw items to match item-data.json structure
    processed_items = process_items(raw_items)

    # Update item_data with processed_items
    for item_name, item_info in processed_items.items():
        if item_name not in item_data:
            item_data[item_name] = item_info

    # Update pokemon data with the held items information
    updated_pokemon_data = update_pokemon_with_held_items(pokemon_data, monsters_data)

    # Update item data with the Pokémon that can hold each item
    updated_item_data = update_items_with_pokemon(monsters_data, item_data)

    # Save the updated data back to the files
    save_json_file(updated_pokemon_data, POKEMON_DATA_FILE)
    save_json_file(updated_item_data, ITEM_DATA_FILE)

if __name__ == "__main__":
    main()
