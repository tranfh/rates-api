## Rates API with Flask
https://github.com/tranfh/rates-api

### Description
This app is a simple Flask API that provides endpoints to retrieve and update rates. It also provides an endpoint to retrieve the price for a specific time range.

This folder structure has been divided into app and libs folders. 

For the purpose of this project, the database is a simple in-memory database. In a production environment, this would be replaced with a proper database such as PostgreSQL or a NoSQL db.
Docker would be used to containerize the app and the database.
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
* The JSON file should contain initial rates

#### Future improvement considerations:
* Use Sqlalchemy to manage orm models using flask-sqlalchemy
* Set up a postgres DB using psycopg2 library
* Create a docker-compose.yml for defining and running multi-container Docker applications
* Caching
* Rate Limiting
* Authentication


---

## File Structure

### app
- app.py: 
  - Main application file
  - Contains the Flask app and the routes 
- models: 
  - Contains the data models
  - output object classes are defined here to standardize the response 
- static: 
  - Contains the rates.json file
- templates: 
  - Contains the HTML file for the UI
- tests: 
  - Contains the test files
---
### libs
- rates: 
  - Contains the code to handle the rates data
  - dto: 
    - Contains the code to handle the data models
  - services: 
    - Contains the code to handle the business logic
    - price and rates services are decoupled to their respective use cases
  - repository: 
    - Contains the code to handle database interactions
---

## Installation
Open up a directory in which you would like to clone the repository and run the following command:
```
cd rates-api
git clone git@github.com:tranfh/rates-api.git
```

Download and install Python 3.8 or higher from the [official website](https://www.python.org/downloads/).

---
Manage your Python virtual environments with [venv](https://docs.python.org/3/library/venv.html).

This step is **optional**. If you don't wish to separate your python versions, you can skip this step.

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


Install a python version using pyenv:
```
pyenv install 3.11.4
```

Set the python version for the project:
```
pyenv local 3.11.4
```


Navigate to the `rates-api` directory and create a virtual environment by running the following command:
```
cd rates-api
python -m venv venv
```

Activate the virtual environment by running the following command:
```
source venv/bin/activate
```

---

Once you have python installed, and are in the project directory, install the required packages by running the following command:
```
pip install -r requirements.txt
```

---

### Usage
To run the app locally, execute the following command while inside the RatesApi directory:
```
python -m app.app
```

Navigate to http://127.0.0.1:5000/ in your web browser to view the API view.

Upon loading the application, before the first request is made a JSON file containing rates located at `app/static/rates.json` will be loaded into the database.
The file must be named `rates.json` and contain the following structure:
```
{
    "rates": [
        {
            "days": "mon,tues,wed,thurs,fri",
            "times": "0600-1800",
            "price": 1500,
            "timezone": "America/New_York"
        },
        {
            "days": "sat,sun",
            "times": "0600-2000",
            "price": 2000,
            "timezone": "America/New_York"
        }
    ]
}
```

On the right hand side of the view you can interact with the API endpoints through the inputs.

Click on the request button to change the request method type (GET, PUT, POST).

Change the url accordingly and click on `Submit` to execute the request.

For the PUT rates request, you can update the rates by clicking on the `Request Body` textarea and providing an array of rates in the JSON format, similar to the `rates.json` file.

![img.png](img.png)

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
**Example**: http://127.0.0.1:5000/rates \
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

If the input datetime range spans more than one day, or the input datetime overlaps multiple rates the API must return:
```
{
    "price": "unavailable"
}
```


---
### Testing
To run the tests, execute the following command:
```
cd rates-api
python -m pytest 
```
---
### Troubleshooting
If you encounter any issues, and you get access denied, navigate to [chrome://net-internals/#sockets]() and click "Flush socket pools" to clear the DNS cache.