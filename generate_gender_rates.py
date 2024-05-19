import json
import os

# Constants
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "gender-rates.json"
POKEMON_DATA_FILE = './data/pokemon-data.json'

# Gender rate mappings
GENDER_RATE_MAPPING = {
    -1: {"name": "Genderless", "female_percentage": 0, "male_percentage": 0, "pokemon_list": []},
    0: {"name": "0% Female, 100% Male", "female_percentage": 0, "male_percentage": 100, "pokemon_list": []},
    1: {"name": "12.5% Female, 87.5% Male", "female_percentage": 12.5, "male_percentage": 87.5, "pokemon_list": []},
    2: {"name": "25% Female, 75% Male", "female_percentage": 25, "male_percentage": 75, "pokemon_list": []},
    3: {"name": "37.5% Female, 62.5% Male", "female_percentage": 37.5, "male_percentage": 62.5, "pokemon_list": []},
    4: {"name": "50% Female, 50% Male", "female_percentage": 50, "male_percentage": 50, "pokemon_list": []},
    5: {"name": "62.5% Female, 37.5% Male", "female_percentage": 62.5, "male_percentage": 37.5, "pokemon_list": []},
    6: {"name": "75% Female, 25% Male", "female_percentage": 75, "male_percentage": 25, "pokemon_list": []},
    7: {"name": "87.5% Female, 12.5% Male", "female_percentage": 87.5, "male_percentage": 12.5, "pokemon_list": []},
    8: {"name": "100% Female, 0% Male", "female_percentage": 100, "male_percentage": 0, "pokemon_list": []}
}

def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def update_gender_rates_with_pokemon(pokemon_data, gender_rates):
    """Updates gender rates with the Pokémon that have each gender rate."""
    for pokemon_name, pokemon_info in pokemon_data.items():
        gender_rate = pokemon_info.get("gender_rate")
        if gender_rate in gender_rates:
            gender_rates[gender_rate]["pokemon_list"].append({"name": pokemon_name, "id": pokemon_info["id"]})
    return gender_rates

def save_json_file(data, file_path):
    """Saves data to a JSON file."""
    if not os.path.exists(DATA_SAVE_PATH):
        os.makedirs(DATA_SAVE_PATH)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # Load data from files
    pokemon_data = read_json_file(POKEMON_DATA_FILE)
    
    # Update gender rates with the Pokémon that have each gender rate
    updated_gender_rates = update_gender_rates_with_pokemon(pokemon_data, GENDER_RATE_MAPPING)
    
    # Save the updated gender rates data
    save_json_file(updated_gender_rates, DATA_SAVE_PATH + OUTPUT_FILE)

if __name__ == "__main__":
    main()
