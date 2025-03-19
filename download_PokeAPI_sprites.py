import requests
import json
import os
import time
from requests.exceptions import SSLError

# Base URLs for the PokeAPI
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
POKEMON_FORM_URL = "https://pokeapi.co/api/v2/pokemon-form/"
DATA_SAVE_PATH = "./data/"
SPRITES_FILE = "pokemon-sprites.json"

EXCLUDED_VARIATION_PATTERNS = [
    "-mega",
    "-gmax",
    "-alola",
    "-hisui",
    "-galar",
    "-rock-star",
    "-belle",
    "-pop-star",
    "-phd",
    "-libre",
    "-cosplay",
    "-original-cap",
    "-hoenn-cap",
    "-sinnoh-cap",
    "-unova-cap",
    "-kalos-cap",
    "-partner-cap",
    "-starter",
    "-world-cap",
    "-primal",
    "-paldea",
    "-totem",
    "palkia-origin",
    "dialga-origin",
    "basculin-white-striped",
    "unown-a",
    "arceus-normal",
    "arceus-unknown",
    "arceus-fairy",
    "mothim-plant",
    "pichu-spiky-eared",
    "burmy-plant",
    "cherrim-overcast",
    "shellos-west",
    "gastrodon-west",
    "deerling-spring",
    "sawsbuck-spring",
]


def request_with_retry(url):
    while True:
        try:
            response = requests.get(url)
            return response
        except (SSLError, requests.exceptions.ReadTimeout) as e:
            if "[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol" in str(
                e
            ) or isinstance(
                e, requests.exceptions.ReadTimeout
            ):
                print(f"Encountered error: {e}. Retrying in 60 seconds...")
                time.sleep(60)
            else:
                raise


def is_in_first_five_generations(species_url):
    response = request_with_retry(species_url)
    if response.status_code == 200:
        species_data = response.json()
        generation_url = species_data["generation"]["url"]
        generation_id = int(generation_url.split("/")[-2])
        return 1 <= generation_id <= 5
    return False


def process_varieties(species_id):
    response = request_with_retry(POKEMON_SPECIES_URL + str(species_id))
    if response.status_code == 200:
        species_data = response.json()
        varieties = species_data["varieties"]

        processed_varieties = []
        for variety in varieties:
            name = variety["pokemon"]["name"]
            # Exclude specific variations
            if any(
                excluded in name
                for excluded in [
                    "-mega",
                    "-gmax",
                    "-alola",
                    "-hisui",
                    "-galar",
                    "-rock-star",
                    "-belle",
                    "-pop-star",
                    "-phd",
                    "-libre",
                    "-cosplay",
                    "-original-cap",
                    "-hoenn-cap",
                    "-sinnoh-cap",
                    "-unova-cap",
                    "-kalos-cap",
                    "-partner-cap",
                    "-starter",
                    "-world-cap",
                    "-primal",
                    "-paldea",
                    "-totem",
                    "palkia-origin",
                    "dialga-origin",
                    "basculin-white-striped",
                ]
            ):
                continue

            variety_id = int(variety["pokemon"]["url"].split("/")[-2])
            processed_varieties.append(variety_id)

        return processed_varieties

    return []


def process_forms(form_data):
    processed_forms = []
    for form in form_data:
        form_name = form["name"]
        if any(pattern in form_name for pattern in EXCLUDED_VARIATION_PATTERNS):
            continue
        form_response = request_with_retry(POKEMON_FORM_URL + form_name)
        if form_response.status_code == 200:
            form_json = form_response.json()
            processed_forms.append({"name": form_name, "id": form_json["id"]})
    return processed_forms


def get_pokemon_sprites(pokemon_id):
    response = request_with_retry(POKEMON_BASE_URL + str(pokemon_id))
    if response.status_code == 200:
        pokemon_data = response.json()
        sprites = pokemon_data.get("sprites", {})
        return {
            "id": pokemon_id,
            "name": pokemon_data["name"],
            "sprites": sprites,
            "forms": pokemon_data.get("forms", []),
        }
    return None


def get_pokemon_form_sprites(form_id):
    response = request_with_retry(POKEMON_FORM_URL + str(form_id))
    if response.status_code == 200:
        form_data = response.json()
        return {
            "id": form_data["id"],
            "name": form_data["name"],
            "sprites": form_data.get("sprites", {}),
        }
    return None


def save_sprites_data(sprites_data):
    with open(
        os.path.join(DATA_SAVE_PATH, SPRITES_FILE), "w", encoding="utf-8"
    ) as file:
        json.dump(sprites_data, file, ensure_ascii=False, indent=4)


def main():
    os.makedirs(DATA_SAVE_PATH, exist_ok=True)

    response = request_with_retry(POKEMON_BASE_URL)
    total_count = response.json()["count"]

    all_sprites_data = {}
    for i in range(1, total_count + 1):
        species_url = POKEMON_SPECIES_URL + str(i)
        if is_in_first_five_generations(species_url):
            varieties = process_varieties(i)
            for variety_id in varieties:
                pokemon_sprites = get_pokemon_sprites(variety_id)
                if pokemon_sprites:
                    forms_info = process_forms(pokemon_sprites.get("forms", []))
                    pokemon_sprites.pop("forms", None)
                    all_sprites_data[pokemon_sprites["name"]] = pokemon_sprites
                    
                    for form_info in forms_info:
                        form_sprites = get_pokemon_form_sprites(form_info["id"])
                        if form_sprites:
                            if form_info["name"] not in all_sprites_data:
                                form_sprites["sprites"]["versions"] = {
                                    "generation-v": {
                                        "black-white": {
                                            "animated": {
                                                "back_default": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/{form_info['id']}.gif",
                                                "back_female": None,
                                                "back_shiny": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/shiny/{form_info['id']}.gif",
                                                "back_shiny_female": None,
                                                "front_default": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{form_info['id']}.gif",
                                                "front_female": None,
                                                "front_shiny": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/shiny/{form_info['id']}.gif",
                                                "front_shiny_female": None,
                                            },
                                            "back_default": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/{form_info['id']}.png",
                                            "back_female": None,
                                            "back_shiny": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/back/shiny/{form_info['id']}.png",
                                            "back_shiny_female": None,
                                            "front_default": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/{form_info['id']}.png",
                                            "front_female": None,
                                            "front_shiny": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/shiny/{form_info['id']}.png",
                                            "front_shiny_female": None,
                                        }
                                    }
                                }
                                all_sprites_data[form_info["name"]] = form_sprites

    save_sprites_data(all_sprites_data)


if __name__ == "__main__":
    main()
