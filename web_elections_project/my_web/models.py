from django.db import models


class Voices (models.Model):
    voice_type = models.CharField(max_length=10, default='')
    author = models.CharField(max_length=999, default='Anonim')
    question = models.CharField(max_length=999)
    voice_picture = models.FileField(
        upload_to='images/',
        default='images/default_image.png'
    )


class Questions (models.Model):
    voice_id = models.IntegerField(default=0)
    voice_type = models.CharField(max_length=10, default='')
    answer_number = models.IntegerField(default=0)
    answer = models.CharField(max_length=999)
    date = models.DateField()


class Answers (models.Model):
    voice_id = models.IntegerField(default=0)
    answer_number = models.IntegerField(default=0)
    author = models.CharField(max_length=999, default='Anonim')
    answer = models.BooleanField(default=False)
    date = models.DateField()


# Create your models here.
