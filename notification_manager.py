import smtplib
from dotenv import find_dotenv,load_dotenv
import os

env_path = find_dotenv()
load_dotenv(env_path)

my_email = os.getenv("my_email")
password = os.getenv("password")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def send_emails(self, email_list, email_msg):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,to_addrs=email_list,msg=email_msg)
            connection.close()
