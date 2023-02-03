from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger,TIME
from sqlalchemy.orm import relationship
from config import Base


class StoreID(Base):
    __tablename__ = "stores"

    store_id = Column(BigInteger, primary_key=True, index=True)

class StoreStatus(Base):
    __tablename__ = "store_status"

    id = Column(BigInteger, primary_key=True, index=True)
    store_id = Column(BigInteger)
    timestamp_utc = Column(DateTime)
    status = Column(String, default='active')

class BQ_results(Base):
    __tablename__ = "bq_results"

    store_id = Column(BigInteger,primary_key=True, index=True)
    timezone_str = Column(String)

class MenuHours(Base):
    __tablename__ = "menu_hours"

    id = Column(BigInteger, primary_key=True, index=True)
    store_id = Column(BigInteger, index=True)
    day = Column(Integer, index=True)
    start_time_local = Column(TIME)
    end_time_local = Column(TIME)

class Result(Base):
    __tablename__ = "result"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    store_id = Column(BigInteger, index=True)
    up_time_last_hour = Column(TIME)
    up_time_last_day = Column(TIME)
    up_time_last_week = Column(TIME)
    down_time_last_hour = Column(TIME)
    down_time_last_day = Column(TIME)
    down_time_last_week = Column(TIME)
    flag = Column(String)