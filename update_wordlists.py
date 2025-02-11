import os
import json
import requests
import rarfile
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment
DOWNLOAD_DIR = "wordlists"
RAR_DOWNLOAD_PATH = os.path.join(DOWNLOAD_DIR, "wordlists.rar")
EXTRACT_PATH = os.path.join(DOWNLOAD_DIR, "extracted")

IGNORE_LIST = [
    "SecLists/contents/Miscellaneous",  # Ignore Miscellaneous directory to avoid rate limit
    "Payloads/Flash/xssproject.swf"  # Ignore bad merge file
]

def download_rar(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded RAR file to {save_path}")

def extract_rar(rar_path, extract_to):
    with rarfile.RarFile(rar_path, "r") as rf:
        rf.extractall(extract_to)
    print(f"Extracted RAR file to {extract_to}")

def fetch_repo_rar(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    
    rar_files = [file for file in repo.get_contents("") if file.path.endswith(".rar")]
    
    if not rar_files:
        print("No RAR files found in repo.")
        return
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    download_rar(rar_files[0].download_url, RAR_DOWNLOAD_PATH)
    os.makedirs(EXTRACT_PATH, exist_ok=True)
    extract_rar(RAR_DOWNLOAD_PATH, EXTRACT_PATH)

def generate_sources_json(repo_list, output_file="sources.json"):
    sources = {}
    for repo in repo_list:
        fetch_repo_rar(repo)
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
