# Generated by Django 5.0.2 on 2024-03-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0014_registerformmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='moder',
            name='is_registered',
            field=models.BooleanField(default=False, verbose_name='Зарегистрирован'),
        ),
    ]