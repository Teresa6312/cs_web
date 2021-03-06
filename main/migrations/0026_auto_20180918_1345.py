# Generated by Django 2.0.7 on 2018-09-18 13:45

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20180918_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionpoint',
            name='collector_icon',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='collector_icon'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='id_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='collector_id'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='license_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='collector_license'),
        ),
        migrations.AlterField(
            model_name='packagesnapshot',
            name='snapshot',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='package_snapshot'),
        ),
    ]
