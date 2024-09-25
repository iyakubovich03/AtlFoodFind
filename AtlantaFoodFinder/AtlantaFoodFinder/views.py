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


from .secrets import get_api_key
import json
def index(request):
    print(Location.get_or_init("ChIJJ2iPNY27EmsR45MJL04zqTc"))
    return HttpResponse("Home page")

def location_detail(request, pk):
    return render(request, 'AtlantaFoodFinder/location.html',
                  {'location': Location.get_or_init(pk), 'isFavorite': is_favorite(request, pk)})

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

#pk is key of the location
@login_required
def add_favorite(request, pk):
    if request.method != 'POST':
        return HttpResponse(405) #not allowed
    else:
        if hasattr(request.user, "account"):
            request.user.account.add_favorite(Location.get_or_init(pk))
        else:
            account = Account.objects.create(user=request.user)
            account.add_favorite(Location.objects.get_or_init(pk))
        return HttpResponseRedirect(reverse("location", kwargs={"pk":pk}))

@login_required
def remove_favorite(request, pk):
    if request.method != 'POST':
        return HttpResponse(405) #not allowed
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
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['<PASSWORD>'])
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("profile"))
        else:
            for msg in form.errors:
                print(msg)
            return render(request, "registration/register.html", {"form": form})

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
   "X-Goog-FieldMask": "places.displayName,places.name"
   }




   response = requests.post(api_url, headers=header, data=json.dumps(data))



   if response.status_code == 200:
       results = response.json()
   else:

       results = response.json()




   return render(request, 'AtlantaFoodFinder/results.html', {'results': results})
def my_html_view(request):
    return render(request, 'AtlantaFoodFinder/results.html')
