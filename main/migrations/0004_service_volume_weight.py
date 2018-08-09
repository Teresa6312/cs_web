# Generated by Django 2.0.7 on 2018-08-05 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180802_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='volume_weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Volume Weight(kg)'),
        ),
    ]