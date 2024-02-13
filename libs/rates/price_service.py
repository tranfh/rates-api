from libs.rates import RatesRepository
from datetime import datetime

from libs.rates.dto.interval import Interval
from libs.utils.errors import MultipleDaysInputError, MultipleRatesError


class PriceService:
    def __init__(self, rates_repository: RatesRepository):
        self.rate_repository = rates_repository

    def get_price(self, start, end):
        try:
            self._validate_interval(start, end)

            # get day of week from start and end
            day_of_week = start.weekday()
            start_hour_str = f"{start.hour:02d}"
            start_minute_str = f"{start.minute:02d}"
            end_hour_str = f"{end.hour:02d}"
            end_minute_str = f"{end.minute:02d}"

            interval = Interval(int(start_hour_str + start_minute_str),int(end_hour_str + end_minute_str))

            # TODO: manage timezone in search
            timezone = start.tzname()
            rates = self.rate_repository.find_rate(day_of_week, interval, timezone)

            if len(rates) > 1:
                raise MultipleRatesError("Multiple rates found for the given interval")

            return rates[0].get_price() if rates else None

        except MultipleDaysInputError as e:
            return "unavailable"
        except MultipleRatesError as e:
            return "unavailable"
        except Exception as e:
            raise e

    def _validate_interval(self, start: datetime, end: datetime):
        if start >= end:
            raise ValueError("Start date time must be before end date time")
        if start.tzinfo != end.tzinfo:
            raise ValueError("Time zones of start and end times must be consistent")
        if start.date() != end.date():
            raise MultipleDaysInputError("Start and end times must be on the same day")

