# Generated by Django 5.0.2 on 2024-03-06 19:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0041_ecolog_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecolog',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
