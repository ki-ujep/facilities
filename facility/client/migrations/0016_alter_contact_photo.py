# Generated by Django 4.2 on 2023-04-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_alter_contact_photo_alter_device_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='photo',
            field=models.ImageField(blank=True, default='managers/male.png', upload_to='managers/'),
        ),
    ]
