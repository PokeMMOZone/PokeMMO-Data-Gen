import json
import os

def read_pokemon_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_pvp_data(pokemon_data):
    pvp_tiers = {}
    for pokemon, data in pokemon_data.items():
        if 'pvp' in data:
            for pvp_info in data['pvp']:
                tier = pvp_info['tier']
                if tier not in pvp_tiers:
                    pvp_tiers[tier] = []
                pvp_tiers[tier].append({"name": pokemon, "id": data["id"]})
    return pvp_tiers

def save_pvp_data(pvp_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(pvp_data, file, ensure_ascii=False, indent=4)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_save_path = "./data/"
    all_pokemon_file = "pokemon-data.json"
    pvp_file = "pvp-data.json"

    # Read the existing Pokémon data
    pokemon_data_path = os.path.join(data_save_path, all_pokemon_file)
    pokemon_data = read_pokemon_data(pokemon_data_path)

    # Generate PvP data
    pvp_data = generate_pvp_data(pokemon_data)

    # Save the PvP data to a JSON file
    pvp_data_path = os.path.join(data_save_path, pvp_file)
    save_pvp_data(pvp_data, pvp_data_path)

    print(f"PvP data saved to {pvp_data_path}")

if __name__ == "__main__":
    main()
