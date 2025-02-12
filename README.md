# GSM_raw_join
Vilniaus GSM žalių duomenų apjungimas 

requirements:
`pip install geopandas shapely tqdm`


## Scripts Overview

### `get_json.py`
- Reads `Suliniai.json` files.
- Extracts data, adds `street_code` and `street_line` attributes.
- Saves the combined output as `combined_Suliniai.json`.

### `get_5jsons.py`
- Reads `Suliniai.json` files.
- Extracts data, adds `street_code` and `street_line` attributes.
- Saves the combined output as 5 json files.

### `get_gdb.py`
- Reads `Plysiai.json` files.
- Converts geometry to `shapely` format using `geopandas`.
- Saves the processed data as a File Geodatabase (`output_plysiai.gdb`).


## All of these scripts are fit to read plysiai, suliniai, duobes, lopai and other files that are in each streets folder. 

