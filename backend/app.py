from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
import pandas as pd
import io

app = FastAPI()

# - A root endpoint that returns a welcome message
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to insightAI backend"
    }

# This endpoint checks the health of the application
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

# This endpoint returns the version of the application
@app.get("/version")
async def get_version():
    return {
        "version": "1.0.0"
    }

# This endpoint allows users to upload CSV files for data ingestion
@app.post("/data/upload")
async def upload_data(file: UploadFile = File(...)):
    try:
        # Read the uploaded file into a pandas DataFrame
        contents = await file.read()
        decoded = contents.decode("utf-8")
        df = pd.read_csv(io.StringIO(decoded))
        # Perform ingestion logic (e.g., save to database or process data)
        return {
            "message": "File uploaded successfully", 
            "columns": df.columns.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
