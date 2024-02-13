from libs.rates.dto.interval import Interval


class RatesRepository:
    def __init__(self):
        self.database = []

    def update_rates(self, rates):
        self.database = rates
        return self.database

    def get_rates(self):
        return self.database

    def find_rate(self, day_of_week: int, interval: Interval, timezone: str):
        rates = []
        for rate in self.database:
            if (
                day_of_week in rate.days_of_week
                and rate.period.start <= interval.start <= rate.period.end
                and rate.period.start <= interval.end <= rate.period.end
            ):
                rates.append(rate)

        return rates
