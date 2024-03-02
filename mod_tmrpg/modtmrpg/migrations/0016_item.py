# Generated by Django 5.0.2 on 2024-03-02 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0015_moder_is_registered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=16, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('price', models.IntegerField(verbose_name='цена')),
                ('image', models.ImageField(upload_to='items/')),
            ],
        ),
    ]
