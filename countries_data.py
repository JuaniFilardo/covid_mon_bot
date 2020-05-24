import csv
import json
import utils
from data.country_flags import FLAGS


class CountriesData:
    def __init__(self):
        self.csv_filename = "data/covid19.csv"
        self.json_filename = "data/covid19.json"
        self.countries = {}
        self.headers = [
            "Position",
            "TotalCases",
            "NewCases",
            "TotalDeaths",
            "NewDeaths",
            "TotalRecovered",
            "ActiveCases",
            "Serious,Critical",
            "Total Cases/1M pop",
            "Deaths/1M pop",
            "TotalTests",
            "Tests/1M pop",
            "Population",
            "Continent",
        ]

    def create_countries_dict(self):
        """Reads the CSV and transforms it into a dictionary in which keys are 
        the country names, while each value is another dictionary with that 
        country's data.
        """
        countries = {}

        with open(self.csv_filename, newline="") as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                # print(r)
                # country = {h: r[h] for h in self.headers}
                country_name = utils.slugify(row["Country"])
                countries[country_name] = row

        self.countries = countries

    def dump_countries_dict(self):
        with open(self.json_filename, "w") as fout:
            json.dump(self.countries, fout, indent=2)
        print("Created new json file.")

    def set_countries_dict(self):
        with open(self.json_filename) as fin:
            self.countries = json.load(fin)

    def get_country(self, country_name):
        return self.countries.get(country_name, {})

    def get_report(self, country_name):
        country = self.get_country(country_name)

        if country.get("Country"):
            if country.get("ActiveCases") != "N/A":
                emojis = utils.get_virus_emoji(
                    utils.string_to_int(country.get("ActiveCases"))
                )
            else:
                emojis = "❓❓❓"
            position = (
                "World ranking: #" + country["Position"]
                if country.get("Position")
                else ""
            )
            cases_trend = self.get_cases_trend(country.get("NewCases"))
            deaths_trend = self.get_deaths_trend(country.get("NewDeaths"))

            cases_per_million = f"({country.get('Total Cases/1M pop')} per million)"
            deaths_per_million = f"({country.get('Deaths/1M pop')} per million)"

            if country.get("Tests/1M pop"):
                tests_per_million = f"They have performed {country.get('Tests/1M pop')} tests per million people."
            else:
                tests_per_million = f"Test data is not available."

            report = f"""
_COVID-19 Report for {country.get('Country')}_ {FLAGS.get(country.get('Country'),"")}

{emojis}

{position}

There are {country.get("ActiveCases")} active cases in {country.get("Country")}. {cases_trend}

Total cases: {country.get("TotalCases")} {cases_per_million}
Total deaths: {country.get("TotalDeaths")} {deaths_trend} {deaths_per_million}
Recovered: {country.get("TotalRecovered")}

{tests_per_million}
"""
        else:
            report = "Is the country name correctly spelled? Try /report USA"
        return report


    def get_cases_trend(self, new_cases):
        if not new_cases:
            return "There are no new reported cases yet."
        elif new_cases == "+1":
            return "So far, only one case has been reported today."
        else:
            return f"So far, {new_cases[1:]} more cases have been reported today."

    def get_deaths_trend(self, new_deaths):
        return f"({new_deaths})" if new_deaths else ""


if __name__ == "__main__":
    countries = CountriesData()
    countries.create_countries_dict()
    countries.dump_countries_dict()
    # countries.set_countries_dict()
    # print(countries.countries["argentina"])
