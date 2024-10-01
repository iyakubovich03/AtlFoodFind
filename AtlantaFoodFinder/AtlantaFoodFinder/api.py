from .secrets import get_api_key
import requests
from datetime import datetime

def url_location_id(id):
    # Reviews are very big, I'm not keeping them in here until I actually parse them correctly
    desiredInfo = ["displayName", "formattedAddress", "internationalPhoneNumber", "rating", "editorialSummary", "reviews", "location"]
    fields = ",".join(desiredInfo)
    return "https://places.googleapis.com/v1/places/" + id + "?fields=" + fields + "&key=" + get_api_key()

def query_location_id(id):
    return requests.get(url_location_id(id)).json()

#Parse string date to django datetime
def parse_date(string_datetime):
    halves = string_datetime.split("T")
    date = halves[0]
    time = halves[1]
    date_components = date.split("-")
    year = int(date_components[0])
    month = int(date_components[1])
    day = int(date_components[2])
    time_components = time[0:-1].split(":") #Remove last character since is always Z
    hour = int(time_components[0])
    minutes = int(time_components[1])
    seconds = int(float(time_components[2]))
    datetime_result = datetime(year, month, day, hour, minutes, seconds)
    return datetime_result

#Parse the name field of each review to its review id
def parse_review_id_from_api_name(api_name):
    return api_name.split("/")[-1]
