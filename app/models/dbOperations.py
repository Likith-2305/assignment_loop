from sqlmodel import Session, select, func, text
from .database import engine
from .models import RestaurantReport, TimeZones
from datetime import datetime


def get_store():
    with Session(engine) as session:
        statement = select(TimeZones)
        results = session.exec(statement)
        return results.all()
    
def get_store_within(start_time: datetime, end_time: datetime, store_id: text):
    with Session(engine) as session:
        statement = text(f"""
                            SELECT 
                                store_id,
                                status,
                                timestamp_utc,
                                id
	                        FROM 
                                public.store_status 
                            WHERE 
                                store_id = '{store_id}' 
                                AND (timestamp_utc <='{end_time}' and timestamp_utc >='{start_time}') 
                            ORDER BY
                                timestamp_utc;
                        """)
        rows = session.execute(statement).all()
        return rows
    
def get_working_hours(store_id: str):
    with Session(engine) as session:
        statement = text(f"""
                        SELECT * from menu_hours where store_id = '{store_id}';    
                    """)
        return session.execute(statement).all()
    
def get_timezone(store_id: str):
    with Session(engine) as session:
        statement = select(TimeZones).where(TimeZones.store_id == store_id)
        return session.exec(statement).first()
    
def makeReport(report_id: str):
    with Session(engine) as session:
        report = RestaurantReport(report_id=report_id, status='Running')
        session.add(report)
        session.commit()
        session.close()

def getReport(report_id: str):
    with Session(engine) as session:
        statement = select(RestaurantReport).where(RestaurantReport.report_id == report_id)
        return session.exec(statement).first()
    
def updateReportStatus(report_id: str):
    with Session(engine) as session:
        statement = select(RestaurantReport).where(RestaurantReport.report_id == report_id)
        reportStatus = session.exec(statement).first()
        reportStatus.status = 'Completed'
        session.add(reportStatus)
        session.commit()
        session.close()