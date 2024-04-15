import requests
import datetime
import flight_data
import pprint
from dotenv import find_dotenv,load_dotenv
import os
env_path = find_dotenv()
load_dotenv(env_path)


sheety_endpoint = os.getenv("sheety_endpoint")

tequila_locations_endpoint = "https://api.tequila.kiwi.com/locations/query"

tequila_headers = {"apikey": os.getenv("apikey")}

tequila_search_endpoint = "https://api.tequila.kiwi.com/v2/search"

todays_date = datetime.date.today() + datetime.timedelta(days=1)
formated_date_today = todays_date.strftime("%d/%m/%Y")

max_return_date = todays_date + datetime.timedelta(days=30 * 8)
formated_max_return_date = max_return_date.strftime("%d/%m/%Y")


class FlightSearch:
    def __init__(self):
        self.test = "test"


def get_IATA_code(current_city, current_row):
    # This class is responsible for talking to the Flight Search API.
    flight_search_params = {"term": str(current_city),
                            "location_types": "city"}
    print(current_city)
    # # same with the previous project, you need to type the names as you see them in the json. For example:
    # # if you write iatacode instead of iataCode, the sheety gives you a 400 error code.
    flight_response = requests.get(url=tequila_locations_endpoint, headers=tequila_headers, params=flight_search_params)
    print(flight_response.status_code)
    print(flight_response.text)
    flight_result = flight_response.json()
    IATA_code = flight_result["locations"][0]["code"]
    print(IATA_code)
    json_data = {"price": {"iataCode": IATA_code}}
    response = requests.put(url=sheety_endpoint + str(current_row), json=json_data)
    print(response.status_code)
    print(response.text)


def structure_flight_data(departure_iata_code, destination_iata_code, destination_common_name, sheet_lowest_price):
    # # For getting destination_iata_code:
    # i tried main.sheet_data[city], because i thought city would return a number, so we could loop through the list.
    # That is not the case, we get the item in the list at index 0, so the dict that is:
    # {'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 54, 'id': 2} etc...
    # If we wanted to do the afformantioned, we would need a range function, e.g. for city in range(0,9) etc...
    tequila_params = {"fly_from": departure_iata_code, "fly_to": destination_iata_code,
                      "date_from": formated_date_today, "date_to": formated_max_return_date,
                      "curr": "EUR",
                      "price_to": sheet_lowest_price,
                      "nights_in_dst_from": 7, "nights_in_dst_to": 28,
                      "one_for_city": 1, "max_stopovers": 0
                      }
    response = requests.get(url=tequila_search_endpoint, params=tequila_params, headers=tequila_headers)
    print(tequila_params)
    print(response.status_code)
    print(response.text)

    try:
        # # Original Result
        result = response.json()
        print(result)
        number_of_cheap_flights = len(result["data"])
        cheapest_flight = result["data"][0]["price"]
    except IndexError:
        print(f"No flights found for {destination_common_name}.")
        increase_stopovers = input("Would you like to search for non-direct flights? Type Y or N:").capitalize()
        if increase_stopovers == "N":
            return None
        else:
            tequila_params["max_stopovers"] = 1
            response_2 = requests.get(url=tequila_search_endpoint, params=tequila_params, headers=tequila_headers)
            print(tequila_params)
            print(response_2.status_code)
            print(response_2.text)
            try:
                # # Backup Result
                result = response_2.json()["data"][0]
                pprint.pprint(result)
                cheapest_flight_data_obj = flight_data.FlightData(
                    price=result["price"],
                    origin_city=result["route"][0]["cityFrom"],
                    origin_airport=result["route"][0]["flyFrom"],
                    destination_city=result["route"][1]["cityTo"],
                    destination_airport=result["route"][1]["flyTo"],
                    out_date=result["route"][0]["local_departure"].split("T")[0],
                    return_date=result["route"][2]["local_departure"].split("T")[0],
                    stop_overs= 1,
                    via_city=result["route"][0]["cityTo"]
                )
                return cheapest_flight_data_obj

            except IndexError:
                print(f"No flights found for {destination_common_name} even with 1 stop-over!")
    else:
        cheapest_flight_data_obj = flight_data.FlightData(
            price=result["data"][0]["price"],
            origin_city=result["data"][0]["route"][0]["cityFrom"],
            origin_airport=result["data"][0]["route"][0]["flyFrom"],
            destination_city=result["data"][0]["route"][0]["cityTo"],
            destination_airport=result["data"][0]["route"][0]["flyTo"],
            out_date=result["data"][0]["route"][0]["local_departure"].split("T")[0],
            return_date=result["data"][0]["route"][0]["local_arrival"].split("T")[0]
        )
        print(f"Number of cheap flights found:{number_of_cheap_flights} for {destination_common_name}")
        # print(f"Price of the cheapest flight is:{cheapest_flight_data_obj.price} from {cheapest_flight_data_obj.origin_city}, Airport:{cheapest_flight_data_obj.origin_airport}  to {destination_common_name}, Airport:{cheapest_flight_data_obj.destination_airport}")
        return cheapest_flight_data_obj
