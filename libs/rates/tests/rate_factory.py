from faker import Faker
from libs.rates.dto.interval import Interval
import random

from libs.rates.dto.rate import Rate

fake = Faker()

class RateFactory:
    @classmethod
    def create(cls, days_of_week=None, period=None, timezone=None, price=None) -> Rate:
        days_of_week = days_of_week if days_of_week else list(set(random.randint(0, 6) for _ in range(random.randint(1, 3))))
        start_hour = random.randint(0, 2259)
        end_hour = start_hour + 100
        period = period if period else Interval(start_hour, end_hour)
        timezone = timezone if timezone else fake.timezone()
        price = price if price else random.randint(100, 10000)
        return Rate(days_of_week, period, timezone, price)

    def create_list(self, count=1) -> list[Rate]:
        return [self.create() for _ in range(count)]