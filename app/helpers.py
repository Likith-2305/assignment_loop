from datetime import datetime, time, timedelta
from models.models import MenuHours, StoreStatus, TimeZones
import pytz
from sqlmodel import SQLModel, Session
from models.database import engine
import pandas as pd

def max(datetime1:time, datetime2:time):
    if datetime1 is None:
        return datetime2
    elif datetime2 is None:
        return datetime1
    else:
        return max(datetime1, datetime2)
    
def shop_open(timings: list, now: datetime, timezone: str):
    day = now.weekday()
    timingList = [menu_hour for menu_hour in timings if menu_hour.day == day]
    if not timingList and len(timings) != 0:
        return False
    if len(timings) == 0:
        return True
    flag = False
    for timing in timingList:
        endTime = timing['end_time_local']
        startTime = timing['start_time_local']
        currentTime = now.time()
        if(endTime> currentTime and startTime < currentTime):
            flag = True
            break
    return flag
    
def convertToUtc(localTime: time, timezone:str):
    localTimezone = pytz.timezone(timezone)
    localTimeWithTz = localTimezone.localize(datetime.combine(datetime.now().date(), localTime))
    utcTimeConverted = localTimeWithTz.astimezone(pytz.utc).time()
    return utcTimeConverted

def convertToLocalTime(utcTime:datetime, timezone: str):
    localTimezone = pytz.timezone(timezone)
    utcTimeWithTz = pytz.utc.localize(utcTime)
    localTimeConverted = utcTimeWithTz.astimezone(localTimezone).replace(tzinfo=None)
    return localTimeConverted

def getLastUpdateTime(storeTimings: list, lastKnownUpdate: datetime):
    print("input*************************************",lastKnownUpdate)
    day = lastKnownUpdate.weekday()
    timingList = [menu_hours for menu_hours in storeTimings if menu_hours.day == day]
    lastKnowTime = lastKnownUpdate.time()
    if len(storeTimings) == 0:
        return lastKnownUpdate
    else:
        for timing in timingList:
            startTime = datetime.combine(lastKnownUpdate.date(), timing['start_time_local'])
            endTime = datetime.combine(lastKnownUpdate.date(), timing['end_time_local'])
            if (lastKnownUpdate<startTime):
                return startTime
            elif(lastKnownUpdate>startTime and lastKnownUpdate<endTime):
                return lastKnownUpdate
        i = 0
        while True:
            i+= 1
            day = (day+i)%7
            nextDayList = [menu_hours for menu_hours in storeTimings if menu_hours.day == day]
            if len(nextDayList) != 0:
                return datetime.combine(lastKnownUpdate.date(), nextDayList[0]['start_time_local'])+timedelta(days=i)
    
def getTotalWorkingHours(store_timings:list):
    workingHours  = 0
    i=1
    for timing in store_timings:
        i+=1
        startTime = datetime.combine(datetime.now(), timing.start_time_local)
        endTime = datetime.combine(datetime.now(), timing.end_time_local)
        workingHours += (endTime-startTime).total_seconds() / 3600.0
    return workingHours

flagFile = "dataImported.flag"

def readFlag():
    try:
        with open(flagFile, "r") as f:
            return f.read().strip() == "True"
    except FileNotFoundError:
        return False

# Write the flag to the file
def write_flag(value):
    with open(flagFile, "w") as f:
        f.write(str(value))


def db_init():
    SQLModel.metadata.create_all(bind=engine)
    dataImported = readFlag()
    if not dataImported:
        with Session(engine) as session:
            df = pd.read_csv("./data/store_status.csv")
            for index, row in df.iterrows():
                try:
                    timestamp = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S %Z")
                except ValueError:
                    timestamp = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f %Z")
                status = StoreStatus(id=index, store_id=row[0], status=row[1], timestamp_utc=timestamp)
                session.add(status)
            df = pd.read_csv("./data/menu_hours.csv")
            for index, row in df.iterrows():
                timings = MenuHours(id=index, store_id=row[0], day=row[1], start_time_local=row[2], end_time_local=row[3])
                session.add(timings)
            df = pd.read_csv("./data/timezones.csv")
            for index, row in df.iterrows():
                timezones = TimeZones(id=index, store_id=row[0], timezone_str=row[1])
                session.add(timezones)
            session.commit()
        write_flag(True)
