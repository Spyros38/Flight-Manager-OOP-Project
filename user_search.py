import requests
from dotenv import find_dotenv,load_dotenv
import os

env_path = find_dotenv()
load_dotenv(env_path)

sheety_endpoint_2 = os.getenv("sheety_endpoint_2")


def create_user():

    logic_switch = True
    user_first_name = input("Please enter your First Name:").title()
    user_last_name = input("Please enter your Last Name:").title()
    user_email = input("Please enter your Email:").lower()
    user_email_check = input("Please enter your Email, again:").lower()

    response_1 = requests.get(url=sheety_endpoint_2)
    result_1 = response_1.json()
    # print(response_1.json())
    # print(response_1.text)

    for person in result_1["users"]:
        if user_email in person["email"]:
            print("You are already in our database!")
            logic_switch = False
            return logic_switch
    if user_email == user_email_check and logic_switch is True:
        # # Notice the camel case that is used in the header - column name:
        sheety_parameters = {"user": {"firstName": user_first_name,
                                      "lastName": user_last_name,
                                      "email": user_email
                                      }
                             }

        response_2 = requests.post(url=sheety_endpoint_2, json=sheety_parameters)
        print(response_2.status_code)
        print(response_2.text)
        response_2.json()
    else:
        print("Sorry, your email address does not match!")


def get_users():
    response_3 = requests.get(url=sheety_endpoint_2)
    all_customer_data_list = response_3.json()["users"]
    print(all_customer_data_list)
    return all_customer_data_list
