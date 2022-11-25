from django.db import models

# Create your models here.
class Route:
    id = models.UUIDField(primary_key=True)
    lng = models.FloatField()
    lat = models.FloatField()
    datetime = models.DateTimeField()
    
    
    