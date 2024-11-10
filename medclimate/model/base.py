# medclimate/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, String

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = "weather_records"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    location = Column(String)
    
    def __repr__(self):
        return f"<WeatherRecord(timestamp={self.timestamp}, temp={self.temperature}°C)>"