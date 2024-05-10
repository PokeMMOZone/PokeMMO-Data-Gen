import json

# File paths
POKEMON_DATA_FILE = './data/pokemon-data.json'
MOVES_DATA_FILE = './data/moves-data.json'

def read_json_file(file_path):
    """ Reads a JSON file and returns its content. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def update_moves_with_pokemon(pokemon_data, moves_data):
    """ Updates moves data with the Pokémon that can learn each move and returns the updated data. """
    for pokemon_name, pokemon_info in pokemon_data.items():
        for move in pokemon_info.get('moves', []):
            move_id = move['id']
            matched = False
            for move_name, move_data in moves_data.items():
                if move_data['id'] == move_id:
                    matched = True
                    # Check if the Pokémon is already in the list
                    if 'learned_by_pokemon' not in move_data:
                        move_data['learned_by_pokemon'] = []
                    if not any(p['id'] == pokemon_info['id'] for p in move_data['learned_by_pokemon']):
                        move_data['learned_by_pokemon'].append({
                            'name': pokemon_name,
                            'id': pokemon_info['id']
                        })
                    break
            if not matched:
                print(f"No matching ID found for move: {move['name']}")
    return moves_data

def save_json_file(data, file_path):
    """ Saves data to a JSON file. """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # Load data from files
    pokemon_data = read_json_file(POKEMON_DATA_FILE)
    moves_data = read_json_file(MOVES_DATA_FILE)

    # Update moves data with the Pokémon that can learn them
    updated_moves_data = update_moves_with_pokemon(pokemon_data, moves_data)

    # Save the updated moves data back to the same file
    save_json_file(updated_moves_data, MOVES_DATA_FILE)

if __name__ == "__main__":
    main()
