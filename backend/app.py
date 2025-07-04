from datetime import datetime
import json
from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
import pandas as pd
import io
from sqlalchemy.orm import Session

from .data_ingestion import clean_and_profile
from .database import engine, SessionLocal
from .models import Base, DatasetMetadata

app = FastAPI()

# Create tables in DB if they don't exist
Base.metadata.create_all(bind=engine)

# - A root endpoint that returns a welcome message
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to insightAI backend"
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

        # Save metadata to DB
        db: Session = SessionLocal()
        metadata = DatasetMetadata(
            filename=file.filename, 
            profile=json.dumps(profile),
            created_at=datetime.utcnow(),
            file_size_bytes=len(contents),
            processing_status="completed"
        )
        db.add(metadata)
        db.commit()
        db.close()

        return {
            "message": "File uploaded successfully", 
            "columns": df.columns.tolist(),
            "profile": profile
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

# This endpoint allows users to list all datasets uploaded
@app.get("/datasets")
async def list_datasets():
    db: Session = SessionLocal()
    datasets = db.query(DatasetMetadata).all()
    db.close()
    return [{"id": d.id, 
             "filename": d.filename, 
             "created_at": d.created_at
             } for d in datasets]

# This endpoint allows users to retrieve metadata for a specific dataset by its ID
@app.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: int):
    db: Session = SessionLocal()
    dataset = db.query(DatasetMetadata).filter(DatasetMetadata.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db.close()
    return {
        "id": dataset.id,
        "filename": dataset.filename,
        "profile": json.loads(dataset.profile),
        "created_at": dataset.created_at
    }

# This endpoint allows users to delete a dataset by its ID
@app.delete("/datasets/{dataset_id}")
async def delete_dataset(dataset_id: int):
    db: Session = SessionLocal()
    dataset = db.query(DatasetMetadata).filter(DatasetMetadata.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db.delete(dataset)
    db.commit()
    db.close()
    return {"message": "Dataset deleted successfully"}

# GET /datasets/{id}/analyze - Full statistical analysis
# GET /datasets/{id}/correlations - Correlation matrix
# GET /datasets/{id}/outliers - Outlier detection
# GET /datasets/{id}/trends - Trend analysis
# POST /datasets/{id}/visualize - Generate charts