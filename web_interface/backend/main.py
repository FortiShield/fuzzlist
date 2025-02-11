from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from data_processing import preprocess_csv, preprocess_json
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or restrict it to specific ones
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Path where processed files will be saved
output_folder = "data/processed"

@app.post("/upload/csv/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and preprocess a CSV file.
    Returns the path to the processed CSV file.
    """
    try:
        # Save the uploaded file to the server
        file_location = os.path.join("data/raw", file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Process the uploaded CSV file
        processed_file = preprocess_csv(file_location, output_folder)
        return {"processed_file": processed_file}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/json/")
async def upload_json(file: UploadFile = File(...)):
    """
    Upload and preprocess a JSON file.
    Returns the path to the processed JSON file.
    """
    try:
        # Save the uploaded file to the server
        file_location = os.path.join("data/raw", file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Process the uploaded JSON file
        processed_file = preprocess_json(file_location, output_folder)
        return {"processed_file": processed_file}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Allows the user to download the processed file.
    """
    file_path = os.path.join(output_folder, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")
