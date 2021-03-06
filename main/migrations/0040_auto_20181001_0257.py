# Generated by Django 2.1.1 on 2018-10-01 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20181001_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricerate',
            name='period',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Shipping Period'),
        ),
        migrations.AlterField(
            model_name='pricerate',
            name='package_type',
            field=models.CharField(blank=True, choices=[('F', 'Food/Grocery'), ('R', 'Regular Goods'), ('B', 'Beauty'), ('L', 'Luxury'), ('M', 'Mix')], default='', max_length=16, verbose_name='Package Type'),
        ),
        migrations.AlterField(
            model_name='service',
            name='package_type',
            field=models.CharField(blank=True, choices=[('F', 'Food/Grocery'), ('R', 'Regular Goods'), ('B', 'Beauty'), ('L', 'Luxury'), ('M', 'Mix')], default='', max_length=16, verbose_name='Package Type'),
        ),
    ]
