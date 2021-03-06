# Generated by Django 2.0.7 on 2018-09-18 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20180917_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderset',
            name='insurance_high',
            field=models.BooleanField(default=False, verbose_name='$10 insurance'),
        ),
        migrations.AddField(
            model_name='orderset',
            name='insurance_low',
            field=models.BooleanField(default=False, verbose_name='$3 insurance'),
        ),
        migrations.AddField(
            model_name='orderset',
            name='insurance_medium',
            field=models.BooleanField(default=False, verbose_name='$5 insurance'),
        ),
    ]
