from libs.rates.dto.days_of_week import number_to_days_mapping
from libs.rates.dto.rate import Rate
import json

class RateOutput:
    def __init__(self, days: str, times: str, timezone: str, price: int):
        self.days = days
        self.times = times
        self.timezone = timezone
        self.price = price

    @classmethod
    def from_model(cls, rate: Rate):
        start_time_str = f"{rate.period.start:04d}"
        end_time_str = f"{rate.period.end:04d}"
        interval_str = f"{start_time_str}-{end_time_str}"
        days = ','.join([number_to_days_mapping[day] for day in rate.days_of_week])

        return RateOutput(days=days, times=interval_str, timezone=rate.timezone, price=rate.price)

    def to_json(self):
        return {
            "days": self.days,
            "price": self.price,
            "times": self.times,
            "tz": self.timezone
        }