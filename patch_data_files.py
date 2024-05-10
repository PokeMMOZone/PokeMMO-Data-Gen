import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_SAVE_PATH = "./data/"
POKEMON_DATA_FILE = "pokemon-data.json"
POKEMON_PATCH_FILE = "patch_pokemon-data.json"
ABILITIES_DATA_FILE = "abilities-data.json"
ITEM_DATA_FILE = "item-data.json"
MOVES_DATA_FILE = "moves-data.json"
MOVES_PATCH_FILE = "patch_move-data.json"


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def update_nested_key(data, key_path, value):
    keys = key_path.split(".")
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value


def apply_patch(original_data, patch_data):
    for key, changes in patch_data.items():
        for change_key, value in changes.items():
            if "_add" in change_key:
                list_key = change_key.replace("_add", "")
                if list_key in original_data[key]:
                    original_data[key][list_key].extend(value)
            elif "_remove" in change_key:
                list_key = change_key.replace("_remove", "")
                if list_key in original_data[key]:
                    original_data[key][list_key] = [
                        item
                        for item in original_data[key][list_key]
                        if item not in value
                    ]
            elif "." in change_key:
                update_nested_key(original_data[key], change_key, value)
            else:
                original_data[key][change_key] = value


def replace_string_in_data(data, old_string, new_string):
    if isinstance(data, dict):
        for key in list(
            data.keys()
        ):  # Use list to avoid RuntimeError due to change in dictionary size during iteration
            new_key = key.replace(old_string, new_string) if old_string in key else key
            value = data[key]
            if isinstance(value, (dict, list)):
                replace_string_in_data(value, old_string, new_string)
            elif isinstance(value, str):
                value = value.replace(old_string, new_string)

            if new_key != key:
                data[new_key] = value
                del data[key]
            else:
                data[key] = value

    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                replace_string_in_data(item, old_string, new_string)
            elif isinstance(item, str) and old_string in item:
                data[i] = item.replace(old_string, new_string)


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    # Process Pokemon Data
    pokemon_original_data = load_json(DATA_SAVE_PATH + POKEMON_DATA_FILE)
    pokemon_patch_data = load_json(os.path.join(current_dir, POKEMON_PATCH_FILE))

    apply_patch(pokemon_original_data, pokemon_patch_data)
    replace_string_in_data(pokemon_original_data, "neutralizing-gas", "reactive-gas")
    replace_string_in_data(pokemon_original_data, "slush-rush", "snow-plow")
    save_json(pokemon_original_data, DATA_SAVE_PATH + POKEMON_DATA_FILE)

    # Process Abilities Data
    abilities_data = load_json(DATA_SAVE_PATH + ABILITIES_DATA_FILE)
    replace_string_in_data(abilities_data, "neutralizing-gas", "reactive-gas")
    replace_string_in_data(abilities_data, "slush-rush", "snow-plow")
    save_json(abilities_data, DATA_SAVE_PATH + ABILITIES_DATA_FILE)

    # Process Item Data
    # item_data = load_json(DATA_SAVE_PATH + ITEM_DATA_FILE)
    # replace_string_in_data(item_data, "assault-vest", "assault-gear")
    # save_json(item_data, DATA_SAVE_PATH + ITEM_DATA_FILE)

    # Process Move Data
    moves_original_data = load_json(DATA_SAVE_PATH + MOVES_DATA_FILE)
    moves_patch_data = load_json(os.path.join(current_dir, MOVES_PATCH_FILE))
    apply_patch(moves_original_data, moves_patch_data)
    save_json(moves_original_data, DATA_SAVE_PATH + MOVES_DATA_FILE)


if __name__ == "__main__":
    main()
