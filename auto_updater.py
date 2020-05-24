import time
from scraper import Scraper
from countries_data import CountriesData


def main():
    while True:
        print("-" * 80)
        print(time.asctime())
        scraper = Scraper()
        scraper.scrape_and_save()

        countries = CountriesData()
        countries.create_countries_dict()
        countries.dump_countries_dict()

        print("See you in 15 minutes!")
        time.sleep(900)


if __name__ == "__main__":
    main()
