# Generated by Django 4.2.7 on 2023-12-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_client_temp_pharmacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='best_distance',
            field=models.FloatField(default=0),
        ),
    ]