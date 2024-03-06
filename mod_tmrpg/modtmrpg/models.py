from django.db import models
from django.db.models.signals import post_init
from django_random_id_model import RandomIDModel
import random

# Create your models here.

class Pex(models.Model):
    hierarchy = models.IntegerField('высота должности', default=1)
    pex_name = models.CharField('pex', max_length=12, unique=True)
    display_name = models.CharField('display_name', max_length=12)
    prefix_color = models.CharField('цвет префикса', max_length=12)
    nickname_color = models.CharField('цвет ника',max_length=12)

    def __str__(self):
        return self.display_name
    
class Moder(RandomIDModel):
    nickname = models.CharField('никнейм', unique=True, max_length=12)
    pex = models.ForeignKey("Pex", to_field='pex_name', default='helper1' , on_delete=models.CASCADE)
    balance = models.IntegerField('баланс', default=0)
    discord = models.ForeignKey("Discord", on_delete=models.SET_NULL, blank=True, null=True)
    is_registered = models.BooleanField('Зарегистрирован', default=False)
    skin_valid = models.BooleanField('Подгрузился ли скин?', default=False)
    head_valid = models.BooleanField('Подгрузилась ли голова?', default=False)

    def __str__(self):
        return f'[{self.pex.display_name}] {self.nickname} | id: {self.id}'
    
    def is_st(self):
        return self.pex.pex_name == "StModer" or self.pex.pex_name == "gm" or self.pex.pex_name == "gd"
    def is_admin(self):
        return self.pex.pex_name == 'curator' or self.pex.pex_name == "techadmin" or self.pex.pex_name == "admin"


class EcoLog(models.Model):
    admin = models.ForeignKey("Moder", null=True, blank=True, on_delete=models.CASCADE, related_name='admin')   
    moder = models.ForeignKey("Moder", null=True, on_delete=models.CASCADE, related_name='moder')   
    amount = models.IntegerField('Количество')
    reason = models.CharField('Причина', max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    def getDate(self):
        return self.date.strftime("%d %b %Y")
    def __str__(self):
        t = f'+{self.amount}' if self.amount>0 else self.amount
        if self.admin:
            return f'[{self.admin.pex.display_name}] {self.admin.nickname} --> {t} --> [{self.moder.pex.display_name}] {self.moder.nickname}'
        return f'[Shop --> {t} --> [{self.moder.pex.display_name}] {self.moder.nickname}'
    class Meta:
        ordering = ['-date']


class Discord(models.Model):
    ds_id = models.IntegerField()
    username = models.CharField(max_length=12)
    avatar = models.TextField('аватарка', blank=True, default='')
    global_name = models.CharField(max_length=12)

    def __str__(self):
        return self.global_name
    

class RegisterFormModel(models.Model):
    secret_code = models.IntegerField()
    password1 = models.CharField('Придумайте пароль',max_length=16)
    password2 = models.CharField('Повторите пароль',max_length=16)

    def __str__(self):
        return self.secret_code
    
class Item(models.Model):
    item_name = models.CharField('название',max_length=31)
    description = models.CharField('описание', blank=True, max_length=30)
    note = models.CharField('примечание', blank=True, max_length=35)
    price = models.IntegerField('цена')
    # image = models.CharField(max_length=100)
    image = models.ImageField('картинка',upload_to ='items/', blank=True,  null=True)
    image_url = models.TextField('Путь либо ссылка на картинку',blank=True, null=True)
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
    media_name = models.CharField('название', max_length=30)
    media_file = models.ImageField(upload_to ='items/')
    category = models.ForeignKey("MediaCategory", on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.media_name} | {self.id}'