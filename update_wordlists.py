import os
import requests
import json
from github import Github

# Load sources from a JSON file
def load_sources(file="sources.json"):
    with open(file, "r") as f:
        return json.load(f)

# Fetch wordlists from GitHub
def fetch_wordlist(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Saved: {save_path}")
    else:
        print(f"Failed to fetch {url}: {response.status_code}")

# Main function to update wordlists
def update_wordlists():
    sources = load_sources()
    os.makedirs("data", exist_ok=True)
    
    for category, urls in sources.items():
        category_path = os.path.join("data", category)
        os.makedirs(category_path, exist_ok=True)
        
        for url in urls:
            filename = url.split("/")[-1]
            save_path = os.path.join(category_path, filename)
            fetch_wordlist(url, save_path)

if __name__ == "__main__":
    update_wordlists()
