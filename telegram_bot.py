import requests

from config import TELEGRAM_SEND_MESSAGE_URL, BASE_TELEGRAM_URL
from covid_data import CovidData
from utils import slugify
from typing import Dict


class TelegramBot:

    BOT_URL = BASE_TELEGRAM_URL

    def prepare_response(self, data: Dict) -> Dict:
        chat_id = self.get_chat_id(data)
        parsed_message = self.parse_message(data)
        command = parsed_message.get("command")
        message = parsed_message.get("message")
        covid_data = CovidData()

        if command == "/start":
            answer = self.get_start_message()
        elif command == "/help" or command == "/help@covid_mon_bot":
            answer = self.get_help()
        elif command == "/stats" or command == "/stats@covid_mon_bot":
            if len(message):
                country = slugify(message)
                answer = covid_data.get_current_status_string(country)
            else:
                answer = "Which country do you want info from? Try /stats `Argentina` or /stats `AR`"
        elif command == "/countries" or command == "/countries@covid_mon_bot":
            answer = covid_data.get_countries_string()
        elif command is None or command == "":
            answer = "Hi! What can I do for you?"
        else:
            answer = "I'm sorry, but I didn't understand 😔"

        json_data = {"chat_id": chat_id, "text": answer, "parse_mode": "Markdown"}
        # covid_data.get_last_two_days()
        return json_data


    def get_start_message(self):
        return """Hi! You can try sending
/stats `<country_code>`
"""

    def get_help(self):
        return """
1️⃣ Get latest info from a country: `/stats <country_code>`
For example:
    `/stats us`
    `/stats United States`

Tip: the number between parenthesis will tell you the latest observed increase.

2️⃣ Get list of available countries: /countries
"""

    def get_chat_id(self, data):
        return data["message"]["chat"]["id"]

    def parse_message(self, data: Dict) -> Dict:
        try:
            split_message = data["message"]["text"].split(" ", 1)
            return {"command": split_message[0], "message": split_message[1]}
        except IndexError:
            return {"command": split_message[0], "message": ""}
        except KeyError:
            return {"command": "", "message": ""}

    def send_message(self, prepared_data):
        """Mandatory arguments: `chat_id` and `text`
        """
        prepared_data["text"] = prepared_data["text"][:4096]  # lest we exceed the limit
        message_url = self.BOT_URL + "/sendMessage"
        requests.post(message_url, json=prepared_data)

    @staticmethod
    def init_webhook(url):
        requests.get(url)
