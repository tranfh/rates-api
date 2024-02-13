from libs.rates.dto import Rate
from libs.rates import RatesRepository


class RatesService:

    def __init__(self, rates_repository: RatesRepository):
        self.rates_repository = rates_repository

    def update_rates(self, rates) -> list[Rate]:
        """
        Updates the rates with the provided data.

        Retrieves the list of rates from the rates repository, updates them
        with the provided data, and returns the modified rates.

        Args:
            rates (list[Rate]): The list of Rate objects containing updated data.

        Returns:
            list[Rate]: The modified rates after updating.
        """
        modified_rates: list[Rate] = self.rates_repository.update_rates(rates)
        return modified_rates

    def get_rates(self) -> list[Rate]:
        """
        Retrieves the list of rates.

        Fetches the list of rates from the rates repository and returns it.

        Returns:
            list[Rate]: The list of rates.
        """
        rates = self.rates_repository.get_rates()
        return rates
