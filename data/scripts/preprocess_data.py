import os
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def clean_data(df):
    """
    Cleans the data by performing typical data preprocessing steps like:
    - Dropping null values
    - Dropping duplicates
    - Renaming columns

    Parameters:
        df (DataFrame): The pandas DataFrame to clean.

    Returns:
        DataFrame: The cleaned pandas DataFrame.
    """
    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Rename columns if necessary (example)
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)

    return df

def generate_dynamic_filename(file_path, output_folder, extension="txt"):
    """
    Generates a dynamic filename based on the input file name, appending a timestamp for uniqueness.
    
    Parameters:
        file_path (str): Path to the input file.
        output_folder (str): Path to the folder where processed data will be saved.
        extension (str): Desired file extension for the output file.

    Returns:
        str: The full path of the output file with a dynamic filename.
    """
    # Extract the file name without the extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the dynamic file name
    dynamic_filename = f"{base_name}_processed_{timestamp}.{extension}"

    # Ensure output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Return the full path for the output file
    return os.path.join(output_folder, dynamic_filename)

def preprocess_txt(file_path, output_folder):
    """
    Preprocesses a .txt file by cleaning it and saving the processed version.

    Parameters:
        file_path (str): Path to the raw .txt file.
        output_folder (str): Path to the folder where processed data will be saved.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        # Read the raw text data
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Clean the data (example: strip whitespace and remove empty lines)
        cleaned_lines = [line.strip() for line in lines if line.strip()]

        # Generate a dynamic filename for the processed file
        output_file = generate_dynamic_filename(file_path, output_folder, extension="txt")

        # Save the cleaned data as a new .txt file
        with open(output_file, 'w') as f:
            f.write("\n".join(cleaned_lines))

        print(f"Processed data saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error processing text file: {e}")
        return None

def preprocess_csv(file_path, output_folder):
    """
    Preprocesses a CSV file by cleaning it and saving the processed version.

    Parameters:
        file_path (str): Path to the raw CSV file.
        output_folder (str): Path to the folder where processed data will be saved.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        # Read the raw CSV data
        df = pd.read_csv(file_path)

        # Clean the data
        df_cleaned = clean_data(df)

        # Generate a dynamic filename for the processed file
        output_file = generate_dynamic_filename(file_path, output_folder, extension="csv")

        # Save the cleaned data as a new CSV
        df_cleaned.to_csv(output_file, index=False)

        print(f"Processed data saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return None

def preprocess_json(file_path, output_folder):
    """
    Preprocesses a JSON file by cleaning it and saving the processed version.

    Parameters:
        file_path (str): Path to the raw JSON file.
        output_folder (str): Path to the folder where processed data will be saved.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        # Read the raw JSON data
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Clean the data (example: remove any empty objects)
        cleaned_data = [item for item in data if item]

        # Generate a dynamic filename for the processed file
        output_file = generate_dynamic_filename(file_path, output_folder, extension="json")

        # Save the cleaned data as a new JSON
        with open(output_file, 'w') as f:
            json.dump(cleaned_data, f, indent=4)

        print(f"Processed data saved to {output_file}")
        return output_file
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return None
    except Exception as e:
        print(f"Error processing JSON file: {e}")
        return None

if __name__ == "__main__":
    # Define the raw data folder
    raw_data_folder = "data/raw"
    output_folder = "data/processed"

    # Get all .txt files from the raw data folder
    txt_files = [f for f in os.listdir(raw_data_folder) if f.endswith('.txt')]

    # Process each .txt file
    for txt_file in txt_files:
        txt_path = os.path.join(raw_data_folder, txt_file)
        preprocess_txt(txt_path, output_folder)

    # Example of preprocessing CSV data
    input_csv = "data/raw/sample_data.csv"
    preprocess_csv(input_csv, output_folder)

    # Example of preprocessing JSON data
    input_json = "data/raw/sample_data.json"
    preprocess_json(input_json, output_folder)
