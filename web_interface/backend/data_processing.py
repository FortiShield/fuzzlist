import os
import pandas as pd
import json
from pathlib import Path

def clean_data(df):
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)
    return df

def preprocess_csv(file_path, output_folder):
    df = pd.read_csv(file_path)
    df_cleaned = clean_data(df)
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(output_folder, 'processed_data.csv')
    df_cleaned.to_csv(output_file, index=False)
    return output_file

def preprocess_json(file_path, output_folder):
    with open(file_path, 'r') as f:
        data = json.load(f)
    cleaned_data = [item for item in data if item]
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(output_folder, 'processed_data.json')
    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=4)
    return output_file
