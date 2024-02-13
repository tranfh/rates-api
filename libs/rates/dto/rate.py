import pytz
from libs.rates.dto import Interval, days_to_number_mapping


class Rate:
    def __init__(self, days_of_week: list[int], period: Interval, timezone: str, price: int):
        """
        Initialize a Rate object.

        Parameters:
        - days_of_week (list[int]): List of integers representing days of the week.
        - period (Interval): Interval object representing the period with start and end hours.
        - timezone (str): String representing the timezone.
        - price (int): Integer representing the price.

        Returns:
        None
        """
        self.days_of_week = days_of_week
        self.timezone = timezone
        self.price = price
        self.period = period

    @classmethod
    def to_model(cls, rate) -> 'Rate':
        """
        Convert a dictionary representing a rate into a Rate object.

        Parameters:
        - rate (dict): Dictionary containing rate information.

        Returns:
        Rate: Rate object created from the input dictionary.
        """
        cls._validate_rate(rate)
        days = [days_to_number_mapping[day] for day in rate['days'].split(',')]
        times = rate['times'].split('-')
        interval = Interval(int(times[0]), int(times[1]))
        return cls(days, interval, rate['tz'], rate['price'])

    def get_price(self):
        """
        Get the price of the rate.

        Returns:
        int: The price of the rate.
        """
        return self.price

    @classmethod
    def _validate_rate(cls, rate):
        """
        Validate the rate dictionary.

        Parameters:
        - rate (dict): Dictionary containing rate information.

        Returns:
        None
        """
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
