from django.db import models
from django.db.models.signals import post_init
from django_random_id_model import RandomIDModel
import random

# Create your models here.

class Moder(RandomIDModel):
    nickname = models.CharField('никнейм', unique=True, max_length=12)
    pex = models.ForeignKey("Pex", on_delete=models.CASCADE)
    balance = models.IntegerField('баланс', default=0)
    discord = models.ForeignKey("Discord", on_delete=models.SET_NULL, blank=True, null=True)
    is_registered = models.BooleanField('Зарегистрирован', default=False)
    is_admin = models.BooleanField('is_admin', default=False)

    def __str__(self):
        return f'[{self.pex.display_name}] {self.nickname} | id: {self.id}'


class Pex(models.Model):
    hierarchy = models.IntegerField('высота должности', default=1)
    pex_name = models.CharField('pex', max_length=12)
    display_name = models.CharField('display_name', max_length=12)
    prefix_color = models.CharField('цвет префикса', max_length=12)
    nickname_color = models.CharField('цвет ника',max_length=12)

    def __str__(self):
        return self.display_name


class Discord(models.Model):
    ds_id = models.IntegerField()
    username = models.CharField(max_length=12)
    avatar = models.TextField('аватарка', blank=True, default='')
    global_name = models.CharField(max_length=12)

    def __str__(self):
        return self.global_name
    

class RegisterFormModel(models.Model):
    secret_code = models.IntegerField()
    password1 = models.CharField(max_length=16)
    password2 = models.CharField(max_length=16)

    def __str__(self):
        return self.secret_code
    
class Item(models.Model):
    item_name = models.CharField('название',max_length=16)
    description = models.TextField('описание')
    note = models.CharField('примечание',max_length=35)
    price = models.IntegerField('цена')
    # image = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='items/')
    type = models.IntegerField()
    # 0 - items
    # 1 - cases
    # 2 - privki
    def __str__(self):
        return self.item_name
    
class MediaCategory(models.Model):
    category_name = models.CharField('название',max_length=12)
    category_folder = models.CharField('путь',max_length=12)
    def __str__(self):
        return f'{self.category_name} | {self.category_folder}'
    
class MediaItem(models.Model):
    media_name = models.CharField('название', max_length=16)
    media_file = models.ImageField(upload_to ='items/')
    category = models.ForeignKey("MediaCategory", on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.media_name} | {self.id}'