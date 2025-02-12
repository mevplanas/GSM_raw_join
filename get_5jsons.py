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

    # Traverse through each subfolder in the numbered folder
    for subfolder in os.listdir(first_folder_path):
        subfolder_path = os.path.join(first_folder_path, subfolder)
        
        # Path to the JSON folder and Suliniai.json file
        json_folder_path = os.path.join(subfolder_path, 'JSON')
        suliniai_file_path = os.path.join(json_folder_path, 'Plysiai.json')
        
        # Check if Suliniai.json exists
        if os.path.exists(suliniai_file_path):
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
            print(f"Plysiai.json not found in {json_folder_path}")

# Function to split the list into chunks
def split_list(data, num_chunks):
    chunk_size = len(data) // num_chunks
    return [data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks - 1)] + [data[(num_chunks - 1) * chunk_size:]]

# Split features into 5 parts
num_files = 5
chunks = split_list(all_features, num_files)

# Save each chunk into a separate JSON file
for i, chunk in enumerate(chunks):
    output_data = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:3346"
            }
        },
        "features": chunk
    }
    output_file_path = f'combined_features_part_{i + 1}.json'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, ensure_ascii=False, indent=4)
    print(f"Part {i + 1} saved to {output_file_path}")

print("Data from all JSON files have been split and saved to multiple files.")
