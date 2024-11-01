from typing import Optional, List,  Any
import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr
class Dealing(Document):
    code: int
    name: str
    buy_date: datetime.date
    cost: float
    shares: int 
    sell_date: Optional[datetime.date] = None
    sell_price: Optional[float] = None

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

async def retrieve_find_dealing(code: int) -> List[Dealing]:
    student = await Dealing.find({"code": {"$eq": code}}).to_list()
    if student:
        return student

async def add_dealing(dealing: Dealing) -> Dealing:
    student = await dealing.create()
    return student