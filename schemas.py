import datetime
from pydantic import BaseModel
from typing import Optional

class BQ_results(BaseModel):
    store_id: int
    timeone_str: Optional[str] = "America/Chicago"

    class Config:
        orm_mode = True

class StoreStatus(BaseModel):
    id: int
    store_id: int
    timestamp_utc: Optional[datetime.datetime] = None
    status: Optional[str] = 'active'

    class Config:
        orm_mode = True

class MenuHours(BaseModel):
    id: int
    store_id: int
    day: Optional[int] = None
    start_time_local: Optional[datetime.time] = None
    end_time_local: Optional[datetime.time] = None

    class Config:   
        orm_mode = True

class Result(BaseModel):
    store_id: int
    up_time_last_hour: Optional[datetime.time] = None
    up_time_last_day: Optional[datetime.time] = None
    up_time_last_week: Optional[datetime.time] = None
    down_time_last_hour: Optional[datetime.time] = None
    down_time_last_day: Optional[datetime.time] = None
    down_time_last_week: Optional[datetime.time] = None

    class Config:   
        orm_mode = True

class StoreID(BaseModel):
    store_id = int