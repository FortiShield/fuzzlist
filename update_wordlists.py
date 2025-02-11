import os
import json
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment

def fetch_repo_files(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    wordlist_files = []
    
    def fetch_files(path=""):
        contents = repo.get_contents(path)
        for content in contents:
            if content.type == "dir":
                fetch_files(content.path)  # Recursively fetch subdirectories
            elif content.path.endswith(".txt"):
                file_url = content.download_url
                if "Payloads/Flash/xssproject.swf" not in file_url:  # Ignore bad merge file
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
        "https://github.com/assetnote/wordlists"
    ]
    generate_sources_json(repo_list)
    print("Generated sources.json")
