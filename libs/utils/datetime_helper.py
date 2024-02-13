from datetime import datetime
import pytz


def isodate_to_datetime(isodate) -> datetime:
    return datetime.strptime(isodate, '%Y-%m-%dT%H:%M:%S%z')


def get_timezone_offset(timezone_name):
    """
    Get the timezone offset from the given timezone name.

    Parameters:
    timezone_name (str): Name of the timezone (e.g., 'America/Chicago').

    Returns:
    str: String representing the timezone offset (e.g., '-05:00').
    """
    # Get the timezone object
    tz = pytz.timezone(timezone_name)

    # Get the current time in the timezone
    now = datetime.now(tz)

    # Get the timezone offset
    return now.strftime('%z')
