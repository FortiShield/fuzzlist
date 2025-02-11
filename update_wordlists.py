import os
import json
import requests
import zipfile
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment
DOWNLOAD_DIR = "wordlists"
ZIP_DOWNLOAD_PATH = os.path.join(DOWNLOAD_DIR, "wordlists.zip")
EXTRACT_PATH = os.path.join(DOWNLOAD_DIR, "extracted")

IGNORE_LIST = [
    "SecLists/contents/Miscellaneous",  # Ignore Miscellaneous directory to avoid rate limit
    "Payloads/Flash/xssproject.swf"  # Ignore bad merge file
]

def download_zip(url, save_path):
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded ZIP file to {save_path}")

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_to)
    print(f"Extracted ZIP file to {extract_to}")

def fetch_repo_zip(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    
    contents = repo.get_contents("")
    zip_files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith(".zip"):
            zip_files.append(file_content)
    
    if not zip_files:
        print("No ZIP files found in repo.")
        return
    
    zip_url = zip_files[0].download_url.replace("blob/", "raw/")  # Ensure correct download URL
    download_zip(zip_url, ZIP_DOWNLOAD_PATH)
    os.makedirs(EXTRACT_PATH, exist_ok=True)
    extract_zip(ZIP_DOWNLOAD_PATH, EXTRACT_PATH)

def generate_sources_json(repo_list, output_file="sources.json"):
    sources = {}
    for repo in repo_list:
        fetch_repo_zip(repo)
        sources[repo] = EXTRACT_PATH
    
    with open(output_file, "w") as f:
        json.dump(sources, f, indent=4)

if __name__ == "__main__":
    repo_list = [
        "https://github.com/danielmiessler/SecLists",
        "https://github.com/assetnote/wordlists"
    ]
    generate_sources_json(repo_list)
    print("Generated sources.json")
