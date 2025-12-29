from django.db import models
from django.db.models import Avg
import math
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to="events/", blank=True, null=True)

  
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0


    def average_rating_int(self):
        return math.floor(self.average_rating())

