from fastapi import FastAPI, Request, File, UploadFile
from datetime import datetime
import report
from fastapi.responses import FileResponse
import json
from MultiPartResponse import MultipartMixedResponse
import helpers

app = FastAPI()

current_utc = "2023-01-25 18:20:00.00 UTC"

current_datetime = datetime.strptime(current_utc, '%Y-%m-%d %H:%M:%S.%f %Z')


@app.get("/trigger_report")
async def generateReport():
    report_id = report.generate(endtime= current_datetime)
    return {"Report ID": report_id}

@app.get("/get_report")
async def getReport(report_id: str):
    status = report.getReport(report_id)
    if status.status == 'Running':
        return {"Status": "Running"}
    else:
        message = {"Status": "Completed"}
        filename = f"report_{report_id}.csv"
        return FileResponse(filename, filename='report.csv', headers={"Content-Disposition": "attachment"}, media_type="text/csv")
        # response = MultipartMixedResponse(json.dumps(message), filename, filename)
        # return response
    
@app.on_event("startup")
def startup():
    helpers.db_init()