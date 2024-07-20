import json
import os

# Constants
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "gender-rates.json"
POKEMON_DATA_FILE = './data/pokemon-data.json'

# Gender rate mappings with translations
GENDER_RATE_MAPPING = {
    -1: {
        "name": "Genderless",
        "female_percentage": 0,
        "male_percentage": 0,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "性別不明"},
            "ko": {"name": "성별 없음"},
            "zh-Hant": {"name": "無性別"},
            "fr": {"name": "Sans sexe"},
            "de": {"name": "Geschlechtslos"},
            "es": {"name": "Sin género"},
            "it": {"name": "Senza sesso"},
            "en": {"name": "Genderless"},
            "ja": {"name": "性別不明"},
            "zh-Hans": {"name": "无性别"}
        }
    },
    0: {
        "name": "0% Female, 100% Male",
        "female_percentage": 0,
        "male_percentage": 100,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス0%・オス100%"},
            "ko": {"name": "0% 암컷, 100% 수컷"},
            "zh-Hant": {"name": "0%雌性，100%雄性"},
            "fr": {"name": "0% femelle, 100% mâle"},
            "de": {"name": "0% weiblich, 100% männlich"},
            "es": {"name": "0% hembra, 100% macho"},
            "it": {"name": "0% femmina, 100% maschio"},
            "en": {"name": "0% Female, 100% Male"},
            "ja": {"name": "メス0%・オス100%"},
            "zh-Hans": {"name": "0%雌性，100%雄性"}
        }
    },
    1: {
        "name": "12.5% Female, 87.5% Male",
        "female_percentage": 12.5,
        "male_percentage": 87.5,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス12.5%・オス87.5%"},
            "ko": {"name": "12.5% 암컷, 87.5% 수컷"},
            "zh-Hant": {"name": "12.5%雌性，87.5%雄性"},
            "fr": {"name": "12.5% femelle, 87.5% mâle"},
            "de": {"name": "12.5% weiblich, 87.5% männlich"},
            "es": {"name": "12.5% hembra, 87.5% macho"},
            "it": {"name": "12.5% femmina, 87.5% maschio"},
            "en": {"name": "12.5% Female, 87.5% Male"},
            "ja": {"name": "メス12.5%・オス87.5%"},
            "zh-Hans": {"name": "12.5%雌性，87.5%雄性"}
        }
    },
    2: {
        "name": "25% Female, 75% Male",
        "female_percentage": 25,
        "male_percentage": 75,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス25%・オス75%"},
            "ko": {"name": "25% 암컷, 75% 수컷"},
            "zh-Hant": {"name": "25%雌性，75%雄性"},
            "fr": {"name": "25% femelle, 75% mâle"},
            "de": {"name": "25% weiblich, 75% männlich"},
            "es": {"name": "25% hembra, 75% macho"},
            "it": {"name": "25% femmina, 75% maschio"},
            "en": {"name": "25% Female, 75% Male"},
            "ja": {"name": "メス25%・オス75%"},
            "zh-Hans": {"name": "25%雌性，75%雄性"}
        }
    },
    4: {
        "name": "50% Female, 50% Male",
        "female_percentage": 50,
        "male_percentage": 50,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス50%・オス50%"},
            "ko": {"name": "50% 암컷, 50% 수컷"},
            "zh-Hant": {"name": "50%雌性，50%雄性"},
            "fr": {"name": "50% femelle, 50% mâle"},
            "de": {"name": "50% weiblich, 50% männlich"},
            "es": {"name": "50% hembra, 50% macho"},
            "it": {"name": "50% femmina, 50% maschio"},
            "en": {"name": "50% Female, 50% Male"},
            "ja": {"name": "メス50%・オス50%"},
            "zh-Hans": {"name": "50%雌性，50%雄性"}
        }
    },
    6: {
        "name": "75% Female, 25% Male",
        "female_percentage": 75,
        "male_percentage": 25,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス75%・オス25%"},
            "ko": {"name": "75% 암컷, 25% 수컷"},
            "zh-Hant": {"name": "75%雌性，25%雄性"},
            "fr": {"name": "75% femelle, 25% mâle"},
            "de": {"name": "75% weiblich, 25% männlich"},
            "es": {"name": "75% hembra, 25% macho"},
            "it": {"name": "75% femmina, 25% maschio"},
            "en": {"name": "75% Female, 25% Male"},
            "ja": {"name": "メス75%・オス25%"},
            "zh-Hans": {"name": "75%雌性，25%雄性"}
        }
    },
    8: {
        "name": "100% Female, 0% Male",
        "female_percentage": 100,
        "male_percentage": 0,
        "pokemon_list": [],
        "name_translations": {
            "ja-Hrkt": {"name": "メス100%・オス0%"},
            "ko": {"name": "100% 암컷, 0% 수컷"},
            "zh-Hant": {"name": "100%雌性，0%雄性"},
            "fr": {"name": "100% femelle, 0% mâle"},
            "de": {"name": "100% weiblich, 0% männlich"},
            "es": {"name": "100% hembra, 0% macho"},
            "it": {"name": "100% femmina, 0% maschio"},
            "en": {"name": "100% Female, 0% Male"},
            "ja": {"name": "メス100%・オス0%"},
            "zh-Hans": {"name": "100%雌性，0%雄性"}
        }
    }
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
