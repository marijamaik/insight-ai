from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    profile = Column(JSON, nullable=False)  # Store profiling info as JSON
    created_at = Column(String, nullable=False)  # Store creation time as string for simplicity