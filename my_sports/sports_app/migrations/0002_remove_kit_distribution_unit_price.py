# Generated by Django 4.2.14 on 2024-08-05 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sports_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit_distribution',
            name='unit_price',
        ),
    ]