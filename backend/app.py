from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
import pandas as pd
import io
from .data_ingestion import clean_and_profile

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
        if file.filename.endswith(".csv"):
            decoded = contents.decode("utf-8")
            df = pd.read_csv(io.StringIO(decoded))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV or Excel file.")
        # Check if the DataFrame is empty
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
        profile = clean_and_profile(df)
        return {
            "message": "File uploaded successfully", 
            "columns": df.columns.tolist(),
            "profile": profile
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
