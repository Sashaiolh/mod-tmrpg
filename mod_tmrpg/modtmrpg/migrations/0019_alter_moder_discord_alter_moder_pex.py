# Generated by Django 5.0.2 on 2024-03-03 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0018_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='discord',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='moder',
            name='pex',
            field=models.CharField(max_length=12, verbose_name='pex'),
        ),
    ]
