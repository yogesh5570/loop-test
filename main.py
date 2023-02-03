from fastapi import FastAPI
import uvicorn
import models
import datetime
from config import SessionLocal, engine
from repositories import *
from load_csv import get_report_id, get_csv
import threading
from fastapi.responses import FileResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        print(e)

def run_query(store_id):
    db = get_db()
    downtime_hour = get_downtime_last_hour(store_id)
    if downtime_hour == datetime.time(0,0):
        uptime_hour = datetime.time(1,0)
    else:
        uptime_hour = datetime.time(0,0)

    downtime_day = get_downtime_last_day(store_id)
    if downtime_day != datetime.time(0,0):
        working_hours = get_working_hours(store_id)
        uptime_day = datetime.timedelta(hours=working_hours.hour, minutes=working_hours.minute, seconds=working_hours.second) - datetime.timedelta(hours=downtime_day.hour,minutes=downtime_day.minute,seconds=downtime_day.second)
    else:
        uptime_day = get_working_hours(store_id)
    
    downtime_week = get_downtime_last_week(store_id)
    if downtime_week != datetime.time(0,0):
        working_week = get_working_hours_week(store_id)
        uptime_week = datetime.timedelta(hours=working_week.hour, minutes=working_week.minute, seconds=working_week.second) - datetime.timedelta(hours=downtime_week.hour,minutes=downtime_week.minute,seconds=downtime_week.second)
    else:
        uptime_week = get_working_hours_week(store_id)

    print(store_id, uptime_day, downtime_day, uptime_hour, downtime_hour, uptime_week, downtime_week)
    result = db.add(models.Result(
        store_id = store_id,
        up_time_last_hour = uptime_hour,
        up_time_last_day = uptime_day,
        up_time_last_week = uptime_week,
        down_time_last_hour = downtime_hour,
        down_time_last_day = downtime_day,
        down_time_last_week = downtime_week,
        flag = "new"
        ))
    db.commit()
    return True

@app.get("/report/")
def generate_report_id():
    result = get_report_id()[0][0]
    t1 = threading.Thread(target=run_query, args=(result,))
    t1.start()
    return {"report_id": result}


@app.get("/report/{store_id}")
def get_store(store_id: int):
    result = get_report_status(store_id)
    if result:
        get_csv(store_id)
        file_loc = 'result_file.csv'
        return FileResponse(file_loc)
    else:
        return {"message": "Running"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)