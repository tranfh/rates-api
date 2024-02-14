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
        days_list: list[str] = rate['days'].replace(" ", "").split(',')
        days = list(set([days_to_number_mapping[day.lower()] for day in days_list]))
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
        # Check for required fields
        required_fields = ['days', 'times', 'tz', 'price']
        seen_properties = set()
        for field in required_fields:
            if field not in rate:
                raise ValueError(f"{field.capitalize()} is required")
            if field in seen_properties:
                raise ValueError(f"Duplicate property found: {field}")
            seen_properties.add(field)

        # Check for unknown fields
        unknown_properties = set(rate.keys()) - set(required_fields)
        if unknown_properties:
            raise ValueError(f"Unknown properties: {', '.join(unknown_properties)}")

        # Validate days
        valid_days = ["mon", "tues", "wed", "thurs", "fri", "sat", "sun"]
        days = rate.get("days")

        if not days:
            raise ValueError("Days of week are required")
        if not isinstance(days, str):
            raise ValueError("Invalid value for 'days'. Please use the short name of the day. E.g. 'mon,tues'")
        days = days.replace(" ", "").split(",")
        if not all(day.lower() in valid_days for day in days):
            raise ValueError("Invalid value for 'days'. Please use the short name of the day. E.g. 'mon,tues'")

        # Validate price
        price = rate.get("price")
        if not isinstance(price, int):
            raise Exception("Invalid value for 'price'. Must be an integer")

        if price < 0:
            raise ValueError("Invalid value for 'price'. Must be a positive integer")

        # Validate times
        times = rate.get("times")
        if not times or not isinstance(times, str):
            raise Exception("Invalid value for 'times'. Must be in format 'HHMM-HHMM'")
        if len(times) != 9 or not times[4] == "-":
            raise Exception("Invalid value for 'times'. Must be in format 'HHMM-HHMM'")
        times = times.split("-")
        if len(times) != 2 or not all(time.isdigit() and len(time) == 4 for time in times):
            raise Exception("Invalid value for 'times'. Must be in format 'HHMM-HHMM'")

        # Validate timezone
        timezone = rate.get("tz")
        if not timezone or not isinstance(timezone, str):
            raise Exception("Invalid value for 'tz'. Must be a string and a valid timezone")

        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Invalid value for 'tz'. Must be a string and a valid timezone")
