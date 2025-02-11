import os
import requests
import yaml
from pathlib import Path

def load_data_sources(file_path):
    """
    Loads the list of data sources from a YAML file.
    
    Parameters:
        file_path (str): Path to the YAML file containing data sources.
        
    Returns:
        list: List of data source dictionaries.
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('data_sources', [])

def download_file(url, destination_folder):
    """
    Downloads a file from a URL and saves it to the destination folder.

    Parameters:
        url (str): The URL to download the file from.
        destination_folder (str): The folder where the file should be saved.
    """
    # Ensure the destination folder exists
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    
    # Extract the filename from the URL
    filename = url.split("/")[-1]
    destination_path = os.path.join(destination_folder, filename)

    # Check if file already exists
    if os.path.exists(destination_path):
        print(f"File '{filename}' already exists. Skipping download.")
        return destination_path

    print(f"Downloading {filename}...")

    # Download the file in chunks and write it to the destination
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we got a successful response

    with open(destination_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded {filename} to {destination_path}")
    return destination_path

if __name__ == "__main__":
    # Load data sources from the config directory
    data_source_file = 'data/config/data_sources.yml'  # Update the path
    sources = load_data_sources(data_source_file)

    # Loop through each data source and download
    for source in sources:
        url = source['url']
        destination_folder = source['destination']  # Use the destination from YAML
        print(f"Downloading from {url} to {destination_folder}...")

        # Download file to the specified destination
        download_file(url, destination_folder)
