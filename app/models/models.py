from sqlmodel import SQLModel, Field
from datetime import datetime, time


class StoreStatus(SQLModel, table = True):
    __tablename__ = "store_status"

    id: int = Field(primary_key=True)
    store_id: str = Field(nullable=False, index=True)
    status:str = Field()
    timestamp_utc: datetime = Field(index=True)
    
class MenuHours(SQLModel, table =True):
    __tablename__ = "menu_hours"

    id: int = Field(primary_key=True)
    store_id: str = Field(nullable=False, index=True)
    day: int = Field()
    start_time_local: time = Field(index=True)
    end_time_local: time = Field(index=True)
    
class TimeZones(SQLModel, table=True):
    __tablename__ = 'timezones'

    id: int = Field(primary_key=True)
    store_id: str = Field(nullable=False, index=True)
    timezone_str:str = Field()
    
class RestaurantReport(SQLModel, table=True):
    __tablename__ = 'report_status'

    report_id:str = Field(nullable=False, index=True, primary_key=True)
    status:str = Field(nullable=False)