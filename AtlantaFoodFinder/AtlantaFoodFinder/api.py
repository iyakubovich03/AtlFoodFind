from .secrets import get_api_key
import requests

def url_location_id(id):
    # Reviews are very big, I'm not keeping them in here until I actually parse them correctly
    desiredInfo = ["displayName", "formattedAddress", "internationalPhoneNumber", "rating", "editorialSummary"]#, "reviews"]
    fields = ",".join(desiredInfo)
    return "https://places.googleapis.com/v1/places/" + id + "?fields=" + fields + "&key=" + get_api_key()

def query_location_id(id):
    return requests.get(url_location_id(id)).json()