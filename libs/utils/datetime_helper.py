from datetime import datetime

def isodate_to_datetime(isodate) -> datetime:
    return datetime.strptime(isodate, '%Y-%m-%dT%H:%M:%S%z')
