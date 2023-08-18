from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(
        min_length=15, max_length=50)
    year: int = Field(le=2024)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 99,
                    "title": "The Hyper Human",
                    "overview": "movie description ....",
                    "year": 2018,
                    "rating": 8.8,
                    "category": "fantasy"
                }
            ]
        }
    }
