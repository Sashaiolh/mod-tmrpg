# Generated by Django 4.1.3 on 2024-03-31 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('modtmrpg', '0059_alter_ecolog_admin_alter_ecolog_moder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecolog',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='modtmrpg.moder'),
        ),
        migrations.AlterField(
            model_name='ecolog',
            name='moder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moder', to='modtmrpg.moder'),
        ),
    ]