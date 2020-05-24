import re
import datetime
import json
import math

non_url_safe = [
    '"',
    "#",
    "$",
    "%",
    "&",
    "+",
    ",",
    "/",
    ":",
    ";",
    "=",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "`",
    "{",
    "|",
    "}",
    "~",
    "'",
]

non_url_safe_regex = re.compile(
    r"[{}]".format("".join(re.escape(x) for x in non_url_safe))
)


def slugify(text):
    text = non_url_safe_regex.sub("", text).strip()
    text = u"-".join(re.split(r"\s+", text))
    return text.lower()


def iso_to_date(isodate):
    isodate = isodate.split("Z")[0]
    return datetime.datetime.fromisoformat(isodate).date().strftime("%A %d. %B %Y")


def get_virus_emoji(active_cases):
    virus_emoji = "🦠"
    clap_emoji = "👏"
    if active_cases > 3:
        return virus_emoji * int(math.log(active_cases))
    return clap_emoji


def string_to_int(value):
    try:
        return int(value.replace(",", ""))
    except:
        return 0


def translate_country(country_name):
    """Tries to account for the fact that there's different ways to
    write the name of the same country, and the slugification alone 
    doesn't not standardise it. Also, it'll be of help to some spanish users.
    """
    translation_dict = {
        "us": "usa",
        "united-states": "usa",
        "united-states-of-america": "usa",
        "estados-unidos": "usa",
        "eeuu": "usa",
        "united-kingdom": "uk",
        "great-britain": "uk",
        "arg": "argentina",
        "ar": "argentina",
        "brasil": "brazil"
    }
    return translation_dict.get(country_name, country_name)