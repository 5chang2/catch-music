from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)


class User(models.Model):
    is_host = models.BooleanField()
    score = models.IntegerField(default=0)
    username = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)