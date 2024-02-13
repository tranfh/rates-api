import pytest
from unittest.mock import patch

from app import application
from libs.rates.dto import Rate


@pytest.fixture
def test_client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


@patch('libs.rates.rates_service.RatesService.update_rates')
def test_before_first_request(mock_update_rates, test_client, monkeypatch):
    # Mocking the existence of the rates.json file
    monkeypatch.setattr('os.path.exists', lambda x: True)

    response = test_client.get('/')
    assert response.status_code == 200
    mock_update_rates.assert_called_once()


def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


@patch('libs.rates.rates_service.RatesService.get_rates')
def test_get_rates(mock_get_rates, test_client):
    response = test_client.get('/rates')
    assert response.status_code == 200
    data = response.json
    assert 'rates' in data
    assert isinstance(data['rates'], list)
    mock_get_rates.assert_called_once()


@patch('libs.rates.rates_service.RatesService.update_rates')
def test_put_rates(mock_update_rates, test_client):
    input_data = {
        'rates': [
            {
                'days': 'mon,tues,thurs',
                'times': '0900-2100',
                'tz': 'America/Chicago',
                'price': 1500
            },
            {
                'days': 'fri,sat,sun',
                'times': '0900-2100',
                'tz': 'America/Chicago',
                'price': 2000
            }
        ]
    }
    response = test_client.put('/rates', json=input_data)
    assert response.status_code == 200
    data = response.json
    assert 'rates' in data
    assert isinstance(data['rates'], list)
    mock_update_rates.assert_called()
    expect_service_input = list(map(lambda rate: Rate.to_model(rate), input_data.get('rates')))

    # Extract arguments passed to update_rates method
    actual_args, _ = mock_update_rates.call_args

    # Convert arguments to Rate objects
    actual_rates = actual_args[0]

    # Check for deep equality of the lists
    assert len(actual_rates) == len(expect_service_input)
    for actual_rate, expected_rate in zip(actual_rates, expect_service_input):
        assert actual_rate.days_of_week == expected_rate.days_of_week
        assert actual_rate.period.start == expected_rate.period.start
        assert actual_rate.period.end == expected_rate.period.end
        assert actual_rate.timezone == expected_rate.timezone
        assert actual_rate.price == expected_rate.price


@patch('libs.rates.rates_service.RatesService.update_rates')
def test_put_rates_with_whitespace_in_days(mock_update_rates, test_client):
    input_data = {
        'rates': [
            {
                'days': ' mon,    tues,  thurs',
                'times': '0900-2100',
                'tz': 'America/Chicago',
                'price': 1500
            },
            {
                'days': ' fri,sat, sun    ',
                'times': '0900-2100',
                'tz': 'America/Chicago',
                'price': 2000
            }
        ]
    }
    response = test_client.put('/rates', json=input_data)
    assert response.status_code == 200
    data = response.json
    assert 'rates' in data
    assert isinstance(data['rates'], list)
    mock_update_rates.assert_called()
    expect_service_input = list(map(lambda rate: Rate.to_model(rate), input_data.get('rates')))

    # Extract arguments passed to update_rates method
    actual_args, _ = mock_update_rates.call_args

    # Convert arguments to Rate objects
    actual_rates = actual_args[0]

    # Check for deep equality of the lists
    assert len(actual_rates) == len(expect_service_input)
    for actual_rate, expected_rate in zip(actual_rates, expect_service_input):
        assert actual_rate.days_of_week == expected_rate.days_of_week
        assert actual_rate.period.start == expected_rate.period.start
        assert actual_rate.period.end == expected_rate.period.end
        assert actual_rate.timezone == expected_rate.timezone
        assert actual_rate.price == expected_rate.price


@patch('libs.rates.price_service.PriceService.get_price')
def test_prices(mock_get_price, test_client):
    mock_get_price.return_value = 1500

    response = test_client.get('/prices', query_string={
        'start': '2024-02-12T09:05:00-05:00',
        'end': '2024-02-12T12:00:00-05:00'
    })
    assert response.status_code == 200
    data = response.json
    assert 'price' in data
    assert data['price'] == 1500


@patch('libs.rates.price_service.PriceService.get_price')
def test_prices_equal_to_0_if_null(mock_get_price, test_client):
    mock_get_price.return_value = None

    response = test_client.get('/prices', query_string={
        'start': '2024-02-12T09:05:00-05:00',
        'end': '2024-02-12T12:00:00-05:00'
    })
    assert response.status_code == 200
    data = response.json
    assert 'price' in data
    assert data['price'] == 0


@pytest.mark.parametrize(
    "input_data, expected_error",
    [
        (
            {
                'rates': [
                    {
                        'days': 'random',
                        'times': '0900-2100',
                        'tz': 'America/Chicago',
                        'price': 1500
                    }
                ]
            },
            "Invalid value for 'days'"
        ),
        (
                {
                    'rates': [
                        {
                            'days': None,
                            'times': '0900-2100',
                            'tz': 'America/Chicago',
                            'price': 1500
                        }
                    ]
                },
                "Days of week are required"
        ),
        (
            {
                'rates': [
                    {
                        'days': 'mon',
                        'times': '',
                        'tz': 'America/Chicago',
                        'price': 1500
                    }
                ]
            },
            "Times is required. Must be in format 'HHMM-HHMM'"
        ),
        (
            {
                'rates': [
                    {
                        'days': 'mon',
                        'times': '0900',
                        'tz': 'America/Chicago',
                        'price': 1500
                    }
                ]
            },
            "Invalid value for 'times'. Must be in format 'HHMM-HHMM'"
        ),
        (
                {
                    'rates': [
                        {
                            'days': 'mon',
                            'times': '0900-1200',
                            'tz': '',
                            'price': 1500
                        }
                    ]
                },
                "Timezone is required"
        ),
        (
                {
                    'rates': [
                        {
                            'days': 'mon',
                            'times': '0900-1200',
                            'tz': 'America/Europe',
                            'price': 1500
                        }
                    ]
                },
                "Invalid value for 'tz'. Must be a string and a valid timezone"
        ),
        (
                {
                    'rates': [
                        {
                            'days': 'mon',
                            'times': '0900-1200',
                            'tz': 12,
                            'price': 1500
                        }
                    ]
                },
                "Invalid value for 'tz'. Must be a string and a valid timezone"
        ),
        (
                {
                    'rates': [
                        {
                            'days': 'mon',
                            'times': '0900-1200',
                            'tz': 'America/Toronto',
                            'price': '12'
                        }
                    ]
                },
                "Invalid value for 'price'. Must be an integer"
        ),
        (
                {
                    'rates': [
                        {
                            'days': 'mon',
                            'times': '0900-1200',
                            'tz': 'America/Toronto',
                            'price': None
                        }
                    ]
                },
                "Price is required"
        )
    ]
)
def test_put_rates_throws_error(test_client, input_data, expected_error):
    response = test_client.put('/rates', json=input_data)
    assert response.status_code == 400
    data = response.json
    assert 'error' in data
    assert data['error'] == expected_error
