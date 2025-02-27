from bs4 import BeautifulSoup
import json

def parse_bookmarks_html(html_file_path, output_json_path):
    """
    Parse a bookmarks HTML file and save the folder structure (with subfolders) as JSON.
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the top-level <DL> element
    top_dl = soup.find('dl')
    if not top_dl:
        print("No <DL> element found in the HTML file.")
        return

    # Recursive function to parse the <DL> structure
    def parse_dl(dl_tag):
        folders = []
        for dt_tag in dl_tag.find_all('dt', recursive=True):  # Iterate over <DT> tags directly inside this <DL>
            h3_tag = dt_tag.find('h3')  # Check if this <DT> contains an <H3> (folder name)
            if h3_tag:
                folder_name = h3_tag.get_text(strip=True)
                # Find nested <DL> under this <DT> (subfolder structure)
                sub_dl_tag = dt_tag.find('dl')
                subfolders = parse_dl(sub_dl_tag) if sub_dl_tag else []

                folders.append({
                    "folder_name": folder_name,
                    "subfolders": subfolders
                })
        return folders

    # Parse the top-level <DL>
    folder_structure = parse_dl(top_dl)

    # Save to JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(folder_structure, json_file, indent=2, ensure_ascii=False)

    print(f"Folder structure successfully saved to {output_json_path}")


if __name__ == "__main__":
    bookmarks_file = 'bookmarks.html'  # Replace with the path to your bookmarks file
    output_file = 'folder_structure.json'  # Replace with your desired JSON output path
    parse_bookmarks_html(bookmarks_file, output_file)
