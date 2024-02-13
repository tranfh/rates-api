import pytest
from unittest.mock import MagicMock
from libs.rates import RatesRepository, Rate
from libs.rates.dto.interval import Interval
from libs.rates.tests.rate_factory import RateFactory

rate_factory = RateFactory()


@pytest.fixture
def rates_repository():
    return RatesRepository()

def test_update_rates(rates_repository):
    # Prepare
    rates = rate_factory.create_list(3)

    # Run
    updated_rates = rates_repository.update_rates(rates)

    # Expect
    assert updated_rates == rates_repository.database
    assert updated_rates == rates


def test_get_rates(rates_repository):
    # Prepare
    rates = rate_factory.create_list(3)
    rates_repository.update_rates(rates)

    # Run
    retrieved_rates = rates_repository.get_rates()

    # Expect
    assert retrieved_rates == rates


def test_find_rate(rates_repository):
    # Prepare
    day_of_week = 1
    interval = Interval(900, 1600)
    timezone = "America/New_York"

    rate_1 = rate_factory.create(days_of_week=[1, 2, 3], period=Interval(900, 1600))
    rate_2 = rate_factory.create(days_of_week=[0, 5, 6], period=Interval(900, 1600))

    rates_repository.update_rates([rate_1, rate_2])

    # Execute
    found_rates = rates_repository.find_rate(day_of_week, interval, timezone)

    # Assert
    assert found_rates == [rate_1]

def test_find__multiple_rates(rates_repository):
    # Prepare
    day_of_week = 1
    interval = Interval(900, 1600)
    timezone = "America/New_York"

    rate_1 = rate_factory.create(days_of_week=[1, 2, 3], period=Interval(900, 1600))
    rate_2 = rate_factory.create(days_of_week=[1, 5, 6], period=Interval(900, 1600))

    rates_repository.update_rates([rate_1, rate_2])

    # Execute
    found_rates = rates_repository.find_rate(day_of_week, interval, timezone)

    # Assert
    assert found_rates == [rate_1, rate_2]