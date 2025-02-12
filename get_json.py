import os
import json
from tqdm import tqdm

# Base folder containing the numbered folders
base_folder = 'Z:\VGTU2024'  # Replace with the actual path

# Prepare a list to store all features
all_features = []

# Get a list of top-level folders that start with a number
top_level_folders = [folder for folder in os.listdir(base_folder) if folder[0].isdigit()]

# Traverse through each numbered folder
for first_folder in tqdm(top_level_folders, desc="Processing top-level folders"):
    first_folder_path = os.path.join(base_folder, first_folder)
    # print(f"Processing folder: {first_folder}")

    # Traverse through each subfolder in the numbered folder
    for subfolder in os.listdir(first_folder_path):
        subfolder_path = os.path.join(first_folder_path, subfolder)
        
        # Path to the JSON folder and Suliniai.json file
        json_folder_path = os.path.join(subfolder_path, 'JSON')
        suliniai_file_path = os.path.join(json_folder_path, 'Suliniai.json')
        
        # Check if Suliniai.json exists
        if os.path.exists(suliniai_file_path):
            # print(f"Found Suliniai.json in {suliniai_file_path}")
            
            # Load the JSON file
            with open(suliniai_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                
                # Extract street_line from the subfolder name
                street_line = subfolder
                
                # Add the street_code and street_line to each feature's properties
                for feature in data['features']:
                    feature['properties']['street_code'] = first_folder
                    feature['properties']['street_line'] = street_line
                    all_features.append(feature)
        else:
            print(f"MakroTekst.json not found in {json_folder_path}")

# print("All folders processed. Compiling data into a single JSON file...")

# Create the final JSON structure
output_data = {
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": "EPSG:3346"
        }
    },
    "features": all_features
}

# Save the combined features to a single JSON file
output_file_path = 'combined_Suliniai.json'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)

print(f"Data from all JSON files have been combined and saved to {output_file_path}")
