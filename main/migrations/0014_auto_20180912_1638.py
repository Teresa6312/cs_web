# Generated by Django 2.0.7 on 2018-09-12 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20180912_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Preferred Language'),
        ),
    ]
