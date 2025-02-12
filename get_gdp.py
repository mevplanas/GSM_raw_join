import os
import json
import geopandas as gpd
from shapely.geometry import shape
from tqdm import tqdm

# Base folder containing the numbered folders
base_folder = 'Z:\VGTU2024'  # Replace with the actual path

# Prepare a list to store all features
features_list = []

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
                
                # Process each feature
                for feature in data['features']:
                    geometry = shape(feature['geometry'])  # Convert GeoJSON geometry to shapely
                    properties = feature['properties']
                    properties['street_code'] = first_folder
                    properties['street_line'] = street_line
                    
                    # Append the geometry and properties as a tuple
                    features_list.append({
                        'geometry': geometry,
                        'properties': properties
                    })
        else:
            print(f"Suliniai.json not found in {json_folder_path}")

# Convert to GeoDataFrame
geometries = [item['geometry'] for item in features_list]
properties = [item['properties'] for item in features_list]
gdf = gpd.GeoDataFrame(properties, geometry=geometries, crs="EPSG:3346")

# Save to .gdb file
output_gdb_path = 'output_plysiai.gdb'
layer_name = 'combined_features'
gdf.to_file(output_gdb_path, layer=layer_name, driver='FileGDB')

print(f"Data has been saved to the file geodatabase at {output_gdb_path}, layer {layer_name}")
