import subprocess
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_dir = os.path.join(parent_dir, "data")

# Check if the data directory exists
if not os.path.exists(data_dir):
    # Create the data directory if it doesn't exist
    os.makedirs(data_dir)
else:
    # If the data directory exists, remove all files within it
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def run_script(script_path):
    """Runs a Python script at the given path."""
    try:
        result = subprocess.run(
            ["python", script_path], check=True, text=True, capture_output=True
        )
        print(f"Script {script_path} executed successfully.")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in script {script_path}: {e}")


# List of scripts to run
scripts_to_run = [
    os.path.join(current_dir, "generate_obtainable_pokemon.py"),
    os.path.join(current_dir, "generate_pokemon_moves.py"),
    os.path.join(current_dir, "generate_locations.py"),
    # os.path.join(current_dir, "generate_pvp_data_Input.py"), Removed cause there seems to be a regression in the exportable data.
    os.path.join(current_dir, "download_PokeAPI_pokemon.py"),
    os.path.join(current_dir, "download_PokeAPI_egg-group.py"),
    os.path.join(current_dir, "download_PokeAPI_moves.py"),
    os.path.join(current_dir, "generate_PokeMMO_items.py"),
    os.path.join(current_dir, "generate_egg_moves.py"),
    os.path.join(current_dir, "download_PokeAPI_abilities.py"),
    os.path.join(current_dir, "patch_data_files.py"),
    os.path.join(current_dir, "add_pokemon_to_moves.py"),
    os.path.join(current_dir, "add_pokemon_to_abilities.py"),
    os.path.join(current_dir, "add_pvp_to_pokemon.py"),
    os.path.join(current_dir, "generate_pvp_data.py"),
    os.path.join(current_dir, "generate_types_data.py"),
    os.path.join(current_dir, "generate_location_data.py"),
    os.path.join(current_dir, "generate_location_rarities.py"),
    os.path.join(current_dir, "generate_location_regions.py"),
    os.path.join(current_dir, "generate_location_types.py"),
    os.path.join(current_dir, "generate_obtainable_data.py"),
    os.path.join(current_dir, "generate_held_items.py"),
    os.path.join(current_dir, "download_PokeAPI_natures.py"),
    os.path.join(current_dir, "generate_gender_rates.py"),
    os.path.join(current_dir, "download_PokeAPI_sprites.py"),
]

for script in scripts_to_run:
    run_script(script)
