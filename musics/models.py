from django.db import models

# Create your models here.
class Music(models.Model):
    singer = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    youtube_url = models.CharField(max_length=100)