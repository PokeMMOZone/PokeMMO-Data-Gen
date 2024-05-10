import json

# File paths
POKEMON_DATA_FILE = './data/pokemon-data.json'
ABILITIES_DATA_FILE = './data/abilities-data.json'

def read_json_file(file_path):
    """ Reads a JSON file and returns its content. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def update_abilities_with_pokemon(pokemon_data, abilities_data):
    """ Updates abilities data with the Pokémon that have each ability and returns the updated data. """
    for pokemon_name, pokemon_info in pokemon_data.items():
        for ability in pokemon_info.get('abilities', []):
            ability_id = ability['id']
            matched = False
            for ability_name, ability_data in abilities_data.items():
                if ability_data['id'] == ability_id:
                    matched = True
                    if 'pokemon_with_ability' not in ability_data:
                        ability_data['pokemon_with_ability'] = []
                    ability_data['pokemon_with_ability'].append({
                        'name': pokemon_name,
                        'id': pokemon_info['id']
                    })
                    break
            if not matched:
                print(f"No matching ID found for ability: {ability['ability_name']}")
    return abilities_data

def save_json_file(data, file_path):
    """ Saves data to a JSON file. """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # Load data from files
    pokemon_data = read_json_file(POKEMON_DATA_FILE)
    abilities_data = read_json_file(ABILITIES_DATA_FILE)

    # Update abilities data with the Pokémon that have them
    updated_abilities_data = update_abilities_with_pokemon(pokemon_data, abilities_data)

    # Save the updated abilities data back to the same file
    save_json_file(updated_abilities_data, ABILITIES_DATA_FILE)

if __name__ == "__main__":
    main()
