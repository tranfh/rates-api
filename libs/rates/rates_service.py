from libs.rates.dto.rate import Rate
from libs.rates.rates_repository import RatesRepository


class RatesService:

    def __init__(self, rates_repository: RatesRepository):
        self.rates_repository = rates_repository

    def update_rates(self, rates) -> list[Rate]:
        modified_rates: list[Rate] = self.rates_repository.update_rates(rates)
        return modified_rates

    def get_rates(self) -> list[Rate]:
        rates = self.rates_repository.get_rates()
        return rates
