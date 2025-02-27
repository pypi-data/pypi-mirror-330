import json
import requests
from urllib.parse import urlparse
import os

def extract_domains(bookmarks):
    """
    Extracts unique domains from a nested bookmarks JSON structure.
    
    Args:
        bookmarks (dict or list): The JSON structure of bookmarks.
    
    Returns:
        set: A set of unique domains.
    """
    domains = set()
    
    def traverse_bookmarks(data):
        if isinstance(data, dict):
            if "url" in data:
                domain = urlparse(data["url"]).netloc
                if domain:
                    domains.add(domain)
            if "subfolders" in data:
                traverse_bookmarks(data["subfolders"])
        elif isinstance(data, list):
            for item in data:
                traverse_bookmarks(item)
    
    traverse_bookmarks(bookmarks)
    return domains


def fetch_svg_icons(domains, output_dir="icons"):
    """
    Fetch SVG icons for a list of domains and save them to a directory.
    
    Args:
        domains (set): A set of domains.
        output_dir (str): Directory to save the downloaded SVG icons.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_icons = []
    
    for domain in domains:
        try:
            # Construct a probable SVG icon URL
            icon_url = f"https://{domain}/favicon.svg"
            response = requests.get(icon_url, timeout=10)
            if response.status_code == 200 and "image/svg+xml" in response.headers.get("Content-Type", ""):
                file_name = os.path.join(output_dir, f"{domain.replace('.', '_')}.svg")
                with open(file_name, "wb") as f:
                    f.write(response.content)
                saved_icons.append(file_name)
                print(f"Saved SVG icon for {domain} at {file_name}")
            else:
                print(f"No SVG icon found for {domain}")
        except Exception as e:
            print(f"Error fetching icon for {domain}: {e}")
    
    return saved_icons


if __name__ == "__main__":
    # Load the JSON data
    with open("bookmarks.json", "r", encoding="utf-8") as f:
        bookmarks_data = json.load(f)
    
    # Step 1: Extract unique domains
    unique_domains = extract_domains(bookmarks_data)
    print(f"Found {len(unique_domains)} unique domains.")
    
    # Step 2: Fetch SVG icons
    icons = fetch_svg_icons(unique_domains)
    print(f"Downloaded {len(icons)} SVG icons.")
