import requests
import json
import os
import time
from requests.exceptions import SSLError

# Base URLs for the PokeAPI
current_dir = os.path.dirname(os.path.abspath(__file__))
POKEMON_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_FORM_URL = "https://pokeapi.co/api/v2/pokemon-form/"
POKEMON_SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species/"
DATA_SAVE_PATH = "./data/"
ALL_POKEMON_FILE = "pokemon-data.json"
LOCATIONS_FILE = os.path.join(current_dir, "locations.json")
SHINYTIERS_FILE = os.path.join(current_dir, "shiny-tiers.json")
MOVES_FILE = os.path.join(current_dir, "pokemon_moves.json")  # Path to the moves file
OBTAINABLE_FILE = os.path.join(current_dir, "obtainable_pokemon.json")
egg_moves_database = {}

# Lookup table to map API egg group names to PokéMMO egg group names
EGG_GROUP_NAME_LOOKUP = {
    "monster": "monster",
    "water1": "watera",
    "water2": "waterb",
    "water3": "waterc",
    "bug": "bug",
    "flying": "flying",
    "ground": "field",
    "fairy": "fairy",
    "plant": "plant",
    "humanshape": "humanoid",
    "mineral": "mineral",
    "ditto": "ditto",
    "dragon": "dragon",
    "no-eggs": "cannot-breed",
    "indeterminate": "chaos",
    # Add any other egg groups that PokéMMO uses which aren't listed in the PokeAPI
}

alpha_list = [
    "bulbasaur",
    "ivysaur",
    "venusaur",
    "charmander",
    "charmeleon",
    "charizard",
    "squirtle",
    "wartortle",
    "blastoise",
    "caterpie",
    "metapod",
    "butterfree",
    "pidgey",
    "pidgeotto",
    "pidgeot",
    "rattata",
    "raticate",
    "spearow",
    "fearow",
    "ekans",
    "arbok",
    "pikachu",
    "raichu",
    "sandshrew",
    "sandslash",
    "nidoran-f",
    "nidorina",
    "nidoqueen",
    "nidoran-m",
    "nidorino",
    "nidoking",
    "clefairy",
    "clefable",
    "vulpix",
    "ninetales",
    "jigglypuff",
    "wigglytuff",
    "zubat",
    "golbat",
    "paras",
    "parasect",
    "venonat",
    "venomoth",
    "meowth",
    "persian",
    "psyduck",
    "golduck",
    "growlithe",
    "arcanine",
    "poliwag",
    "poliwhirl",
    "poliwrath",
    "bellsprout",
    "weepinbell",
    "victreebel",
    "tentacool",
    "tentacruel",
    "geodude",
    "graveler",
    "golem",
    "ponyta",
    "rapidash",
    "magnemite",
    "magneton",
    "seel",
    "dewgong",
    "shellder",
    "cloyster",
    "gastly",
    "haunter",
    "gengar",
    "onix",
    "drowzee",
    "hypno",
    "krabby",
    "kingler",
    "voltorb",
    "electrode",
    "cubone",
    "marowak",
    "lickitung",
    "rhyhorn",
    "rhydon",
    "chansey",
    "kangaskhan",
    "horsea",
    "seadra",
    "staryu",
    "starmie",
    "jynx",
    "electabuzz",
    "magmar",
    "pinsir",
    "tauros",
    "magikarp",
    "gyarados",
    "lapras",
    "ditto",
    "eevee",
    "vaporeon",
    "jolteon",
    "flareon",
    "dratini",
    "dragonair",
    "dragonite",
    "hoothoot",
    "noctowl",
    "ledyba",
    "ledian",
    "spinarak",
    "ariados",
    "crobat",
    "pichu",
    "cleffa",
    "igglybuff",
    "natu",
    "xatu",
    "mareep",
    "flaaffy",
    "ampharos",
    "marill",
    "azumarill",
    "sudowoodo",
    "politoed",
    "aipom",
    "sunkern",
    "sunflora",
    "yanma",
    "wooper",
    "quagsire",
    "espeon",
    "umbreon",
    "murkrow",
    "misdreavus",
    "pineco",
    "forretress",
    "gligar",
    "steelix",
    "snubbull",
    "granbull",
    "qwilfish",
    "sneasel",
    "teddiursa",
    "ursaring",
    "swinub",
    "piloswine",
    "corsola",
    "delibird",
    "mantine",
    "houndour",
    "houndoom",
    "kingdra",
    "stantler",
    "smoochum",
    "elekid",
    "magby",
    "miltank",
    "blissey",
    "larvitar",
    "pupitar",
    "tyranitar",
    "poochyena",
    "mightyena",
    "zigzagoon",
    "linoone",
    "wingull",
    "pelipper",
    "ralts",
    "kirlia",
    "gardevoir",
    "shroomish",
    "breloom",
    "slakoth",
    "vigoroth",
    "slaking",
    "whismur",
    "loudred",
    "exploud",
    "makuhita",
    "hariyama",
    "azurill",
    "sableye",
    "aron",
    "lairon",
    "aggron",
    "plusle",
    "minun",
    "roselia",
    "carvanha",
    "sharpedo",
    "spoink",
    "grumpig",
    "spinda",
    "swablu",
    "altaria",
    "seviper",
    "corphish",
    "crawdaunt",
    "feebas",
    "milotic",
    "shuppet",
    "banette",
    "duskull",
    "dusclops",
    "tropius",
    "snorunt",
    "glalie",
    "spheal",
    "sealeo",
    "walrein",
    "bagon",
    "shelgon",
    "salamence",
    "starly",
    "staravia",
    "staraptor",
    "shinx",
    "luxio",
    "luxray",
    "budew",
    "roserade",
    "buizel",
    "floatzel",
    "ambipom",
    "drifloon",
    "drifblim",
    "buneary",
    "lopunny",
    "mismagius",
    "honchkrow",
    "glameow",
    "purugly",
    "stunky",
    "skuntank",
    "bronzor",
    "bronzong",
    "bonsly",
    "happiny",
    "spiritomb",
    "gible",
    "gabite",
    "garchomp",
    "riolu",
    "lucario",
    "skorupi",
    "drapion",
    "mantyke",
    "snover",
    "abomasnow",
    "weavile",
    "magnezone",
    "lickilicky",
    "rhyperior",
    "electivire",
    "magmortar",
    "yanmega",
    "leafeon",
    "glaceon",
    "gliscor",
    "mamoswine",
    "gallade",
    "dusknoir",
    "froslass",
    "patrat",
    "watchog",
    "lillipup",
    "herdier",
    "stoutland",
    "munna",
    "musharna",
    "blitzle",
    "zebstrika",
    "drilbur",
    "excadrill",
    "cottonee",
    "whimsicott",
    "sandile",
    "krokorok",
    "krookodile",
    "zorua",
    "zoroark",
    "minccino",
    "cinccino",
    "vanillite",
    "vanillish",
    "vanilluxe",
    "foongus",
    "amoonguss",
    "litwick",
    "lampent",
    "chandelure",
    "cubchoo",
    "beartic",
    "cryogonal",
    "rufflet",
    "braviary",
    "golett",
    "golurk",
    "vullaby",
    "mandibuzz",
    "venipede",
    "whirlipede",
    "scolipede",
    "suicune",
    "tangela",
    "tangrowth"
]

egg_group_updates = {
    "shedinja": ["cannot-breed"],
    "nidorina": ["monster", "field"],
    "nidoqueen": ["monster", "field"],
    # Add more Pokémon and their updated egg groups here
}


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


def get_evolution_chain_data(evolution_chain_url):
    response = request_with_retry(evolution_chain_url)
    if response.status_code == 200:
        evolution_chain_data = response.json()
        process_evolution_chain(evolution_chain_data["chain"])
        remove_urls(evolution_chain_data)
        del evolution_chain_data["chain"]["evolution_details"]
        return evolution_chain_data
    return None


def get_pokemon_generation(species_id):
    response = request_with_retry(POKEMON_SPECIES_URL + str(species_id))
    if response.status_code == 200:
        species_data = response.json()
        generation_url = species_data["generation"]["url"]
        generation_id = int(generation_url.split("/")[-2])
        return generation_id
    return None


def process_evolution_chain(chain):
    if "species" in chain:
        species_url = chain["species"].get("url")
        if species_url:
            species_id = int(species_url.split("/")[-2])
            generation_id = get_pokemon_generation(species_id)
            if generation_id is not None and generation_id <= 5:
                chain["species"]["id"] = species_id
                del chain["species"]["url"]
            else:
                return  # Skip processing if the Pokémon is not from Gen 1-5

    if "evolves_to" in chain:
        filtered_evolves_to = []
        for evolves_to in chain["evolves_to"]:
            species_url = evolves_to["species"].get("url")
            if species_url:
                species_id = int(species_url.split("/")[-2])
                generation_id = get_pokemon_generation(species_id)
                if generation_id is not None and generation_id <= 5:
                    process_evolution_chain(
                        evolves_to
                    )  # Recursively process the next evolution
                    filtered_evolves_to.append(evolves_to)
        chain["evolves_to"] = filtered_evolves_to  # Update with filtered evolutions


def process_pokemon_egg_moves(pokemon_name, moves):
    """Process egg moves for a given Pokémon and update the database."""
    egg_moves = [move for move in moves if move["type"] == "EGG"]
    if egg_moves:
        egg_moves_database[pokemon_name] = egg_moves


def add_egg_moves_to_evolutions(all_pokemon_data, pokemon_name, egg_moves):
    """Add egg moves to the evolutions of a given Pokémon if they don't have them."""
    updates = {}  # Initialize an empty dictionary to store updates

    if pokemon_name in all_pokemon_data:
        # Extract the top-level evolution data
        evolution_chain_data = all_pokemon_data[pokemon_name].get("evolution_chain", {})

        # Traverse the evolution chain to find evolved forms
        current_stage = evolution_chain_data.get("chain", {})
        while current_stage:
            evolves_to = current_stage.get("evolves_to", [])
            for evolution in evolves_to:
                species_data = evolution.get("species", {})
                evolution_name = species_data.get("name")
                if evolution_name in all_pokemon_data:
                    evolution_moves = all_pokemon_data[evolution_name].get("moves", [])
                    existing_egg_move_ids = {
                        move["id"]
                        for move in evolution_moves
                        if move["type"] == "EGG"
                    }
                    new_egg_moves = [
                        move
                        for move in egg_moves
                        if move["id"] not in existing_egg_move_ids
                    ]
                    if new_egg_moves:
                        updates[evolution_name] = evolution_moves + new_egg_moves

            # Go to the next stage in the chain
            if len(evolves_to) > 0:
                current_stage = evolves_to[0]
            else:
                break

    return updates


def process_held_items(held_items):
    processed_items = []
    for item in held_items:
        item_id = int(item["item"]["url"].split("/")[-2])
        processed_items.append(
            {
                "id": item_id,
                "item_name": item["item"]["name"],
            }
        )
    return processed_items


def remove_urls(dictionary):
    for key, value in list(dictionary.items()):
        if isinstance(value, dict):
            if "url" in value:
                del value["url"]  # Remove the URL from the dictionary
            else:
                remove_urls(
                    value
                )  # Recursively call remove_urls on nested dictionaries
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    if "url" in item:
                        del item[
                            "url"
                        ]  # Remove the URL from the dictionary within the list
                    else:
                        remove_urls(
                            item
                        )  # Recursively call remove_urls on dictionaries within the list


def is_in_first_five_generations(generation_url):
    generation_id = int(generation_url.split("/")[-2])
    return 1 <= generation_id <= 5


def process_egg_groups(egg_groups):
    return [
        EGG_GROUP_NAME_LOOKUP.get(group["name"], group["name"]) for group in egg_groups
    ]


def update_egg_groups(all_pokemon_data, egg_group_updates):
    for pokemon_name, new_egg_groups in egg_group_updates.items():
        if pokemon_name in all_pokemon_data:
            all_pokemon_data[pokemon_name]["egg_groups"] = new_egg_groups


def process_growth_rate(growth_rate):
    return growth_rate["name"]


def process_stats(stats):
    return [
        {
            "stat_name": stat["stat"]["name"],
            "base_stat": stat["base_stat"],
            "effort": stat["effort"],
        }
        for stat in stats
    ]


def process_types(types):
    return [type_entry["type"]["name"] for type_entry in types]


def process_past_types(pokemon_data):
    if "past_types" in pokemon_data and pokemon_data["past_types"]:
        for past_type_entry in pokemon_data["past_types"]:
            # Check if the generation is Generation 5
            if past_type_entry["generation"]["name"] == "generation-v":
                processed_types = [
                    type_entry["type"]["name"]
                    for type_entry in past_type_entry["types"]
                ]
                if processed_types:
                    pokemon_data["types"] = processed_types
                    break  # Stop processing after finding Generation 5 types


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
    "sawsbuck-spring"
]

def process_varieties(species_id):
    response = request_with_retry(POKEMON_SPECIES_URL + str(species_id))
    if response.status_code == 200:
        species_data = response.json()
        varieties = species_data["varieties"]

        processed_varieties = []
        for variety in varieties:
            name = variety["pokemon"]["name"]
            if any(pattern in name for pattern in EXCLUDED_VARIATION_PATTERNS):
                continue

            variety_id = int(variety["pokemon"]["url"].split("/")[-2])
            processed_varieties.append(
                {"name": name, "id": variety_id, "is_default": variety["is_default"]}
            )

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


def process_abilities(abilities):
    return [
        {
            "id": int(
                ability["ability"]["url"].split("/")[-2]
            ),  # Extracting the ID from the URL
            "ability_name": ability["ability"]["name"],
            "is_hidden": ability["is_hidden"],
            "slot": ability["slot"],
        }
        for ability in abilities
    ]


def process_name_translations(names):
    translations = {}
    for name_entry in names:
        language_name = name_entry["language"]["name"]
        translations[language_name] = {"name": name_entry["name"]}
    return translations


def save_all_data(all_data):
    with open(DATA_SAVE_PATH + ALL_POKEMON_FILE, "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)


def read_locations():
    with open(LOCATIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def read_shiny_tiers():
    with open(SHINYTIERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def read_moves():
    with open(MOVES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def read_obtainable_pokemon():
    with open(OBTAINABLE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_unique_moves(moves_data):
    unique_moves = set()
    for pokemon, data in moves_data.items():
        for move in data["moves"]:
            unique_moves.add((move["name"], move["id"]))
    return unique_moves


def main():
    all_pokemon_data = {}
    locations_data = read_locations()
    shiny_tiers_data = read_shiny_tiers()
    moves_data = read_moves()
    obtainable_pokemon = read_obtainable_pokemon()

    response = request_with_retry(POKEMON_BASE_URL)
    total_count = response.json()["count"]

    for i in range(1, total_count + 1):
        species_response = request_with_retry(POKEMON_SPECIES_URL + str(i))
        if species_response.status_code == 200:
            species_data = species_response.json()

            if not is_in_first_five_generations(species_data["generation"]["url"]):
                continue

            species_data.pop("flavor_text_entries", None)  # Remove unwanted fields
            species_data.pop("genera", None)
            species_data.pop("generation", None)
            species_data.pop("habitat", None)
            species_data.pop("pal_park_encounters", None)
            species_data.pop("pokedex_numbers", None)
            species_data.pop("color", None)
            species_data.pop("form_descriptions", None)
            species_data.pop("shape", None)
            species_data["egg_groups"] = process_egg_groups(species_data["egg_groups"])
            species_data["growth_rate"] = process_growth_rate(
                species_data["growth_rate"]
            )

            # Process name translations
            species_data["name_translations"] = process_name_translations(
                species_data["names"]
            )
            species_data.pop("names", None)  # Remove the 'names' key after processing

            # Set 'alpha' field
            pokemon_name = species_data["name"].lower()
            species_data["alpha"] = "yes" if pokemon_name in alpha_list else "no"
            species_data["obtainable"] = obtainable_pokemon.get(pokemon_name, {}).get(
                "obtainable", False
            )

            evolution_chain_url = species_data.get("evolution_chain", {}).get("url")
            if evolution_chain_url:
                evolution_chain_data = get_evolution_chain_data(evolution_chain_url)
                species_data["evolution_chain"] = evolution_chain_data

            varieties = process_varieties(i)  # Process varieties for the species
            for variety in varieties:
                variety_id = variety["id"]
                variety_name = variety["name"]
                pokemon_response = request_with_retry(
                    POKEMON_BASE_URL + str(variety_id)
                )
                if pokemon_response.status_code == 200:
                    pokemon_data = pokemon_response.json()
                    pokemon_name = pokemon_data["name"]

                    if "held_items" in pokemon_data:
                        pokemon_data["held_items"] = process_held_items(
                            pokemon_data["held_items"]
                        )

                    if "sprites" in pokemon_data:
                        pokemon_data["sprites"].pop("versions", None)
                        pokemon_data["sprites"].pop("other", None)

                    # Process stats and types
                    if "stats" in pokemon_data:
                        pokemon_data["stats"] = process_stats(pokemon_data["stats"])
                    if "types" in pokemon_data:
                        pokemon_data["types"] = process_types(pokemon_data["types"])
                    if "abilities" in pokemon_data:
                        pokemon_data["abilities"] = process_abilities(
                            pokemon_data["abilities"]
                        )
                    if "forms" in pokemon_data:
                        pokemon_data["forms"] = process_forms(pokemon_data["forms"])

                    process_past_types(pokemon_data)

                    pokemon_data.pop("game_indices", None)
                    pokemon_data.pop("location_area_encounters", None)
                    pokemon_data.pop("moves", None)
                    pokemon_data.pop("height", None)
                    pokemon_data.pop("weight", None)
                    pokemon_data.pop("past_types", None)
                    pokemon_data.pop("past_abilities", None)

                    pokemon_name = species_data["name"]
                    if pokemon_name in locations_data:
                        species_data["location_area_encounters"] = locations_data[
                            pokemon_name
                        ]["locations"]
                    if pokemon_name in moves_data:
                        species_data["moves"] = moves_data[pokemon_name]["moves"]
                    if pokemon_name in moves_data:
                        process_pokemon_egg_moves(
                            pokemon_name, moves_data[pokemon_name]["moves"]
                        )
                    if pokemon_name in shiny_tiers_data:
                        species_data.update(shiny_tiers_data[pokemon_name])

                    remove_urls(species_data)
                    remove_urls(pokemon_data)

                    # Merge species data with pokemon data for the specific variety
                    merged_data = {**species_data, **pokemon_data}
                    merged_data["varieties"] = varieties
                    merged_data.pop(
                        "species", None
                    )  # Remove the 'species' key from merged data
                    # merged_data.pop("forms", None)

                    # Store the data for this variety in the main dictionary
                    all_pokemon_data[variety_name] = merged_data

                    # Now process forms for the variety
                    forms_info = process_forms(merged_data.get("forms", []))
                    for form_info in forms_info:
                        form_name = form_info["name"]
                        if form_name not in all_pokemon_data:
                            form_response = request_with_retry(POKEMON_FORM_URL + str(form_info["id"]))
                            if form_response.status_code == 200:
                                form_data = form_response.json()
                                form_data.pop("moves", None)
                                if "types" in form_data:
                                    form_data["types"] = process_types(form_data["types"])
                                remove_urls(form_data)
                                merged_form_data = {**species_data, **form_data}
                                merged_form_data["varieties"] = varieties
                                merged_form_data.pop("species", None)
                                merged_form_data.pop("form_order", None)
                                merged_form_data.pop("form_names", None)
                                merged_form_data.pop("form_name", None)
                                merged_form_data.pop("names", None)
                                merged_form_data.pop("pokemon", None)
                                merged_form_data.pop("version_group", None)
                                merged_form_data.pop("is_battle_only", None)
                                merged_form_data.pop("is_default", None)
                                merged_form_data.pop("is_mega", None)
                                all_pokemon_data[form_name] = merged_form_data

    all_unique_moves = get_all_unique_moves(all_pokemon_data)

    smeargle_moves = [
        {"id": move_id, "name": move_name, "type": "sketch"}
        for move_name, move_id in all_unique_moves
    ]

    # Sort Smeargle's moves by their ID to maintain consistent order
    smeargle_moves.sort(key=lambda move: move["id"])

    # Check if Smeargle is in all_pokemon_data
    if "smeargle" not in all_pokemon_data:
        all_pokemon_data["smeargle"] = {"name": "smeargle", "moves": []}

    # Retrieve Smeargle's existing moves
    existing_smeargle_moves = all_pokemon_data["smeargle"].get("moves", [])

    # Merge unique moves with existing ones, avoiding duplicates
    existing_move_names = {move["name"] for move in existing_smeargle_moves}
    merged_moves = existing_smeargle_moves + [
        move for move in smeargle_moves if move["name"] not in existing_move_names
    ]

    # Update Smeargle's moves in all_pokemon_data
    all_pokemon_data["smeargle"]["moves"] = merged_moves

    # Add egg moves to evolutions and merge updates
    for pokemon_name, egg_moves in egg_moves_database.items():
        updates = add_egg_moves_to_evolutions(all_pokemon_data, pokemon_name, egg_moves)
        # Apply the updates to all_pokemon_data
        for evolution_name, moves in updates.items():
            all_pokemon_data[evolution_name]["moves"] = moves

    update_egg_groups(all_pokemon_data, egg_group_updates)

    save_all_data(all_pokemon_data)


if __name__ == "__main__":
    main()
