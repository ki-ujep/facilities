# Generated by Django 4.2 on 2023-04-27 12:28

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0019_category_parent"),
    ]

    operations = [
        TrigramExtension(),
    ]