from models import dbOperations
from datetime import datetime, timedelta
import helpers
import csv
import datetime
import threading

def generateReport(endTime: datetime, stores: list, timestamp: str, fieldnames: list):
    for store in stores:
        timezone = dbOperations.get_timezone(store.store_id).timezone_str
        validFileName = f'report_{timestamp}.csv'
        startTime = endTime - timedelta(weeks=1)
        pollingData = dbOperations.get_store_within(startTime, endTime, store.store_id)
        endTime = helpers.convertToLocalTime(endTime, timezone)
        startTime = helpers.convertToLocalTime(startTime, timezone)    
        storeTimings = dbOperations.get_working_hours(store.store_id)
        lastKnownUpdate = helpers.getLastUpdateTime(storeTimings, startTime)
        uptime_last_week = 0
        uptime_last_day = 0
        uptime_last_hour = 0
        for i in pollingData:
            pollTimeinLocal = helpers.convertToLocalTime(i.timestamp_utc, timezone)
            if  i.status == 'active':
                # print(f"*******polling time in local: {pollTimeinLocal}\n********lastKnownupdate: {lastKnownUpdate}")  
                time_difference = (pollTimeinLocal-lastKnownUpdate).total_seconds() / 3600.0
                if (pollTimeinLocal < endTime-timedelta(days=1)):
                    if helpers.shop_open(storeTimings, lastKnownUpdate, timezone):
                        print(f"*******polling time in local: {pollTimeinLocal}\n********lastKnownupdate: {lastKnownUpdate}**************************inside week")
                        print(f'*********************time difference{time_difference}, uptime last week: {uptime_last_week}')
                        uptime_last_week += time_difference
                elif (pollTimeinLocal >= endTime-timedelta(days=1) and pollTimeinLocal <= endTime-timedelta(hours=1)):
                    if helpers.shop_open(storeTimings, lastKnownUpdate, timezone):
                        uptime_last_day += time_difference
                        uptime_last_week += time_difference
                elif(pollTimeinLocal >= endTime-timedelta(hours=1)):
                    time_difference_in_mins = (pollTimeinLocal-lastKnownUpdate).total_seconds() / 60.0
                    if helpers.shop_open(storeTimings, lastKnownUpdate, timezone):
                        uptime_last_day += time_difference
                        uptime_last_week += time_difference
                        uptime_last_hour += time_difference_in_mins
            # print(f"store timings: {storeTimings}\npoll time: {pollTimeinLocal}")
            lastKnownUpdate = helpers.getLastUpdateTime(storeTimings, pollTimeinLocal)
            print("output**********************", lastKnownUpdate)

        if uptime_last_hour > 60:
            uptime_last_hour = 60
        downtimeLastHour = 60 - uptime_last_hour
        downtimeLastDay = 24 - uptime_last_day
        downtimeLastWeek = helpers.getTotalWorkingHours(storeTimings) - uptime_last_week
        row_data = {'store_id': store.store_id,
                    'uptime_last_hour(in minutes)': uptime_last_hour,
                    'uptime_last_day(in hours)': uptime_last_day, 
                    'update_last_week(in hours)': uptime_last_week, 
                    'downtime_last_hour(in minutes)': downtimeLastHour,
                    'downtime_last_day(in hours)': downtimeLastDay,
                    'downtime_last_week(in hours)': downtimeLastWeek
                    }
        with open(validFileName, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(row_data)
    dbOperations.updateReportStatus(timestamp)    
    
def generate(endtime: datetime):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    dbOperations.makeReport(timestamp)
    reportStatus = dbOperations.getReport(timestamp)
    valid_filename = f'report_{timestamp}.csv'
    fieldnames = ['store_id', 'uptime_last_hour(in minutes)', 'uptime_last_day(in hours)', 
                  'update_last_week(in hours)', 'downtime_last_hour(in minutes)','downtime_last_day(in hours)', 'downtime_last_week(in hours)']
    with open(valid_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    stores = dbOperations.get_store()
    newThread = threading.Thread(target=generateReport, args=(endtime, stores, timestamp, fieldnames))
    newThread.start()
    return timestamp

def getReport(report_id:str):
    reportStatus = dbOperations.getReport(report_id)
    return reportStatus
