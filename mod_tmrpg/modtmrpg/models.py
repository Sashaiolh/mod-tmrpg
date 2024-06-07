from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_init
from django_random_id_model import RandomIDModel
import random

# Create your models here.

class Pex(models.Model):
    hierarchy = models.IntegerField('высота должности', default=1)
    pex_name = models.CharField('pex', max_length=12, unique=True)
    display_name = models.CharField('display_name', max_length=15)
    prefix_color = models.CharField('цвет префикса', max_length=12)
    nickname_color = models.CharField('цвет ника',max_length=12)
    OC_nickname_color = models.CharField('Цвет ника в компе', default='#383838',max_length=12)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return f'{self.pex_name} | {self.display_name} | {self.prefix_color}'
    
class Moder(RandomIDModel):
    nickname = models.CharField('никнейм', unique=True, max_length=32)
    pex = models.ForeignKey("Pex", to_field='pex_name', default='helper1' , on_delete=models.CASCADE)
    balance = models.IntegerField('баланс', default=0)
    discord = models.ForeignKey("Discord", on_delete=models.SET_NULL, blank=True, null=True)
    is_registered = models.BooleanField('Зарегистрирован', default=False)
    skin_valid = models.BooleanField('Подгрузился ли скин?', default=False)
    head_valid = models.BooleanField('Подгрузилась ли голова?', default=False)

    def __str__(self):
        return f'[{self.pex.display_name}] {self.nickname} | id: {self.id}'
    
    class Meta:
        ordering = ['-pex__hierarchy']
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"
    
    def is_st(self):
        return self.pex.pex_name == "StModer" or self.pex.pex_name == "gm" or self.pex.pex_name == "gd" or self.pex.pex_name == "techadmin"
    def is_admin(self):
        return self.pex.pex_name == 'curator' or self.pex.pex_name == "admin"
    
    def get_all_reprimands(self):
        return Reprimand.objects.filter(moder=self)


class EcoLog(models.Model):
    admin = models.ForeignKey("Moder", null=True, blank=True, on_delete=models.CASCADE, related_name='admin')   
    moder = models.ForeignKey("Moder", null=True, on_delete=models.CASCADE, related_name='moder')   
    amount = models.IntegerField('Количество')
    reason = models.TextField('Причина')
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
        verbose_name = "Лог экономики"
        verbose_name_plural = "Логи экономики"


class Reprimand(models.Model):
    admin = models.ForeignKey("Moder", null=True, on_delete=models.CASCADE, related_name='modtmrpg.Reprimand.admin+')   
    moder = models.ForeignKey("Moder", null=True, on_delete=models.CASCADE, related_name='modtmrpg.Reprimand.moder+')
    reason = models.TextField('Причина')
    date = models.DateTimeField(auto_now_add=True)
    def getDate(self):
        return self.date.strftime("%d %b %Y")
    def __str__(self):
        return f'[{self.admin.pex.display_name}] {self.admin.nickname} --> [{self.moder.pex.display_name}] {self.moder.nickname}'
    class Meta:
        ordering = ['-date']
        verbose_name = "Выговор"
        verbose_name_plural = "Выговоры"


class Discord(models.Model):
    ds_id = models.IntegerField()
    username = models.CharField(max_length=32)
    avatar = models.TextField('аватарка', blank=True, default='')
    global_name = models.CharField(max_length=32)

    def __str__(self):
        return self.global_name
    
    class Meta:
        verbose_name = "Дискорд"
        verbose_name_plural = "Дискорды"
    

class RegisterFormModel(models.Model):
    secret_code = models.IntegerField()
    password1 = models.CharField('Придумайте пароль',max_length=16)
    password2 = models.CharField('Повторите пароль',max_length=16)

    def __str__(self):
        return self.secret_code
    class Meta:
        verbose_name = "Регистрацционная форма"
        verbose_name_plural = "Регистрационные формы"
    
class Item(models.Model):
    item_name = models.CharField('название',max_length=31)
    description = models.CharField('описание', blank=True, max_length=30)
    note = models.CharField('примечание', blank=True, max_length=35)
    price = models.IntegerField('цена', validators=[MinValueValidator(1)])
    # image = models.CharField(max_length=100)
    image = models.ImageField('картинка',upload_to ='items/', blank=True,  null=True)
    image_url = models.TextField('Путь либо ссылка на картинку (не трогай, если вставил картинкой)',blank=True, null=True)
    type = models.IntegerField('НЕ ТРОГАТЬ(type)', default=0)
    is_auto = models.IntegerField('НЕ ТРОГАТЬ(auto)', default=0)
    # 0 - items
    # 1 - cases
    # 2 - privki
    
    def __str__(self):
        return f'{self.item_name} | цена: {self.price}💵'
    class Meta:
        ordering = ['-type', '-price']
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
    
class MediaCategory(models.Model):
    category_name = models.CharField('название',max_length=12)
    category_folder = models.CharField('путь',max_length=12)
    def __str__(self):
        return f'{self.category_name} | {self.category_folder}'
    class Meta:
        verbose_name = "Категория медиа"
        verbose_name_plural = "Категории медиа"
    
class MediaItem(models.Model):
    media_name = models.CharField('название', max_length=30)
    media_file = models.ImageField(upload_to ='items/')
    category = models.ForeignKey("MediaCategory", on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return f'{self.media_name} | {self.id}'
    class Meta:
        verbose_name = "Предмет медиа"
        verbose_name_plural = "Предметы медиа"

class Config(models.Model):
    config_name = models.CharField('Название',max_length=31)
    config = models.TextField('Конфиг', blank=True)
    description = models.TextField('Заметки/описание', blank=True)
    
    def __str__(self):
        return f'{self.config_name}'
    class Meta:
        verbose_name = "Конфиг"
        verbose_name_plural = "Конфиги"


class EnigmaConfig(models.Model):
    config_name = models.CharField('Название', max_length=31)
    config = models.TextField('Конфиг', blank=True)
    description = models.TextField('Заметки/описание', blank=True)

    def __str__(self):
        return f'{self.config_name}'

    class Meta:
        verbose_name = "Конфиг EnigmaRPG"
        verbose_name_plural = "Конфиги EnigmaRPG"


class BonusRequest(models.Model):
    title = models.CharField("Заголовок", max_length=30)
    moder = models.ForeignKey("Moder", null=True, on_delete=models.CASCADE, related_name='bonus_moder')
    description = models.TextField("Описание")

    request_amount = models.IntegerField(validators=[MinValueValidator(1)])
    final_amount = models.IntegerField(validators=[MinValueValidator(1)], blank=True, null=True)

    who_accepted = models.ForeignKey("Moder", null=True, blank=True, on_delete=models.CASCADE, related_name='bonus_admin')
    is_canceled = models.BooleanField('Отклонен', default=False, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)
    def is_accepted(self):
        return self.who_accepted is not None

    def getDate(self):
        return self.date.strftime("%d %b %Y")\

    def __str__(self):
        return f'id:{self.id} | {self.moder.nickname} | {self.title} | {self.request_amount} | {self.is_accepted()}'

    class Meta:
        ordering = ['date']
        verbose_name = "Запрос на надбавку"
        verbose_name_plural = "Запросы на надбавку"