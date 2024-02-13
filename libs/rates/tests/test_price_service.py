from datetime import datetime
import pytest
from unittest.mock import MagicMock
from libs.rates import RatesRepository, PriceService
from libs.rates.dto.interval import Interval
from libs.rates.tests.rate_factory import RateFactory
from libs.utils.errors import MultipleDaysInputError, MultipleRatesError

# Mock RatesRepository
rates_repository = MagicMock(spec=RatesRepository)
rate_factory = RateFactory()


@pytest.fixture
def price_service():
    return PriceService(rates_repository)


def test_get_price_valid_interval(price_service):
    # Prepare
    start = datetime(2024, 2, 12, 10, 0)
    end = datetime(2024, 2, 12, 12, 0)

    # Run
    rate = rate_factory.create(period=Interval(900, 1600))
    rates_repository.find_rate.return_value = [rate]
    price = price_service.get_price(start, end)

    # Expect
    assert price == rate.get_price()


def test_get_price_empty_result(price_service):
    # Mock data
    start = datetime(2024, 2, 12, 10, 0)
    end = datetime(2024, 2, 12, 12, 0)

    # Set up repository to return empty list
    rates_repository.find_rate.return_value = []

    # Call get_price
    price = price_service.get_price(start, end)

    # Expect
    assert price is None  # Or any other appropriate response


def test_get_price_multiple_rates_error(price_service):
    # Prepare
    start = datetime(2024, 2, 12, 10, 0)
    end = datetime(2024, 2, 12, 12, 0)

    rate_a = rate_factory.create(days_of_week=[1, 2, 5], period=Interval(900, 1600))
    rate_b = rate_factory.create(days_of_week=[1, 3, 6], period=Interval(900, 1600))
    rates_repository.find_rate.return_value = [rate_a, rate_b]

    # Run
    price = price_service.get_price(start, end)

    # Expect
    assert price == 'unavailable'

def test_get_price_multiple_days_input_error(price_service):
    # Mock data
    start = datetime(2024, 2, 12, 10, 0)
    end = datetime(2024, 2, 13, 12, 0)  # End time is on the next day

    # Run
    price = price_service.get_price(start, end)

    # Expect
    assert price == 'unavailable'

def test_get_price_invalid_interval(price_service):
    # Mock data
    start = datetime(2024, 2, 12, 10, 0)
    end = datetime(2024, 2, 12, 8, 0)  # End time before start time

    # Call get_price
    with pytest.raises(ValueError):
        price_service.get_price(start, end)