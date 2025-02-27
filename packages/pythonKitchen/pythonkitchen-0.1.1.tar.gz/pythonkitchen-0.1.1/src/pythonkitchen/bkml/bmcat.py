from bs4 import BeautifulSoup
import json

def parse_bookmarks_html(html_file_path, output_json_path, icon_url=False):
    """
    Parse a bookmarks HTML file and save the folder structure (with subfolders, URLs, and optional icons) as JSON.

    Parameters:
    - html_file_path (str): Path to the bookmarks HTML file.
    - output_json_path (str): Path to save the JSON output.
    - icon_url (bool): Whether to include the ICON URL in the output. Default is False.
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

            # Check for links (<A> tags) within this <DT> and add them to the current level
            a_tag = dt_tag.find('a')
            if a_tag:
                link_url = a_tag.get('href', '').strip()
                link_title = a_tag.get_text(strip=True)
                link_data = {
                    "link_title": link_title,
                    "url": link_url,
                }
                if icon_url:  # Add icon URL only if icon_url parameter is True
                    link_icon = a_tag.get('icon', '').strip()
                    link_data["icon"] = link_icon if link_icon else None

                folders.append(link_data)

        return folders

    # Parse the top-level <DL>
    folder_structure = parse_dl(top_dl)

    # Save to JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(folder_structure, json_file, indent=2, ensure_ascii=False)

    print(f"Folder structure successfully saved to {output_json_path}")


if __name__ == "__main__":
    bookmarks_file = 'bookmarks.html'  # Replace with the path to your bookmarks file
    output_file = 'folder_structure_with_optional_icons.json'  # Replace with your desired JSON output path
    # Call the function with icon_url set to True to include icons
    parse_bookmarks_html(bookmarks_file, output_file, icon_url=False)
