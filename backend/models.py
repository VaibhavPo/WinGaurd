from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    camera_id = Column(String)
    label = Column(String)
    species = Column(String)
    confidence = Column(Float)
    image_path = Column(String)
