import datetime
from sqlalchemy import Column, DateTime, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    profile = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    file_size_bytes = Column(Integer)  # Add file size tracking
    processing_status = Column(String, default="completed")  # For future async processing