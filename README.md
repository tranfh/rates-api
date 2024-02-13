## Rates API with Flask

### Description
This app is a simple Flask API that provides endpoints to retrieve and update rates. It also provides an endpoint to retrieve the price for a specific time range.

This folder structure has been divided into app and libs folders. 

The app folder contains the main application code, while the libs folder contains the helper functions and classes.

The purpose of this structure is to ensure that the code is modular and easy to maintain.

Code within the `app` folder is responsible for handling the API requests and responses.

Code within the `libs` folder is responsible for handling the business logic.

Within the `libs` folder there are two subfolders:
- rates: Contains the code to handle the rates data
  - dto: Contains the code to handle the data models
  - services: Contains the code to handle the business logic
  - repository: Contains the code to handle database interactions
- utils: Contains the code to handle any helper functions

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