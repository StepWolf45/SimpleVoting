from django.db import models


class MultyVoiceHistory (models.Model):
    question = models.CharField(max_length=999)
    answer1 = models.CharField(max_length=999)
    answer2 = models.CharField(max_length=999)
    answer3 = models.CharField(max_length=999)
    answer4 = models.CharField(max_length=999)
    answer5 = models.CharField(max_length=999)


# Create your models here.
