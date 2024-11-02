import datetime

def timestamp_as_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)
    return dt