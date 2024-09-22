from django.http import HttpResponse
from django.views import generic
from .models import Location
from django.shortcuts import render
import requests


from .secrets import get_api_key
import json
def index(request):
    print(Location.get_or_init("ChIJJ2iPNY27EmsR45MJL04zqTc"))
    return HttpResponse("Home page")

class LocationView(generic.DetailView):
    model = Location
    template_name = "AtlantaFoodFinder/location.html"

def search_restaurants(request):
   cuisine = request.POST.get('search_term', 'restaurant')
   if cuisine != "restaurant":
       cuisine+="_restaurant"

    # based on search bar (type of cuisine)
   api_key = get_api_key()
   radius = 5000
   api_url="https://places.googleapis.com/v1/places:searchNearby"


   data = {
     "includedTypes": [
       cuisine
     ],
     "maxResultCount": 10,
     "locationRestriction": {
       "circle": {
         "center": {
           "latitude": 33.7490,
           "longitude": -84.3880
         },
         "radius": radius
       }
     }
   }
   header = {
   "Content-Type": 'application/json',
   "X-Goog-Api-Key": api_key,
   "X-Goog-FieldMask": "places.displayName"
   }


   response = requests.post(api_url, headers=header, data=json.dumps(data))


   if response.status_code == 200:
       results = response.json()
   else:

       results = response.json()




   return render(request, 'AtlantaFoodFinder/results.html', {'results': results})
def my_html_view(request):
    return render(request, 'AtlantaFoodFinder/results.html')
