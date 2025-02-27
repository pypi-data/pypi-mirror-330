import os
import csv

# Get the VFX_LIB environment variable
ASSET_INGEST_DIR = os.getenv('ASSET_INGEST_DIR')

# Define the path to the ingest folder
ingest_folder = os.path.join(ASSET_INGEST_DIR, 'textures', 'hdri')

# Function to list HDRIs and create CSV
def list_hdri_files(ingest_folder):
    hdri_files = []

    # Iterate through files in the ingest folder
    for filename in os.listdir(ingest_folder):
        if filename.endswith('.hdr') or filename.endswith('.exr'):
            hdri_files.append(filename)

    return hdri_files

# Generate CSV with file attributes
# Generate CSV with file attributes

def generate_csv(hdri_files):
    csv_data = []
    fieldnames = ['file', 'file_path', 'source', 'scene', 'clouds', 'hour', 'color', 'resol', 'variant']
    for filename in hdri_files:
        file_attributes = {
            'file': filename,
            'file_path': os.path.join(ingest_folder, filename),
            'source': '',
            'scene': '',
            'clouds': '',
            'hour': '',
            'color': '',
            'resol': '',
            'variant': ''
        }
        csv_data.append(file_attributes)

    # Write CSV file
    csv_filename = 'hdri_file_attributes.csv'
    csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"CSV file '{csv_filename}' created successfully.")

# Main function
def main():
    hdri_files = list_hdri_files(ingest_folder)
    generate_csv(hdri_files)

if __name__ == "__main__":
    main()

