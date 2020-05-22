import re
import datetime
import json

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
