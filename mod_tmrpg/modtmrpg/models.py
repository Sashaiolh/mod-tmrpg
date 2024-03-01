from django.db import models

# Create your models here.

class Moder(models.Model):
    nickname = models.CharField(max_length=12)
    pex = models.CharField(max_length=12)

