# Generated by Django 4.1.3 on 2024-04-02 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0061_config_pex_oc_nickname_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='nickname',
            field=models.CharField(max_length=32, unique=True, verbose_name='никнейм'),
        ),
    ]
