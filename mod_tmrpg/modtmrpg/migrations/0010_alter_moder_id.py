# Generated by Django 5.0.2 on 2024-03-02 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0009_alter_moder_discord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False),
        ),
    ]
