from django.db import models
from .api import query_location_id, parse_date, parse_review_id_from_api_name
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    # All the ones I tested were length 27, but I'm being generous with field size
    # until we have more concrete information about a good max
    place_id = models.CharField(max_length=64, primary_key=True)
    address = models.CharField(max_length=512, default="")
    contact_info = models.CharField(max_length=512, default="")
    cuisine_type = models.CharField(max_length=256, default="")
    name = models.CharField(max_length=256, default="")
    last_update_date = models.DateTimeField(default=timezone.now)

    #Average rating, based on reviews
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def update_from_web(self):
        updates = query_location_id(self.place_id)
        self.address = updates['formattedAddress']
        self.contact_info = updates['internationalPhoneNumber']
        self.rating = updates['rating']
        self.name = updates['displayName']['text']
        self.cuisine_type = updates['editorialSummary']['text']
        self.last_update_date = timezone.now()
        for review_json in updates['reviews']:
            Review.add_if_not_in_db(self, review_json)
        self.save()

    @classmethod
    def get_or_init(_class, id):
        try:
            database_result = Location.objects.get(place_id=id)
            return database_result
        except Location.DoesNotExist:
            new_result = Location.objects.create(place_id=id)
            new_result.update_from_web()
            return new_result

    def display(self):
        return self.__str__()


class Review(models.Model):
    review_id = models.CharField(max_length=64, primary_key=True, default="")
    #Can be null since there's no good default. However, shouldn't ever be null
    #if the review is properly constructed
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0)
    user = models.CharField(max_length=128, default="")
    date = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=1024, default="")

    def __str__(self):
        return self.user + " says " + self.text

    def update_from_json(self, review_json):
        self.score = review_json['rating']
        self.text = review_json['text']['text']
        self.user = review_json['authorAttribution']['displayName']
        self.data = parse_date(review_json['publishTime'])
        self.save()

    @classmethod
    def add_if_not_in_db(_class, location, review_json):
        id = parse_review_id_from_api_name(review_json['name'])
        try:
            database_result = Review.objects.get(review_id=id)
        except Review.DoesNotExist:
            new_review = Review.objects.create(location=location, review_id=id)
            new_review.update_from_json(review_json)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    favorites = models.ManyToManyField(Location, blank=True)
    def add_favorite(self, location):
        self.favorites.add(location)
        self.save()

    def remove_favorite(self, location):
        self.favorites.remove(location)
        self.save()