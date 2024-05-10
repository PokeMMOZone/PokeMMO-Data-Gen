import requests
import json
import os

# Base URLs for the PokeAPI
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
SPRITES_FILE = "pokemon-sprites.json"


def is_in_first_five_generations(species_url):
    response = requests.get(species_url)
    if response.status_code == 200:
        species_data = response.json()
        generation_url = species_data["generation"]["url"]
        generation_id = int(generation_url.split("/")[-2])
        return 1 <= generation_id <= 5
    return False


def process_varieties(species_id):
    response = requests.get(POKEMON_SPECIES_URL + str(species_id))
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
                    "basculin-white-striped"
                ]
            ):
                continue

            variety_id = int(variety["pokemon"]["url"].split("/")[-2])
            processed_varieties.append(variety_id)

        return processed_varieties

    return []


def get_pokemon_sprites(pokemon_id):
    response = requests.get(POKEMON_BASE_URL + str(pokemon_id))
    if response.status_code == 200:
        pokemon_data = response.json()
        sprites = pokemon_data.get("sprites", {})
        return {"id": pokemon_id, "name": pokemon_data["name"], "sprites": sprites}
    return None


def save_sprites_data(sprites_data):
    with open(
        os.path.join(DATA_SAVE_PATH, SPRITES_FILE), "w", encoding="utf-8"
    ) as file:
        json.dump(sprites_data, file, ensure_ascii=False, indent=4)


def main():
    os.makedirs(DATA_SAVE_PATH, exist_ok=True)

    response = requests.get(POKEMON_BASE_URL)
    total_count = response.json()["count"]

    all_sprites_data = {}
    for i in range(1, total_count + 1):
        species_url = POKEMON_SPECIES_URL + str(i)
        if is_in_first_five_generations(species_url):
            varieties = process_varieties(i)
            for variety_id in varieties:
                pokemon_sprites = get_pokemon_sprites(variety_id)
                if pokemon_sprites:
                    all_sprites_data[pokemon_sprites["name"]] = pokemon_sprites

    save_sprites_data(all_sprites_data)


if __name__ == "__main__":
    main()
