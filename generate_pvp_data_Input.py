import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
pvp_data_file = os.path.join(current_dir, "pokemon-pvp-data.json")
info_directory = os.path.join(current_dir, "dump/info")
monsters_file = os.path.join(
    info_directory, "monsters.json"
)  # Path to the monsters.json file

# Lookup table for tier name changes
tier_lookup = {
    "Untiered": "UN",
    "Under Used": "UU",
    "Never Used": "NU",
    "Over Used": "OU",
    "Ubers": "UB",
    # Add any additional tier mappings here
}

# Name change lookup
name_change_lookup = {
    "nidoran♀": "nidoran-f",
    "nidoran♂": "nidoran-m",
    "farfetch'd": "farfetchd",
    "mr. mime": "mr-mime",
    "mime jr.": "mime-jr",
    "basculin": "basculin-red-striped",
    "wormadam": "wormadam-plant",
    # Add more name mappings as needed
}

# Custom Pokémon data to be added or override existing entries
custom_pokemon_data = {
    "castform-sunny": {"pvp": [{"tier": "UN"}]},
    "castform-rainy": {"pvp": [{"tier": "UN"}]},
    "castform-snowy": {"pvp": [{"tier": "UN"}]},
    "deoxys-normal": {"pvp": [{"tier": "UB"}]},
    "deoxys-attack": {"pvp": [{"tier": "UB"}]},
    "deoxys-defense": {"pvp": [{"tier": "UB"}]},
    "deoxys-speed": {"pvp": [{"tier": "UB"}]},
    "wormadam-sandy": {"pvp": [{"tier": "UN"}]},
    "wormadam-trash": {"pvp": [{"tier": "UN"}]},
    "rotom-heat": {"pvp": [{"tier": "UU"}]},
    "rotom-wash": {"pvp": [{"tier": "UU"}]},
    "rotom-frost": {"pvp": [{"tier": "UU"}]},
    "rotom-fan": {"pvp": [{"tier": "UU"}]},
    "rotom-mow": {"pvp": [{"tier": "UU"}]},
    "giratina-altered": {"pvp": [{"tier": "UB"}]},
    "giratina-origin": {"pvp": [{"tier": "UB"}]},
    "shaymin-sky": {"pvp": [{"tier": "UB"}]},
    "shaymin-land": {"pvp": [{"tier": "OU"}]},
    "basculin-blue-striped": {"pvp": [{"tier": "UN"}]},
    "darmanitan-standard": {"pvp": [{"tier": "OU"}]},
    "darmanitan-zen": {"pvp": [{"tier": "OU"}]},
    "tornadus-incarnate": {"pvp": [{"tier": "UB"}]},
    "tornadus-therian": {"pvp": [{"tier": "UB"}]},
    "thundurus-incarnate": {"pvp": [{"tier": "UB"}]},
    "thundurus-therian": {"pvp": [{"tier": "UB"}]},
    "landorus-incarnate": {"pvp": [{"tier": "UB"}]},
    "landorus-therian": {"pvp": [{"tier": "UB"}]},
    "kyurem-black": {"pvp": [{"tier": "UB"}]},
    "kyurem-white": {"pvp": [{"tier": "UB"}]},
    "keldeo-ordinary": {"pvp": [{"tier": "UB"}]},
    "keldeo-resolute": {"pvp": [{"tier": "UB"}]},
    "meloetta-aria": {"pvp": [{"tier": "UB"}]},
    "meloetta-pirouette": {"pvp": [{"tier": "UB"}]},
    # Add more custom Pokémon data as needed
}


def generate_pvp_data_json(filepath):
    pvp_data = {}

    # Open the monsters.json file
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

        for pokemon in data:
            # Using the Pokémon's name in lowercase as the key
            pokemon_name = pokemon["name"].lower()

            # Check if the Pokémon's name needs to be changed
            if pokemon_name in name_change_lookup:
                pokemon_name = name_change_lookup[pokemon_name]

            # Extracting the tier information
            tier_info = pokemon.get(
                "tiers", "UN"
            )  # Default to "UN" if tier is not specified
            if isinstance(tier_info, list):
                tier = tier_info[0] if tier_info else "UN"
            else:
                tier = tier_info

            tier = tier_lookup.get(
                tier, "UN"
            )  # Map tier using the lookup table, default to "UN"

            # Constructing the PvP data
            pvp_data[pokemon_name] = {"pvp": [{"tier": tier}]}

    # Merging custom Pokémon data
    for pokemon_name, data in custom_pokemon_data.items():
        pvp_data[pokemon_name] = data

    # Write the compiled PvP data to pokemon-pvp-data.json
    with open(pvp_data_file, "w", encoding="utf-8") as outfile:
        json.dump(pvp_data, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_pvp_data_json(monsters_file)
