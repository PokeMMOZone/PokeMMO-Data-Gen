import requests
import json
import os
import time
from requests.exceptions import SSLError

# Constants
BASE_URL = "https://pokeapi.co/api/v2/nature/"
DATA_SAVE_PATH = "./data/"
OUTPUT_FILE = "natures-data.json"
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the data directory exists
if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)


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


def get_all_natures():
    natures = []
    next_url = BASE_URL  # Start with the initial URL

    while next_url:
        response = request_with_retry(next_url)
        if response.status_code == 200:
            data = response.json()
            natures.extend(data.get("results", []))
            next_url = data.get("next")  # URL for the next page of results
        else:
            print(f"Failed to fetch natures list: HTTP {response.status_code}")
            break

    return [nature["name"] for nature in natures]


def get_nature_data(nature_name):
    response = request_with_retry(f"{BASE_URL}{nature_name}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for nature {nature_name}")
        return None


def process_nature_data(raw_data):
    increased_stat = (
        raw_data.get("increased_stat", {}).get("name")
        if raw_data.get("increased_stat")
        else None
    )
    decreased_stat = (
        raw_data.get("decreased_stat", {}).get("name")
        if raw_data.get("decreased_stat")
        else None
    )
    likes_flavor = (
        raw_data.get("likes_flavor", {}).get("name")
        if raw_data.get("likes_flavor")
        else None
    )
    hates_flavor = (
        raw_data.get("hates_flavor", {}).get("name")
        if raw_data.get("hates_flavor")
        else None
    )

    move_battle_styles = [
        {
            "move_battle_style": preference.get("move_battle_style", {}).get("name"),
            "low_hp_preference": preference.get("low_hp_preference"),
            "high_hp_preference": preference.get("high_hp_preference"),
        }
        for preference in raw_data.get("move_battle_style_preferences", [])
    ]

    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "increased_stat": increased_stat,
        "decreased_stat": decreased_stat,
        "likes_flavor": likes_flavor,
        "hates_flavor": hates_flavor,
        "move_battle_style_preferences": move_battle_styles,
    }
    return processed_data


def save_natures_to_file(natures, filename):
    with open(DATA_SAVE_PATH + filename, "w", encoding="utf-8") as file:
        json.dump(natures, file, ensure_ascii=False, indent=4)


def main():
    all_nature_names = get_all_natures()
    all_natures = {}

    for nature_name in all_nature_names:
        nature_data = get_nature_data(nature_name)
        if nature_data:
            processed_data = process_nature_data(nature_data)
            all_natures[processed_data["name"]] = processed_data

    save_natures_to_file(all_natures, OUTPUT_FILE)


if __name__ == "__main__":
    main()
