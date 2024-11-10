from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime, timedelta

# Import your internal logic/services
from services.weather_service import WeatherService
from services.analysis_service import AnalysisService
from config.settings import Settings

app = FastAPI(title="MedClimate API")