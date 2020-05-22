import requests
import datetime

from config import API_COVID
from utils import slugify, iso_to_date
from data.country_flags import FLAGS


class CovidData:
    def __init__(self):
        ...

    def get_countries(self):
        url = API_COVID + "/countries"
        data = requests.get(url)
        countries_list = data.json()
        return countries_list

    def get_countries_string(self, update=False):
        if update:
            countries_list = [c["Country"] for c in self.get_countries()]
            sorted_countries_list = sorted(countries_list)
            sorted_countries_string = "\n".join(sorted_countries_list)
            with open("data/countries_list.txt", "w") as fout:
                fout.write(sorted_countries_string)
        else:
            with open("data/countries_list.txt") as fin:
                sorted_countries_string = fin.read()
        return sorted_countries_string

    def get_country_all_status(self, country):
        url = API_COVID + "/total/country/" + country
        data = requests.get(url)
        today_status = data.json()[-1]
        return today_status

    def get_current_status_string(self, country):
        status = self.get_country_all_status(country)
        if type(status) == dict:
            date = iso_to_date(status["Date"])
            status_as_string = f"""
📆 {date}

_ Coronavirus report from {status["Country"]}_ {FLAGS.get(status["Country"], "")}
🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠

Confirmed cases: {status["Confirmed"]}
Total deaths: {status["Deaths"]}
Recovered: {status["Recovered"]}

Active cases: {status["Active"]}
"""
        else:
            status_as_string = (
                "Didn't find anything. Is the *name of the country* correctly spelled?"
            )
        return status_as_string
