import requests
from pprint import pprint
from dotenv import find_dotenv, load_dotenv
import os

env_path = find_dotenv()
load_dotenv(env_path)

sheety_user_id = os.getenv("sheety_user_id")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        sheety_endpoint = f"https://api.sheety.co/{sheety_user_id}/flightDealsCopy/prices"
        # # Add user and pass here later:
        sheety_header = {}

        response_1 = requests.get(url=sheety_endpoint)
        # print(response_1.status_code)
        result_1 = response_1.json()
        # pprint(result_1)
        self.prices = result_1["prices"]
