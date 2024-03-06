# Generated by Django 5.0.2 on 2024-03-05 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0032_alter_item_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='pex',
            field=models.ForeignKey(default='helper1', on_delete=django.db.models.deletion.CASCADE, to='modtmrpg.pex', to_field='pex_name'),
        ),
        migrations.AlterField(
            model_name='pex',
            name='pex_name',
            field=models.CharField(max_length=12, unique=True, verbose_name='pex'),
        ),
        migrations.AlterField(
            model_name='registerformmodel',
            name='password1',
            field=models.CharField(max_length=16, verbose_name='Придумайте пароль'),
        ),
        migrations.AlterField(
            model_name='registerformmodel',
            name='password2',
            field=models.CharField(max_length=16, verbose_name='Повторите пароль'),
        ),
    ]