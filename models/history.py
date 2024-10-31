from typing import Optional, List,  Any
import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr
class History(Document):
    code: int
    name: str
    time: datetime.date
    start: float
    high: float
    low: float
    close: float
    volumn: int
    turnover: int

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
        name = "history"



async def retrieve_history_find_code(code: int, end_date: datetime.date, max: int) -> List[History]:
    student = await History.find({"code": {"$eq": code}}).find({"time": {"$lte": end_date}}).limit(max).sort("-time").to_list()
    if student:
        return student

async def retrieve_history_atr(code: int, end_date: datetime.date, cycle:int) -> int:
    his_list = await History.find({"code": {"$eq": code}}).find({"time": {"$lte": end_date}}).limit(cycle).sort("-time").to_list()
    if his_list is None:
        return None
    Tr_total = 0
    for his in his_list:
        # if his.tr == 0:
        prev = his_list[his_list.index(his)-1]
        Tr1 = (his.high - his.low)
        Tr2 = abs(his.high - prev.close)
        Tr3 = abs(his.low - prev.close)
        Tr = max(Tr1, Tr2, Tr3)
        # else:
        #     Tr = his.tr
        Tr_total += Tr
    return Tr_total / 14