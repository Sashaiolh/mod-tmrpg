# Generated by Django 4.1.3 on 2024-04-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0062_alter_moder_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discord',
            name='global_name',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='discord',
            name='username',
            field=models.CharField(max_length=32),
        ),
    ]
