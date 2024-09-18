from django.db import models
from .api import query_location_id
from django.utils import timezone

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

    def update(self):
        self._update_fields()
        self.save()

    def _update_fields(self):
        updates = query_location_id(self.place_id)
        self.address = updates['formattedAddress']
        self.contact_info = updates['internationalPhoneNumber']
        self.rating = updates['rating']
        self.name = updates['displayName']['text']
        self.cuisine_type = updates['editorialSummary']['text']
        self.last_update_date = timezone.now()
        #also need to update all the reviews

    @classmethod
    def get_or_init(_class, id):
        try:
            database_result = Location.objects.get(place_id=id)
            return database_result
        except Location.DoesNotExist:
            new_result = Location.objects.create(place_id=id)
            new_result.update()
            return new_result


class Review(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    score = models.IntegerField()
    user = models.CharField(max_length=128)
    date = models.DateTimeField()
    text = models.CharField(max_length=1024)

    def __str__(self):
        return self.user + " says " + self.text
