from libs.rates.dto.interval import Interval
from libs.rates.dto.days_of_week import days_to_number_mapping, number_to_days_mapping
import pytz


class Rate:
    def __init__(self, days_of_week: list[int], period: Interval, timezone: str, price: int):
        self.days_of_week = days_of_week  # List of integers representing days of the week
        self.timezone = timezone  # String representing the timezone
        self.price = price  # Integer representing the price
        self.period = period  # Dictionary representing the period with start hour and end hour

    @classmethod
    def to_model(cls, rate):
        cls._validate_rate(rate)
        days = [days_to_number_mapping[day] for day in rate['days'].split(',')]
        times = rate['times'].split('-')
        interval = Interval(int(times[0]), int(times[1]))
        return cls(days, interval, rate['tz'], rate['price'])

    def get_price(self):
        return self.price

    @classmethod
    def _validate_rate(cls, rate):
        if not rate.get('days'):
            raise Exception("Days of week are required")
        if not rate.get('times'):
            raise Exception("Times is required. Must be in format 'HHMM-HHMM'")
        if not rate.get('tz'):
            raise Exception("Timezone is required")
        if not rate.get('price'):
            raise Exception("Price is required")

        valid_days = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
        days = rate.get("days").split(",")
        if not all(day in valid_days for day in days):
            raise ValueError("Invalid value for 'days'")

        if not isinstance(rate.get("price"), int):
            raise Exception("Invalid value for 'price'. Must be an integer")

        times = rate.get("times")
        if len(times) != 9 or not times[4] == "-":
            raise Exception("Invalid value for 'times'. Must be in format 'HHMM-HHMM'")
        times = times.split("-")
        if len(times) != 2 or not all(time.isdigit() and len(time) == 4 for time in times):
            raise Exception("Invalid value for 'times'. Must be in format 'HHMM-HHMM'")

        timezone = rate.get("tz")
        if not timezone or not isinstance(timezone, str):
            raise Exception("Invalid value for 'tz'. Must be a string and a valid timezone")

        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Invalid value for 'tz'. Must be a string and a valid timezone")
