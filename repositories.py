import datetime
from utils import *
from sqlalchemy import cast, DATE
from load_csv import update_flag
import models
from config import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close

def get_report_status(store_id):
    db = get_db()
    result = db.query(models.Result).filter(models.Result.store_id == store_id).filter(models.Result.flag == "new").all()
    if result:
        update_flag(store_id)
        return True
    else:
        return False

def get_downtime_last_hour(store_id):
    db = get_db()
    current_timestamp, weekday = get_time_hour()
    store_status = db.query(models.StoreStatus).filter(models.StoreStatus.store_id == store_id).filter(models.StoreStatus.timestamp_utc <= current_timestamp).order_by(models.StoreStatus.timestamp_utc.desc()).filter(models.StoreStatus.status == 'inactive').first()
    if store_status:
        weekday2, time, x_date = get_weekday_and_time(store_status.timestamp_utc)
        menu_hours = db.query(models.MenuHours).filter(models.MenuHours.store_id == store_id).filter(models.MenuHours.day == weekday).all()
        if menu_hours:
            if menu_hours[0].start_time_local <= time <= menu_hours[0].end_time_local:
                current_time = datetime.datetime.now().time()
                diff = datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) - datetime.timedelta(hours=time.hour,minutes=time.minute,seconds=time.second)
                time_diff = (datetime.datetime.min + diff).time()
            else:
                time_diff = datetime.time(1, 0)
            return time_diff
        else:
            time_diff = datetime.time(0, 0)
    else:
        time_diff = datetime.time(0, 0)
    return time_diff


def get_downtime_last_day(store_id):
    db = get_db()
    weekday, time, x_date = get_weekday_and_time(datetime.datetime.now())
    store_status = db.query(models.StoreStatus).filter(models.StoreStatus.store_id == store_id).filter(cast(models.StoreStatus.timestamp_utc, DATE) == datetime.date.today()).filter(models.StoreStatus.status == 'inactive').all()
    count_time = datetime.timedelta(0)
    if store_status:
        menu_hours = db.query(models.MenuHours).filter(models.MenuHours.store_id == store_id).filter(models.MenuHours.day == weekday).all()
        for i in range(len(store_status)):
            weekday, time, x_date = get_weekday_and_time(store_status[i].timestamp_utc)
            if menu_hours:
                if menu_hours[0].start_time_local <= time <= menu_hours[0].end_time_local:
                    current_time = datetime.datetime.now().time()
                    time_diff = datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) - datetime.timedelta(hours=time.hour,minutes=time.minute,seconds=time.second)
                    count_time += time_diff
                else:
                    time_diff = datetime.timedelta(hours=1)
                    count_time += time_diff
                if i > 1:
                    for j in range(0,22,3):
                        if time_in_range(datetime.time(j,0), datetime.time(j+3,0), store_status[i].timestamp_utc.time(), store_status[i-1].timestamp_utc.time()):
                            count_time += datetime.timedelta(hours=3)
            else:
                if i > 1:
                    for j in range(0,22,3):
                        if time_in_range(datetime.time(j,0), datetime.time(j+3,0), store_status[i].timestamp_utc.time(), store_status[i-1].timestamp_utc.time()):
                            count_time += datetime.timedelta(hours=3)

    count_time = (datetime.datetime.min + count_time).time()
    return count_time


def get_downtime_last_week(store_id):
    db = get_db()
    store_status = db.query(models.StoreStatus).filter(models.StoreStatus.store_id == store_id).filter(models.StoreStatus.timestamp_utc >= datetime.date.today() - datetime.timedelta(days=7)).filter(models.StoreStatus.status == 'inactive').all()
    menu_hours = db.query(models.MenuHours).filter(models.MenuHours.store_id == store_id).all()
    count_time = datetime.timedelta(0)
    for i in range(len(store_status)):
        weekday, time, x_date = get_weekday_and_time(store_status[i].timestamp_utc)
        if menu_hours:
            for x in menu_hours:
                if x.day == weekday:
                    if menu_hours[0].start_time_local <= time <= menu_hours[0].end_time_local:
                        current_time = datetime.datetime.now().time()
                        time_diff = datetime.timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second) - datetime.timedelta(hours=time.hour,minutes=time.minute,seconds=time.second)
                        count_time += time_diff
                    else:
                        time_diff = datetime.timedelta(hours=1)
                        count_time += time_diff
                    if i > 1:
                        for j in range(0,22,3):
                            if time_in_range(datetime.time(j,0), datetime.time(j+3,0), store_status[i].timestamp_utc.time(), store_status[i-1].timestamp_utc.time()):
                                count_time += datetime.timedelta(hours=3)
            else:
                for j in range(0,22,3):
                    if time_in_range(datetime.time(j,0), datetime.time(j+3,0), store_status[i].timestamp_utc.time(), store_status[i-1].timestamp_utc.time()):
                        count_time += datetime.timedelta(hours=3)

    count_time = (datetime.datetime.min + count_time).time()
    return count_time

def get_working_hours(store_id):
    db = get_db()
    weekday, time, x_date = get_weekday_and_time(datetime.datetime.now())
    menu_hours = db.query(models.MenuHours).filter(models.MenuHours.store_id == store_id).filter(models.MenuHours.day == weekday).all()
    working_hours = datetime.timedelta(0)

    for i in menu_hours:
        start_time = i.start_time_local
        end_time = i.end_time_local
        time_diff = datetime.timedelta(hours=end_time.hour,minutes=end_time.minute,seconds=end_time.second) - datetime.timedelta(hours=start_time.hour,minutes=start_time.minute,seconds=start_time.second)
        working_hours += time_diff
    
    working_hours = (datetime.datetime.min + working_hours).time()
    return working_hours

def get_working_hours_week(store_id):
    db = get_db()
    working_hours = datetime.timedelta(0)
    for weekday in range(0, 7):
        menu_hours = db.query(models.MenuHours).filter(models.MenuHours.store_id == store_id).filter(models.MenuHours.day == weekday).all()
        for i in menu_hours:
            start_time = i.start_time_local
            end_time = i.end_time_local
            time_diff = datetime.timedelta(hours=end_time.hour,minutes=end_time.minute,seconds=end_time.second) - datetime.timedelta(hours=start_time.hour,minutes=start_time.minute,seconds=start_time.second)
            working_hours += time_diff
    
    working_hours = (datetime.datetime.min + working_hours).time()
    return working_hours