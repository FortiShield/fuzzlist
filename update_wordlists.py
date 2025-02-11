import os
import json
import time
from github import Github, RateLimitExceededException

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment

def fetch_repo_files(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    wordlist_files = []
    
    def fetch_files(path=""):
        try:
            contents = repo.get_contents(path)
            while contents:
                content = contents.pop(0)
                if content.type == "dir":
                    contents.extend(repo.get_contents(content.path))  # Handle pagination properly
                elif content.path.endswith(".txt"):
                    wordlist_files.append(content.download_url)
        except RateLimitExceededException:
            print("Rate limit exceeded. Sleeping for 2 minutes...")
            time.sleep(120)
            fetch_files(path)  # Retry after cooldown

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
