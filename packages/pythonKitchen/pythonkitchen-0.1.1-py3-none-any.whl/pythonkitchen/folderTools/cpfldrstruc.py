import os
import shutil

def copy_folder_structure(source_dir, destination_dir):
    """
    Recursively copies the folder structure from source_dir to destination_dir without copying the files.
    """
    for root, dirs, files in os.walk(source_dir):
        # Calculate the relative path from the source directory to the current directory being traversed
        relative_path = os.path.relpath(root, source_dir)
        
        # Create the corresponding directory structure in the destination directory
        destination_path = os.path.join(destination_dir, relative_path)
        os.makedirs(destination_path, exist_ok=True)
        
        # Print the directories being created (optional)
        print("Copying directory:", destination_path)
        
    print("Folder structure copied successfully!")

# Example usage:
source_directory = "/Users/suhail/Library/CloudStorage/Dropbox/threeD/courses/29_Cinematic_Lighting_in_Houdini/usd"
destination_directory = "/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/usd"

copy_folder_structure(source_directory, destination_directory)

