import datetime
import pytz

def local_to_utc(area,time):
    local = pytz.timezone(area)
    naive = datetime.datetime.strftime(f"{datetime.date.today()} {time}", "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc).time()
    return utc_dt

def get_weekday_and_time(timestamp_utc):
    x_date = datetime.date(timestamp_utc.year, timestamp_utc.month, timestamp_utc.day)
    time = timestamp_utc.time()
    weekday = x_date.weekday()
    return weekday, time, x_date

def get_week_date():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    return week_ago

def get_time_hour():
    current_timestamp = datetime.datetime.now() - datetime.timedelta(hours=1)
    weekday = current_timestamp.weekday()
    return current_timestamp, weekday

def time_in_range(start, end, time1 , time2):
    return start <= time1 and time2 <= end