import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
OBTAINABLE_FILE = os.path.join(current_dir, "obtainable_pokemon.json")
info_directory = os.path.join(current_dir, "dump/info")
monsters_file = os.path.join(
    info_directory, "monsters.json"
)  # Path to the monsters.json file

# Add your lookup dictionary here for renaming pokemon if needed
name_change_lookup = {
    "nidoran♀": "nidoran-f",
    "nidoran♂": "nidoran-m",
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr",
    # Add more name mappings as needed
}


def generate_obtainable_json(filepath):
    # Dictionary to hold all obtainable data
    obtainable_data = {}

    # Open the monsters.json file
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

        for pokemon in data:
            # Using the Pokémon's name in lowercase as the key
            pokemon_name = pokemon["name"].lower()

            # Check if the Pokémon's name needs to be changed
            if pokemon_name in name_change_lookup:
                pokemon_name = name_change_lookup[pokemon_name]

            # Creating a dictionary with the 'obtainable' key
            obtainable_info = {"obtainable": pokemon.get("obtainable", False)}

            # Assigning the dictionary to the Pokémon name key
            obtainable_data[pokemon_name] = obtainable_info

    # Write the compiled data to obtainable_pokemon.json
    with open(OBTAINABLE_FILE, "w", encoding="utf-8") as outfile:
        json.dump(obtainable_data, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_obtainable_json(monsters_file)
