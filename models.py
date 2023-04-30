from django.db import models
import datetime
import pytz

class Hotel(models.Model):
   name = models.CharField(max_length=50)
   type = models.CharField(max_length=20)
   country = models.CharField(max_length=20)
   city = models.CharField(max_length=20)
   address = models.CharField(max_length=100, null=True, default="Address")
   description = models.CharField(max_length=150, default="Description")
   pricerange = models.CharField(max_length=30, default="per night")
   image_url = models.CharField(max_length=255, default="img/otel.jpg")

class Room(models.Model):
   type = models.CharField(max_length=20)
   occupancy = models.CharField(max_length=10)
   price = models.BigIntegerField(default=10000)
   hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

class Booking(models.Model):
   date_of_booking = models.DateTimeField(auto_now=True)
   from_date = models.DateTimeField()
   to_date = models.DateTimeField()
   rooms = models.ManyToManyField(Room)

   def _get_amount(self):
       amount = 0
       days = (self.to_date - self.from_date).days
       for room in self.rooms.all():
           amount = amount + (int(room.price)*days)
       return amount

   def _get_valid_date(self):
       utc = pytz.utc
       if self.to_date < utc.localize(datetime.datetime.today()):
           return False
       else:
           return True

   amount = property(_get_amount)
   valid_date = property(_get_valid_date)
