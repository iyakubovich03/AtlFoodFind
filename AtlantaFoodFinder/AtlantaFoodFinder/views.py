from django.http import HttpResponse
from django.views import generic
from .models import Location

def index(request):
    print(Location.get_or_init("ChIJJ2iPNY27EmsR45MJL04zqTc"))
    return HttpResponse("Home page")

class LocationView(generic.DetailView):
    model = Location
    template_name = "AtlantaFoodFinder/location.html"