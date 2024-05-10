import json
import os


def read_pokemon_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_obtainable_data(pokemon_data):
    obtainable_data = {"true": [], "false": []}
    for pokemon, data in pokemon_data.items():
        obtainable = data.get("obtainable", False)
        key = "true" if obtainable else "false"
        # Include both name and ID in the appended data
        obtainable_data[key].append({"name": pokemon, "id": data["id"]})
    return obtainable_data


def save_obtainable_data(obtainable_data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(obtainable_data, file, ensure_ascii=False, indent=4)


def main():
    data_save_path = "./data/"
    input_file = "pokemon-data.json"
    output_file = "obtainable-data.json"

    # Read the Pokémon data
    pokemon_data_path = os.path.join(data_save_path, input_file)
    pokemon_data = read_pokemon_data(pokemon_data_path)

    # Generate obtainable data
    obtainable_data = generate_obtainable_data(pokemon_data)

    # Save the obtainable data to a JSON file
    obtainable_data_path = os.path.join(data_save_path, output_file)
    save_obtainable_data(obtainable_data, obtainable_data_path)

    print(f"Obtainable data saved to {obtainable_data_path}")


if __name__ == "__main__":
    main()
