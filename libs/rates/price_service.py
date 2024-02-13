from datetime import datetime
from typing import Optional

from libs.rates import RatesRepository
from libs.rates.dto import Interval
from libs.utils.errors import MultipleDaysInputError, MultipleRatesError


class PriceService:
    def __init__(self, rates_repository: RatesRepository):
        self.rate_repository = rates_repository

    def get_price(self, start: datetime, end: datetime) -> Optional[float or str]:
        """
        Calculate the price for the specified time interval.

        Parameters:
        - start (datetime): Start datetime of the interval.
        - end (datetime): End datetime of the interval.

        Returns:
        - float or None: Price for the interval, or None if no matching rate is found.
        """
        try:
            self._validate_interval(start, end)

            day_of_week = start.weekday()
            interval = self._create_interval(start, end)
            timezone = self._get_timezone_offset(start)

            rates = self.rate_repository.find_rate(day_of_week, interval, timezone)

            if len(rates) > 1:
                raise MultipleRatesError("Multiple rates found for the given interval")

            return rates[0].get_price() if rates else None

        except MultipleDaysInputError:
            return "unavailable"
        except MultipleRatesError:
            return "unavailable"
        except Exception as e:
            raise e

    def _validate_interval(self, start: datetime, end: datetime) -> None:
        """
        Validate the time interval.

        Parameters:
        - start (datetime): Start datetime of the interval.
        - end (datetime): End datetime of the interval.
        """
        if start >= end:
            raise ValueError("Start date time must be before end date time")
        if start.tzinfo != end.tzinfo:
            raise ValueError("Time zones of start and end times must be consistent")
        if start.date() != end.date():
            raise MultipleDaysInputError("Start and end times must be on the same day")


    def _create_interval(self, start: datetime, end: datetime) -> Interval:
        """
        Create an interval object from start and end datetimes.

        Parameters:
        - start (datetime): Start datetime of the interval.
        - end (datetime): End datetime of the interval.

        Returns:
        - Interval: Interval object representing the time interval.
        """
        start_hour_str = f"{start.hour:02d}"
        start_minute_str = f"{start.minute:02d}"
        end_hour_str = f"{end.hour:02d}"
        end_minute_str = f"{end.minute:02d}"

        return Interval(int(start_hour_str + start_minute_str), int(end_hour_str + end_minute_str))

    def _get_timezone_offset(self, dt: datetime) -> str:
        """
        Get the timezone offset from the datetime object.

        Parameters:
        - dt (datetime): Datetime object.

        Returns:
        - str: Timezone offset in the format '±HH:MM'.
        """
        return dt.strftime('%z')



