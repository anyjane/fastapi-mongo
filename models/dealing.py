from typing import Optional, List,  Any
import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr
class Dealing(Document):
    code: int
    name: str
    time: datetime.date
    shares: int 
    cost: float

    class Config:
        json_schema_extra = {
            "example": {
                "code": 12345,
                "name": "abdul@school.com",
                "time": datetime.date.today(), 
                "shares": 4,
                "cost": 4
            }
        }

    class Settings:
        name = "dealing"


async def retrieve_dealings() -> List[Dealing]:
    students = await Dealing.all().to_list()
    return students