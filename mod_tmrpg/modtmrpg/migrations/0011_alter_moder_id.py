# Generated by Django 5.0.2 on 2024-03-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0010_alter_moder_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moder',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
