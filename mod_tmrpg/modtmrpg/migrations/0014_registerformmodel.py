# Generated by Django 5.0.2 on 2024-03-02 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0013_alter_moder_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_code', models.IntegerField()),
                ('password1', models.CharField(max_length=16)),
                ('password2', models.CharField(max_length=16)),
            ],
        ),
    ]