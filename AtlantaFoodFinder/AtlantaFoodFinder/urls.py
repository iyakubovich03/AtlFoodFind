"""
URL configuration for AtlantaFoodFinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import admin
from . import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("locations/<pk>/", views.location_detail, name="location"),
    path("places/", views.search_restaurants, name="results"),
    #path("search/", views.search_restaurants(request), name="search")
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.UserView.as_view(), name="profile"),
    path("locations/<pk>/addFavorite", views.add_favorite, name="addFavorite"),
    path("locations/<pk>/removeFavorite", views.remove_favorite, name="removeFavorite"),
]
