from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User


class Film(models.Model):
    gernes = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=50, default='')
    storyline = models.TextField(default='')
    stars = models.CharField(max_length=255)
    creators = models.CharField(max_length=255)
    languages = models.CharField(max_length=100)
    release_date = models.DateField()
    run_time = models.IntegerField(help_text="Enter run length in minutes")
    trailer = EmbedVideoField()
    poster = models.ImageField(null=True, blank=True, upload_to='media')
    production_companies=models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Auditorium(models.Model):
    code=models.CharField(max_length=50, default='')
    description=models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Seat(models.Model):
    code=models.CharField(max_length=10, default='')
    auditorium= models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.fullname


class ShowTime(models.Model):
    time = models.TimeField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return str(self.time) + '-' + str(self.film)


class Booking(models.Model):
    time=models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'time',
            'customer',
            'seat',
        )