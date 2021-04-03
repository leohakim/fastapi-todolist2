import uuid
from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

class TaskModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    timestamp: datetime = Field(default=datetime.now())
    completed: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "My important task",
                "datetime": "2021-04-03T11:21:29:64129",
                "completed": False,
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "name": "My other important task",
                "completed": True,
            }
        }
