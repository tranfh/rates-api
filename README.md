## Rates API with Flask
### Description
This app is a simple Flask API that provides endpoints to retrieve and update rates. It also provides an endpoint to retrieve the price for a specific time range.

This folder structure has been divided into app and libs folders. 

The app folder contains the main application code, while the libs folder contains the helper functions and classes.

The purpose of this structure is to ensure that the code is modular and easy to maintain.

Code within the `app` folder is responsible for handling the API requests and responses.

Code within the `libs` folder is responsible for handling the business logic.

Within the `libs` folder there are two sub-folders:
- rates: Contains the code to handle the rates data
  - dto: Contains the code to handle the data models
  - services: Contains the code to handle the business logic
  - repository: Contains the code to handle database interactions
- utils: Contains the code to handle any helper functions

---
### User Story
As a user I should be able to fetch and modify rates for a specific datetime range via an API call.

### Acceptance Criteria:
#### API Endpoints:
* The application must have two endpoints: rates and price.
* Both endpoints must be accessible via HTTP on port 5000.
* Responses from the API must be in JSON format.
* Load json file rates into database

#### Rates Endpoint:
* The rates endpoint should support PUT and GET methods.
* PUT method allows updating rate information by submitting a modified rates JSON.
* The submitted JSON overwrites the stored rates.
* The GET method returns the rates stored.

#### Price Endpoint:
* The price endpoint should support GET method.
* It should accept query parameters start and end, representing the start and end datetime of the parking duration in ISO-8601 format with timezones.
* The response should contain the calculated price.
* If the input datetime range spans more than one day, the API must return "unavailable".
* If the input datetime range spans multiple rates, the API must return "unavailable".
* Rates will not span multiple days.

#### Application Startup:
    * Rates should be specified in a JSON file and automatically loaded on application startup.
    * The format of the JSON file should match the structure that can be submitted to the rates endpoint.
    * The JSON file should contain initial rates and their respective

#### Documentation:
* There must be clear documentation explaining how to run the application.
* API endpoints must be thoroughly documented, including their usage and expected responses.

#### Testing:
* Unit tests must be in place to ensure the correctness of the application.
* Automated tests should cover various scenarios including valid and invalid inputs for both endpoints.
* Tests should be comprehensive to cover edge cases and expected behaviors.

---
## Installation
Open up a directory in which you would like to clone the repository and run the following command:
```
git clone git@github.com:tranfh/rates-api.git
```

Download and install Python 3.8 or higher from the [official website](https://www.python.org/downloads/).
Manage your Python virtual environments with [venv](https://docs.python.org/3/library/venv.html).
To install pyenv, run the following command:

macOS:
```
brew install pyenv
```
Linux:
```
curl https://pyenv.run | bash
```
Windows:
```
choco install pyenv-win
```
\
Navigate to the `RatesApi` directory and create a virtual environment by running the following command:
```
cd RatesApi
python -m venv venv
```

Activate the virtual environment by running the following command:
```
source venv/bin/activate
```

Install the required packages by running the following command:
```
pip install -r requirements.txt
```
---
### Usage
To run the app locally, execute the following command while inside the RatesApi directory:
```
python -m app.app
```

### API Endpoints
#### 1. Home
**URL**: /\
**Method**: GET\
**Description**: Displays a simple UI containing the API details.\
**Example**: http://127.0.0.1:5000/

#### 2. Get Rates
**URL**: /rates \
**Method**: GET \
**Description**: Retrieves a list of rates.\
**Example**: http://127.0.0.1:5000/rates
**Example Response**:
```
{
    "rates": [
        {
            "days": "mon,tues,wed,thurs,fri",
            "times": "0600-1800",
            "price": 1500
        },
        {
            "days": "sat,sun",
            "times": "0600-2000",
            "price": 2000
        }
    ]
}
```

#### 3. Update Rates
**URL**: /rates \
**Method**: PUT \
**Description**: Updates the rates with new data, overwriting existing data\
**Example**: http://127.0.0.1:5000/rates
**Example Request**:
```
{
    "rates": [
        {
            "days": "mon,tues,wed,thurs,fri",
            "times": "0600-1800",
            "price": 1500
        },
        {
            "days": "sat,sun",
            "times": "0600-2000",
            "price": 2000
        }
    ]
}
```


#### 4. Get Prices
**URL**: /prices \
**Method**: GET \
**Description**: Retrieves the price for a specific time range. \
**Parameters**: \
**start**: Start date and time (ISO 8601 format) \
**end**: End date and time (ISO 8601 format) \
**Example**: http://127.0.0.1:5000/prices?start=2024-02-12T09:05:00-05:00&end=2024-02-12T12:00:00-05:00
**Example Response**:
```
{
    "price": 4500
}
```
---
### Testing
To run the tests, execute the following command:
```
cd RatesApi
python -m pytest 
```
---
### Troubleshooting
If you encounter any issues, and you get access denied, navigate to [chrome://net-internals/#sockets]() and click "Flush socket pools" to clear the DNS cache.