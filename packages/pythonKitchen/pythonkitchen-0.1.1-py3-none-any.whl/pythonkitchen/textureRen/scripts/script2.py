import os
import json
import shutil
import csv

# Get the VFX_LIB environment variable
ASSET_INGEST_DIR = os.getenv('ASSET_INGEST_DIR')
VFX_LIB = os.getenv('VFX_LIB')

# Define the paths
ingest_folder = os.path.join(ASSET_INGEST_DIR, 'textures', 'hdri')
hdri_folder = os.path.join(VFX_LIB, 'hdri')
parent_dir = os.path.abspath(os.path.join(__file__,'../..'))
renamed_json_path = os.path.join(parent_dir, 'textures_renamed.json')
csv_file_path = './hdri_file_attributes.csv'
hdri_json_path = '../hdri.json'


#load CSV file
def load_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


# Load JSON files
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


# Rename files and update JSON
def rename_files_and_update_json():
    hdri_data = load_csv(csv_file_path)
    json_data = load_json(hdri_json_path)
    naming_codes = load_json('../namingcodes.json')
    renamed_json_data = load_json(renamed_json_path)

    for entry in hdri_data:
                
        old_filename = entry['file']
        old_file_path = entry['file_path']
        source = naming_codes['source'][entry['source']]
        scene = naming_codes['scene'][entry['scene']]
        clouds = naming_codes['clouds'][entry['clouds']]
        hour = naming_codes['hour'][entry['hour']]
        resol = entry['resol']
        color = naming_codes['color'][entry['color']]
        variant = naming_codes['variant'][entry['variant']]
        file_extension = old_filename.split('.')[-1]

        # Generate new file name
        new_filename = f'{source}_{scene}_{clouds}_{hour}_{color}_{variant}.{file_extension}'
        
        # Check if entry already exists in renamed_json_data
        if new_filename not in renamed_json_data['hdri']:
            renamed_json_data['hdri'][new_filename] = {
                'source': source,
                'scene': scene,
                'clouds': clouds,
                'hour': hour,
                'color': color,
                'resol': resol,
                'variant': variant,
                'old_file_name': old_filename
            }
        # Rename the file
        new_file_path = os.path.join(hdri_folder, new_filename)
        shutil.move(old_file_path, new_file_path)


    with open(renamed_json_path, 'w') as json_file:
        json.dump(renamed_json_data, json_file, indent=4)


def main():
    rename_files_and_update_json()

if __name__ == "__main__":
    main()

