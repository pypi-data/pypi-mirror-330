import json
import os
import re

# Load JSON files
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def rename_hdri():

    parent_dir = os.path.abspath(os.path.join(__file__,'../..'))
    renamed_json_path = os.path.join(parent_dir, 'textures_renamed.json')
    new_renamed_json_path = os.path.join(parent_dir, 'textures_renamed_new.json')
    renamed_json_data = load_json(renamed_json_path)
    new_renamed_json_data = {'hdri': {}}
    VFX_LIB = os.getenv('VFX_LIB')
    hdri_folder = os.path.join(VFX_LIB, 'hdri')
    for current_file_name, attribs in renamed_json_data['hdri'].items():
        resolution = attribs['resol']
        new_filename = re.sub(r'(_)([^_]+)(_v\d+)([^_a-zA-Z]+)(\.\w+$)', rf'1_{resolution}_\2\3\4\5', current_file_name)
        new_renamed_json_data['hdri'][new_filename]=renamed_json_data['hdri'][current_file_name]
        old_file_path = os.path.join(hdri_folder,current_file_name)
        new_file_path = os.path.join(hdri_folder,new_filename)
        os.rename(old_file_path, new_file_path)

   # with open(new_renamed_json_path, 'w') as json_file:
   #     json.dump(new_renamed_json_data, json_file, indent=4)

def main():
    rename_hdri()

if __name__=='__main__':
    main()
