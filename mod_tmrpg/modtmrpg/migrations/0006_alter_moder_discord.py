# Generated by Django 5.0.2 on 2024-03-02 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0005_alter_moder_discord_alter_moder_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='discord',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='modtmrpg.discord'),
        ),
    ]
