import pytest
from unittest.mock import MagicMock
from libs.rates import RatesRepository, RatesService
from libs.rates.dto.interval import Interval
from libs.rates.dto.rate import Rate
from libs.rates.tests.rate_factory import RateFactory

# Mock RatesRepository
rates_repository = MagicMock(spec=RatesRepository)
rate_factory = RateFactory()

@pytest.fixture
def rates_service():
    return RatesService(rates_repository)


def test_update_rates(rates_service):
    # Prepare
    rates_to_update = rate_factory.create_list(2)
    rates_repository.update_rates.return_value = rates_to_update

    # Run
    updated_rates = rates_service.update_rates(rates_to_update)

    # Expect
    assert updated_rates == rates_to_update

def test_get_rates(rates_service):
    # Prepare
    rates_from_repository = rate_factory.create_list(2)
    rates_repository.get_rates.return_value = rates_from_repository

    # Run

    rates = rates_service.get_rates()

    # Expect
    assert rates == rates_from_repository

def test_get_none_if_rates_doesnt_exist(rates_service):
    # Prepare
    rates_repository.get_rates.return_value = []

    # Run
    rates = rates_service.get_rates()

    # Expect
    assert rates == []