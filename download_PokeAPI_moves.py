import requests
import json
import os
import time
from requests.exceptions import SSLError

# Constants
BASE_URL = "https://pokeapi.co/api/v2/move/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "moves-data.json"
current_dir = os.path.dirname(os.path.abspath(__file__))
info_directory = os.path.join(current_dir, "dump/info")
skills_file = os.path.join(info_directory, "skills.json")


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


def load_skills():
    with open(skills_file, "r", encoding="utf-8") as file:
        return json.load(file)


def get_skill_data_by_id(move_id, skills):
    # Assuming each skill in skills.json is a dictionary with an "id" key
    for skill in skills:
        if skill["id"] == move_id:
            return skill
    return None


def get_all_moves():
    moves = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = request_with_retry(next_url)
        if response.status_code == 200:
            data = response.json()
            moves.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch moves list: HTTP {response.status_code}")
            break

    return [move["name"] for move in moves]


def get_move_data(move_name):
    response = request_with_retry(f"{BASE_URL}{move_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for move {move_name}")
        return None


def is_move_in_generations_1_to_5(move_data):
    generation_name = move_data.get("generation", {}).get("name", "")
    return generation_name in [
        "generation-i",
        "generation-ii",
        "generation-iii",
        "generation-iv",
        "generation-v",
    ]


def process_move_data(raw_data, skills):
    # Skip moves with type 'shadow'
    if raw_data.get("type", {}).get("name") == "shadow":
        return None

    skill_data = get_skill_data_by_id(raw_data.get("id"), skills)
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "accuracy": (
            skill_data["base_accuracy"] if skill_data else raw_data.get("accuracy")
        ),
        "effect_chance": raw_data.get("effect_chance"),
        "pp": skill_data["base_pp"] if skill_data else raw_data.get("pp"),
        "priority": raw_data.get("priority"),
        "power": skill_data["base_power"] if skill_data else raw_data.get("power"),
        "damage_class": raw_data.get("damage_class", {}).get("name"),
        "type": raw_data.get("type", {}).get("name"),
        "effect": (
            raw_data.get("effect_entries")[0].get("short_effect")
            if raw_data.get("effect_entries")
            else None
        ),
    }
    return processed_data


def save_moves_to_file(moves, filename):
    with open(DATA_SAVE_PATH + filename, "w", encoding="utf-8") as file:
        json.dump(moves, file, ensure_ascii=False, indent=4)


def main():
    skills = load_skills()  # Load the skills from the file
    all_move_names = get_all_moves()
    all_moves = {}

    for move_name in all_move_names:
        move_data = get_move_data(move_name)
        if move_data and is_move_in_generations_1_to_5(move_data):
            processed_data = process_move_data(move_data, skills)
            if processed_data:  # Add only if processed_data is not None
                all_moves[processed_data["name"]] = processed_data

    save_moves_to_file(all_moves, OUTPUT_FILE)


if __name__ == "__main__":
    main()
