# Generated by Django 5.0.2 on 2024-03-03 01:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0019_alter_moder_discord_alter_moder_pex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='discord',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='modtmrpg.discord'),
        ),
        migrations.AlterField(
            model_name='moder',
            name='pex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modtmrpg.pex'),
        ),
    ]