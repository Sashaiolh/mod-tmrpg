# Generated by Django 5.0.2 on 2024-03-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0007_alter_moder_discord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discord',
            name='avatar',
            field=models.TextField(blank=True, default='', verbose_name='аватарка'),
        ),
    ]
