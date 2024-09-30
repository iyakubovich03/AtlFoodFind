from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Location, Account
from django.shortcuts import render
import requests
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from geopy.distance import geodesic
from django.http import JsonResponse

from .secrets import get_api_key
import json
def index(request):
    return render(request, "AtlantaFoodFinder/homepage.html")

def location_detail(request, pk):
    api_key = get_api_key()

    return render(request, 'AtlantaFoodFinder/location.html',
                  {'location': Location.get_or_init(pk), 'isFavorite': is_favorite(request, pk), "api_key": api_key})

def is_favorite(request, pk):
    if hasattr(request.user, "account"):
        if request.user.account.favorites.contains(Location.get_or_init(pk)):
            return True
    return False

class UserView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "AtlantaFoodFinder/profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['favorites_empty'] = self.favorites_empty(self.request.user)
        return context

    def favorites_empty(self, user):
        if not hasattr(user, "account"):
            return True
        else:
            favorites = user.account.favorites.all()
            if len(favorites) == 0:
                return True
            else:
                return False


#pk is key of the location
@login_required
def add_favorite(request, pk):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("location", kwargs={"pk":pk}))
    else:
        if hasattr(request.user, "account"):
            request.user.account.add_favorite(Location.get_or_init(pk))
        else:
            account = Account.objects.create(user=request.user)
            account.add_favorite(Location.get_or_init(pk))
        return HttpResponseRedirect(reverse("location", kwargs={"pk":pk}))

@login_required
def remove_favorite(request, pk):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("location", kwargs={"pk":pk}))
    else:
        if hasattr(request.user, "account"):
            request.user.account.remove_favorite(Location.get_or_init(pk))
            # no else condition since don't need to create an account if they just want to remove
        return HttpResponseRedirect(reverse("location", kwargs={"pk":pk}))

def account_creation(request):
    if request.method != 'POST':
        return render(request, "registration/register.html", {"form":UserCreationForm})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        else:
            return render(request, "registration/register.html", {"form": form})


def search_restaurants(request):
   cuisine = request.POST.get('search_term', 'restaurant')
   rating=request.POST.get('rating')
   location=request.POST.get('location')
   if cuisine != "restaurant":
       cuisine+="_restaurant"

    # based on search bar (type of cuisine)
   api_key = get_api_key()
   radius = 5000
   api_url="https://places.googleapis.com/v1/places:searchText"

   data = {
       "textQuery": cuisine,
       "locationBias": {
           "circle": {
               "center": {
                   "latitude": 33.7490,
                   "longitude":  -84.3880
               },
               "radius": 500.0
           }
       }
   }
   header = {
   "Content-Type": 'application/json',
   "X-Goog-Api-Key": api_key,
   "X-Goog-FieldMask": "places.displayName,places.name,places.rating,place.location"
   }




   response = requests.post(api_url, headers=header, data=json.dumps(data))



   if response.status_code == 200:
       results = response.json()
   else:

       results = response.json()
       return results

    newData=[]

    #cant iterate?
    for po in results.get('places', []):
        latitude = po.get('location').get('latitude')
        longitude = po.get('location').get('longitude')
        user_location = (33.7490, -84.3880)
        restaurant_location = (latitude, longitude)
        distance = geodesic(user_location, restaurant_location).kilometers
        newData.append({
            'name': po.get('displayName').get('text'),
            'placeId': po.get('name'),
            'rating': po.get('rating'),
            'distance_km': distance,
        })
    if rating and location:
        #add to this figure out
        return render(request, 'AtlantaFoodFinder/results.html',
                          {'search_text': request.POST.get('search_term'), 'results': obj})
    elif rating:
        sorted_by_distance = sorted(newData, key=lambda x: x['rating'])
        obj = JsonResponse(sorted_by_distance, safe=False)
        return render(request, 'AtlantaFoodFinder/results.html',
                         {'search_text': request.POST.get('search_term'), 'results': obj})
    elif location:
        sorted_by_distance = sorted(newData, key=lambda x: x['rating'])
        obj = JsonResponse(sorted_by_distance, safe=False)
        return render(request, 'AtlantaFoodFinder/results.html',{'search_text': request.POST.get('search_term'), 'results': obj})
    else:
        obj=JsonResponse(newData, safe=False)
        return render(request, 'AtlantaFoodFinder/results.html',{'search_text': request.POST.get('search_term'), 'results':obj})



