#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager
import flight_search
import user_search
import notification_manager


origin_airport = "LON"

DataManager = data_manager.DataManager()
sheet_data = DataManager.prices
print(sheet_data)

# # Add a user to the Database:
user_search.create_user()

# # If the IATA CODE is empty, find the IATA code:
for data in sheet_data:
    if data["iataCode"] == "":
        flight_search.get_IATA_code(data["city"], data["id"])
        print(data)

else:
    for data in sheet_data:
        flight = flight_search.structure_flight_data("LON",data["iataCode"], data["city"],data["lowestPrice"])
        if flight is None:
            continue
        if flight.price < data["lowestPrice"]:
            message = f"Price of the cheapest flight is: {flight.price} EUR, from {flight.origin_city}" +\
                       f" Airport:{flight.origin_airport}  to {flight.destination_city}, Airport:{flight.destination_airport}"
            print(message)
            users = user_search.get_users()
            print(users)
            users_emails_list = [row["email"] for row in users]
            print(users_emails_list)
            # Send notifications through email:
            NotificationManager = notification_manager.NotificationManager()
            NotificationManager.send_emails(email_list=users_emails_list,
                                            email_msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8'))
        else:
            print(f"There arent any CHEAP flights found! Try again later!")
            if flight.stop_overs > 0:
                print(f"Flight has {flight.stop_overs} at {flight.via_city}.")
