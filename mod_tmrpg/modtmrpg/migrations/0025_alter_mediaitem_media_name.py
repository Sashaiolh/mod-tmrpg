# Generated by Django 5.0.2 on 2024-03-03 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0024_mediacategory_category_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='media_name',
            field=models.CharField(max_length=16, verbose_name='название'),
        ),
    ]
