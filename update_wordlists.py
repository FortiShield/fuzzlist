import os
import json
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment

IGNORE_LIST = [
    "SecLists/contents/Miscellaneous",  # Ignore Miscellaneous directory to avoid rate limit
    "Payloads/Flash/xssproject.swf"  # Ignore bad merge file
]

def fetch_repo_files(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    wordlist_files = []
    
    def fetch_files(path=""):
        if any(ignore in path for ignore in IGNORE_LIST):
            return  # Skip ignored paths
        
        contents = repo.get_contents(path)
        for content in contents:
            if content.type == "dir":
                fetch_files(content.path)  # Recursively fetch subdirectories
            elif content.path.endswith(".txt"):
                file_url = content.download_url
                wordlist_files.append(file_url)

    fetch_files()
    return wordlist_files

def generate_sources_json(repo_list, output_file="sources.json"):
    sources = {}
    for repo in repo_list:
        sources[repo] = fetch_repo_files(repo)
    
    with open(output_file, "w") as f:
        json.dump(sources, f, indent=4)

if __name__ == "__main__":
    repo_list = [
        "https://github.com/danielmiessler/SecLists",
        "https://github.com/assetnote/wordlists"
    ]
    generate_sources_json(repo_list)
    print("Generated sources.json")
