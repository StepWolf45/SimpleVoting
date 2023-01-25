from django.db import models


class MultyVoiceHistory (models.Model):
    question = models.CharField(max_length=999)
    answer1 = models.CharField(max_length=999)
    answer2 = models.CharField(max_length=999)
    answer3 = models.CharField(max_length=999)
    answer4 = models.CharField(max_length=999)
    answer5 = models.CharField(max_length=999)


class VoiceHistory (models.Model):
    voice_id = models.IntegerField()
    username = models.CharField(max_length=999)

    answer1 = models.BooleanField()
    answer2 = models.BooleanField()
    answer3 = models.BooleanField()
    answer4 = models.BooleanField()
    answer5 = models.BooleanField()

    date = models.DateField()


# Create your models here.
