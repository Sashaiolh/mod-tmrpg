# Generated by Django 5.0.2 on 2024-03-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0038_ecolog_moder_alter_ecolog_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecolog',
            name='amount',
            field=models.IntegerField(verbose_name='Количество'),
        ),
    ]