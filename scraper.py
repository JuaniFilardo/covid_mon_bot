import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict, Iterable


class Scraper:
    def __init__(self):
        self.target = "https://www.worldometers.info/coronavirus/"
        self.headers = [
            "Position",
            "Country",
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

    def get_soup(self) -> BeautifulSoup:
        page = requests.get(self.target)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    def get_table_from_soup(self, soup: BeautifulSoup) -> List[List[str]]:
        data = []
        table = soup.find(id="main_table_countries_today")
        data.append(self.headers)

        table_body = table.find("tbody")
        rows = table_body.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)
        return data

    def update_csv(self, data: Iterable, filename="data/covid19.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def scrape_and_save(self):
        soup = self.get_soup()
        table = self.get_table_from_soup(soup)
        self.update_csv(table)
        print("Saved new csv file.")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape_and_save()
