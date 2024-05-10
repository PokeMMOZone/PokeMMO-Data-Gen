import json
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    """Writes data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def merge_pvp_data(pokemon_data, pvp_data):
    """Merges PvP data into the main Pokémon data."""
    for pokemon_name, data in pvp_data.items():
        if pokemon_name in pokemon_data:
            pokemon_data[pokemon_name].update(data)
        else:
            print(f"Warning: '{pokemon_name}' not found in Pokémon data.")
    return pokemon_data

def main():
    ALL_POKEMON_FILE = "pokemon-data.json"
    DATA_SAVE_PATH = "./data/"
    pokemon_data_path = DATA_SAVE_PATH + ALL_POKEMON_FILE  # Path to the main Pokémon data file
    pvp_data_path = os.path.join(current_dir, "pokemon-pvp-data.json") # Path to the PvP data file


    # Read the existing data files
    pokemon_data = read_json_file(pokemon_data_path)
    pvp_data = read_json_file(pvp_data_path)

    # Merge the PvP data into the main Pokémon data
    merged_data = merge_pvp_data(pokemon_data, pvp_data)

    # Save the updated data back to the main data file
    write_json_file(merged_data, pokemon_data_path)
    print("PvP data merged successfully.")

if __name__ == "__main__":
    main()
