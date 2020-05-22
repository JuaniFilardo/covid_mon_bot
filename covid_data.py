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
        last_status = data.json()[-2:]
        return last_status

    def get_current_status_string(self, country):
        try:
            status = self.get_country_all_status(country)
            yesterday, today = status[0], status[1]

            date = iso_to_date(today["Date"])
            status_as_string = f"""
📆 {date}

_ Coronavirus report from {today["Country"]}_ {FLAGS.get(today["Country"], "")}
🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠🦠

Confirmed cases: {today["Confirmed"]} (+{today["Confirmed"] - yesterday["Confirmed"]})
Total deaths: {today["Deaths"]} (+{today["Deaths"] - yesterday["Deaths"]})
Recovered: {today["Recovered"]} (+{today["Recovered"] - yesterday["Recovered"]})

Active cases: {today["Active"]} ({self.get_active_cases_change(today["Active"], yesterday["Active"])})
"""
        except:
            status_as_string = (
                "Didn't find anything. Is the *name of the country* correctly spelled?"
            )
        return status_as_string

    def get_active_cases_change(self, today, yesterday):
        sign = "+" if today > yesterday else "-"
        return sign + str(abs(today - yesterday))
