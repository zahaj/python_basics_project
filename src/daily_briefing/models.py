"""
Defines the Pydantic models for the application.

Pydantic models are used for:
1. Data validation of incoming API requests.
2. Defining the structure of outgoing API responses.
3. Generating OpenAPI schema for the interactive documentation.
"""
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

@dataclass(frozen=True) # 'frozen=True' makes instances immutable
class WeatherInfo:
    """Represents structured weather information."""
    city: str
    temperature: float
    feels_like: float
    description: str
    icon_code: str
    
class BriefingResponse(BaseModel):
    """Defines the response structure for the main /briefing endpoint."""
    user_name: str
    city: str
    weather_summary: Optional[str] = None
    latest_post_title: Optional[str] = None
    error_message: Optional[str] = None

class BriefingLog(BaseModel):
    """Pydantic schema for reading log entries from the API."""
    id: int
    user_id: int
    city: str
    created_at: datetime
    # This allows the Pydantic model to be created from an ORM object
    model_config = ConfigDict(from_attributes=True)