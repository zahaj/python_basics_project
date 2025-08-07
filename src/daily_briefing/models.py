from dataclasses import dataclass
from typing import Union
import math

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class WeatherInfo:
    """
    A dataclass to hold structured weather information.
    'frozen=True' makes instances immutable, which is good practice for data
    objects that shouldn't be changed after creation.
    """
    city: str
    temperature: float
    feels_like: float
    description: str
    icon_code: str # e.g., '01d' for clear sky day
    
class BriefingResponse(BaseModel):
    """Pydantic model for the briefing API response."""
    user_name: str
    city: str
    weather_summary: Optional[str] = None
    latest_post_title: Optional[str] = None
    error_message: Optional[str] = None

# SQLAlchemy models are your database layer — they represent data in the database.
# Pydantic models are your API/data validation layer — they represent data you send
# or receive via FastAPI (or similar frameworks).
# You don’t want to expose raw database models directly to users, so you convert
# SQLAlchemy models → Pydantic models for API responses.

class BriefingLog(BaseModel):
    """Pydantic schema for reading log entries from the API."""
    id: int
    user_id: int
    city: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True) # This allows the Pydantic model to be created from an ORM object

class Shape:
    """This is a base class for different shapes."""

    def area(self) -> int:
        """Calculates the area of the shape."""
        return 0

    def perimeter(self):
        """Calculates the perimeter of the shape."""
        return 0
    
    def __str__(self):
        return f"Shape()"
    
    def __repr__(self):
        return f"Shape()"
    
class Circle(Shape):

    def __init__(self, radius: Union[int, float]):
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise ValueError("Radius must be a positive number")
        self.radius = radius

    def area(self):
        """Calculates an area of a circle."""
        area = math.pi * self.radius ** 2
        return area
    
    def perimeter(self):
        """Returns a perimeter of a circle."""
        perimeter = 2 * math.pi * self.radius
        return perimeter

    def __str__(self):
        return f"Circle(Radius: {self.radius})"

    def __repr__(self):
        return f"Circle(radius={self.radius})"

class Rectangle(Shape):
    
    def __init__(self, length: Union[int, float], width: Union[int, float]):
        if not isinstance(length, (int, float)) or length <= 0:
            raise ValueError("Length must be a positive number")
        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive number")
        self.length = length
        self.width = width
    
    def area(self):
        """Returns an area of a rectangle with sides: length and width."""
        area =  self.length * self.width
        return area

    def perimeter(self):
        """Returns a perimeter of a rectangle with sides: length and width."""
        perimeter = 2 * (self.length + self.width)
        return perimeter
    
    def __str__(self):
        return f"Rectangle(Length: {self.length}, Width: {self.width})"

    def __repr__(self):
        return f"Rectangle(length={self.length}, width={self.width})"

# frozen=True makes instances of the dataclass immutable (their attributes cannot be changed after creation),
# which is often a good choice for data-holding objects
@dataclass(frozen=True)
class Vector:

    x: Union[float, int]
    y: Union[float, int]

    def __add__(self, other):
        """Implements vector addition (self + other)."""
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type for +: 'Vector' and '{type(other).__name__}'")
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Implements vector subtraction (self - other)."""
        if not isinstance(other, Vector):
            raise TypeError(f"Unsupported operand type for -: 'Vector' and '{type(other).__name__}'")
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]):
        """Implements scalar multiplication (vector * scalar)."""
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Unsupported operand type for *: 'Vector' and '{type(scalar).__name__}' (expected scalar)")
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        """Calculates the Euclidean magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

# vector1 = Vector(1.6, -0.2)
# print(vector1, vector1.__repr__())