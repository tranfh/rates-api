from libs.rates.dto import Interval
from libs.utils.datetime_helper import get_timezone_offset_from_name


class RatesRepository:
    def __init__(self):
        self.database = []

    def update_rates(self, rates):
        self.database = rates
        return self.database

    def get_rates(self):
        return self.database

    def find_rate(self, day_of_week: int, interval: Interval, timezone: str):
        """
        Find rates based on the specified criteria.

        Parameters:
        - day_of_week (int): Day of the week (0 for Monday, 1 for Tuesday, ..., 6 for Sunday).
        - interval (Interval): Time interval to search for rates.
        - timezone (str): Timezone offset (e.g., 'UTC-05:00').

        Returns:
        - List[Rate]: List of rates that match the criteria.
        """

        # Initialize list to store matching rates
        rates = []

        # Iterate through database and find matching rates
        for rate in self.database:
            # Matching weekday and timezone
            if day_of_week in rate.days_of_week and get_timezone_offset_from_name(rate.timezone) == timezone:
                # Check if interval overlaps with rate period
                if (rate.period.start <= interval.start < rate.period.end) or \
                        (rate.period.start <= interval.end < rate.period.end) or \
                        (interval.start < rate.period.start and interval.end > rate.period.end):
                    rates.append(rate)

        return rates
