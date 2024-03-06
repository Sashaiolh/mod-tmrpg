# Generated by Django 5.0.2 on 2024-03-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0030_alter_item_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_url',
            field=models.TextField(blank=True, null=True, verbose_name='либо ссылка на картинку'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/', verbose_name='картинка'),
        ),
    ]
