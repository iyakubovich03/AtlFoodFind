# Generated by Django 5.1.1 on 2024-09-27 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AtlantaFoodFinder', '0004_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
