# Generated by Django 2.0.7 on 2018-09-12 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20180912_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Available'),
        ),
    ]
