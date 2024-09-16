from django.db import models
from .api import query_location_id
from django.utils import timezone

class Location(models.Model):
    # All the ones I tested were length 27, but I'm being generous with field size
    # until we have more concrete information about a good max
    place_id = models.CharField(max_length=64)
    address = models.CharField(max_length=512)
    contact_info = models.CharField(max_length=512)
    cuisine_type = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    last_update_date = models.DateTimeField

    #Average rating, based on reviews
    rating = models.FloatField()

    def __str__(self):
        return self.name

    def update(self):
        if self.place_id is not None:
            updates = query_location_id(self.place_id)
            self.address = updates['formattedAddress']
            self.contact_info = updates['internationalPhoneNumber']
            self.rating = updates['rating']
            self.name = updates['displayName']['text']
            self.cuisine_type = updates['editorialSummary']['text']
            self.last_update_date = timezone.now()
            self.save()
            #also need to update all the reviews


class Review(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    score = models.IntegerField()
    user = models.CharField(max_length=128)
    date = models.DateTimeField()
    text = models.CharField(max_length=1024)

    def __str__(self):
        return self.user + " says " + self.text
