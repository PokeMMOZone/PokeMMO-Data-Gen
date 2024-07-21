import json
import os
import xml.etree.ElementTree as ET

# Constants
current_dir = os.path.dirname(os.path.abspath(__file__))
info_directory = os.path.join(current_dir, "dump", "info")
strings_directory = os.path.join(current_dir, "dump", "strings")
DATA_SOURCE_PATH = os.path.join(info_directory, "items.json")  # Path to your items.json file
DATA_SAVE_PATH = "./data/"  # Adjust this path as necessary
OUTPUT_FILE = "item-data.json"  # The output file name

# List of supported languages with corresponding files
languages = ["en", "de", "es", "fr", "it", "ja", "ko", "pl", "pt-BR", "zh-Hant"]

def parse_xml_file(filepath):
    """Parses an XML file and returns a dictionary of string ID to translations."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    translations = {}
    for string in root.findall('string'):
        string_id = string.get('id')
        translations[string_id] = string.text
    return translations

def read_translations():
    """Reads and parses all translation XML files."""
    translations = {lang: {} for lang in languages}
    for lang in languages:
        file_path = os.path.join(strings_directory, f"dump_strings_{lang}.xml")
        if os.path.exists(file_path):
            translations[lang] = parse_xml_file(file_path)
    return translations

def read_json_file(filepath):
    """Reads data from a given JSON file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_item_data(raw_data, translations):
    """Processes and structures item data."""
    name_translations = {lang: {"name": translations[lang].get(str(raw_data["name_string_id"]), "")} for lang in languages}
    desc_translations = {lang: {"effect": translations[lang].get(str(raw_data["desc_string_id"]), "")} for lang in languages}
    
    processed_data = {
        "id": raw_data.get("id"),
        "name": raw_data.get("name"),
        "name_translations": name_translations,
        "effect": raw_data.get("desc"),
        "effect_translations": desc_translations,
        "sprite": raw_data.get("icon_id")
    }
    return processed_data

def save_items_to_file(items, filename):
    """Saves items to a JSON file."""
    if not os.path.exists(DATA_SAVE_PATH):
        os.makedirs(DATA_SAVE_PATH)
    with open(os.path.join(DATA_SAVE_PATH, filename), 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=4)

def main():
    translations = read_translations()
    items = read_json_file(DATA_SOURCE_PATH)
    all_items = {}

    for item in items:
        processed_data = process_item_data(item, translations)
        item_name_key = processed_data["name"].replace(" ", "-").lower()
        all_items[item_name_key] = processed_data

    save_items_to_file(all_items, OUTPUT_FILE)

if __name__ == "__main__":
    main()
