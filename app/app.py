import json
import logging
import os

from flask import Flask, request, jsonify, g, render_template

from app.model import PriceOutput, RateOutput
from libs.rates.dto import Rate
from libs.rates import RatesService, PriceService, RatesRepository
from libs.utils.datetime_helper import isodate_to_datetime

ingestion_completed = False

application = Flask(__name__)
rate_repository = RatesRepository()
price_service = PriceService(rates_repository=rate_repository)
rate_service = RatesService(rates_repository=rate_repository)

# Set up logging
application.logger.setLevel(logging.DEBUG)



@application.route('/')
def home():
    return render_template('index.html')


@application.before_request
def before_first_request():
    """
    Runs the ingestion process before the first request if not already completed.
    """
    global ingestion_completed
    if not ingestion_completed:
        ingest_rates()
        ingestion_completed = True


def ingest_rates():
    """
    Runs the ingestion process to update rates from a JSON file.
    """
    application.logger.info("Ingestion process running")

    static_folder = application.static_folder
    file_path = os.path.join(static_folder, 'rates.json')

    if not os.path.exists(file_path):
        application.logger.warning("File not found. Could not ingest rates.")
        return

    # Read and parse the JSON data from the file
    with open(file_path, 'r') as file:
        try:
            # Load JSON data from file
            rates_json = json.load(file)

            # Extract rates from JSON data and convert them into Rate objects
            rates_list = [Rate.to_model(rate) for rate in rates_json.get('rates', [])]

            # Update rates using the rate_service
            rate_service.update_rates(rates_list)

            application.logger.info("Rates updated successfully.")
        except json.JSONDecodeError as e:
            application.logger.error("Error decoding JSON:", e)
        except Exception as e:
            application.logger.error("Error occurred while ingesting rates:", e)
        finally:
            file.close()

    application.logger.info("Ingestion process finished.")


@application.route('/rates', methods=['GET', 'PUT'])
def rates():
    """
     Retrieves or updates rates based on the HTTP request method.

     For GET requests, retrieves a list of rates.
     For PUT requests, updates the rates with new data.

     Returns:
     JSON response with rates or error message.
     """
    if request.method == 'GET':
        application.logger.info("Fetching all rates...")
        rates_list = rate_service.get_rates()
        result = [RateOutput.from_model(rate).to_json() for rate in rates_list]
        return jsonify({"rates": result})

    elif request.method == 'PUT':
        application.logger.warning("Overwriting existing rates with new rates...")
        try:
            # Convert rates to model objects using map
            if isinstance(request.json, str):
                data: dict = json.loads(request.json)
            else:
                data: dict = request.json

            rates_input = [Rate.to_model(rate) for rate in data.get('rates', [])]

            # Update rates and convert them back to model objects using map
            rates_list = rate_service.update_rates(rates_input)
            result = [RateOutput.from_model(rate).to_json() for rate in rates_list]

            return jsonify({"rates": result})
        except ValueError as e:
            application.logger.error("Error updating rates: %s", e)
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            application.logger.error("Error updating rates: %s", e)
            return jsonify({'error': str(e)}), 400
    else:
        application.logger.error("Method not allowed.")
        return 'Method not allowed', 405


@application.route('/prices', methods=['GET'])
def prices():
    """
    Endpoint to retrieve the price for a specific time range.

    Retrieves start and end dates from query parameters, validates them,
    and calculates the price using the PriceService. Returns the price
    in JSON format.

    Returns:
        JSON response containing the price or an error message.
    """
    # Get start and end dates from query parameters
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')

    application.logger.info(f"Fetching price for start: {start_date} and end: {end_date}")

    # Validate start and end dates
    if not start_date or not end_date:
        return jsonify({'error': 'Start and end date times are required'}), 400

    try:
        # Convert start and end dates to datetime objects
        start = isodate_to_datetime(start_date)
        end = isodate_to_datetime(end_date)

        # Get the price for the specified time range
        price = price_service.get_price(start, end)

        # Return the price in JSON format
        return PriceOutput(price).to_json()

    except ValueError as e:
        application.logger.error("Error fetching prices:", e)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        application.logger.error("Error fetching prices:", e)
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    application.run(port=5000)
