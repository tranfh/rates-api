import json
import os

from flask import Flask, request, jsonify, g, render_template

from app.model.price_output import PriceOutput
from app.model.rate_output import RateOutput
from libs.rates import RatesService, PriceService, RatesRepository, Rate
from libs.utils.datetime_helper import isodate_to_datetime

application = Flask(__name__)
rate_repository = RatesRepository()
price_service = PriceService(rates_repository=rate_repository)
rate_service = RatesService(rates_repository=rate_repository)


@application.route('/')
def home():
    return render_template('index.html')


# Register the ingestion process to run before the first request
@application.before_request
def before_first_request():
    if not g.get('ingestion_completed', False):
        run_ingestion_process()
        g.ingestion_completed = True


def run_ingestion_process():
    print("Ingestion process running...")
    static_folder = application.static_folder
    file_path = os.path.join(static_folder, 'rates.json')

    if not os.path.exists(file_path):
        print("File not found.")
        return

    # Read and parse the JSON data from the file
    with open(file_path, 'r') as file:
        try:
            # Load JSON data from file
            rates_json = json.load(file)

            # Extract rates from JSON data and convert them into Rate objects
            rates_list = [Rate.to_model(rate) for rate in rates_json.get('rates')]

            # Update rates using the rate_service
            rate_service.update_rates(rates_list)

            print("Rates updated successfully.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        except Exception as e:
            print("Error occurred while ingesting rates:", e)
        finally:
            file.close()

    print("Ingestion process finished.")

@application.route('/rates', methods=['GET', 'PUT'])
def rates():
    if request.method == 'GET':
        rates_list = rate_service.get_rates()
        result = list(map(lambda rate: RateOutput.from_model(rate).to_json(), rates_list))
        return jsonify({"rates": result})

    elif request.method == 'PUT':
        try:
            # Convert rates to model objects using map
            rates_input = list(map(lambda rate: Rate.to_model(rate), request.json.get('rates', [])))

            # Update rates and convert them back to model objects using map
            rates_list = rate_service.update_rates(rates_input)
            result = list(map(lambda rate: RateOutput.from_model(rate).to_json(), rates_list))

            return jsonify({"rates": result})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return 'Method not allowed', 405


@application.route('/prices', methods=['GET'])
def prices():
    # Get start and end dates from query parameters
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Validate start and end dates
    if not start_date or not end_date:
        return jsonify({'error': 'Start and end date times are required'}), 400

    try:
        start = isodate_to_datetime(start_date)
        end = isodate_to_datetime(end_date)
        price = price_service.get_price(start, end)
        return PriceOutput(price).to_json()

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    application.run(port=5000, debug=True)

