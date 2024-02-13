## Rates API with Flask

### Description
This app is a simple Flask API that provides endpoints to retrieve and update rates. It also provides an endpoint to retrieve the price for a specific time range.

### Installation
To install the required dependencies, run the following command:


`pip install -r requirements.txt`

### Usage
To run the app locally, execute the following command:
```
cd RatesApi
python -m app.app
```

### API Endpoints
#### 1. Home
**URL**: /\
**Method**: GET\
**Description**: Displays a simple greeting message.\
**Example**: http://127.0.0.1:5000/

#### 2. Get Rates
**URL**: /rates \
**Method**: GET \
**Description**: Retrieves a list of rates.\
**Example**: http://127.0.0.1:5000/rates

#### 3. Update Rates
**URL**: /rates \
**Method**: PUT \
**Description**: Updates the rates with new data, overwriting existing data\
**Example**: http://127.0.0.1:5000/rates

#### 4. Get Prices
**URL**: /prices \
**Method**: GET \
**Description**: Retrieves the price for a specific time range. \
**Parameters**: \
**start**: Start date and time (ISO 8601 format) \
**end**: End date and time (ISO 8601 format) \
Example: http://127.0.0.1:5000/prices?start=2024-02-12T09:05:00-05:00&end=2024-02-12T12:00:00-05:00

### Testing
To run the tests, execute the following command:
```
cd RatesApi
python -m pytest 
```

### Troubleshooting
If you encounter any issues, and you get an access denied, navigate to [chrome://net-internals/#sockets]() and click "Flush socket pools" to clear the DNS cache.