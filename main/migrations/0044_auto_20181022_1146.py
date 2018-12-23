# Generated by Django 2.1.1 on 2018-10-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_auto_20181003_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricerate',
            name='package_type',
            field=models.CharField(blank=True, choices=[('B-F', 'Food/Grocery'), ('A-R', 'Regular Goods'), ('C-B', 'Beauty'), ('D-L', 'Luxury'), ('E-M', 'Mix')], default='', max_length=16, verbose_name='Package Type'),
        ),
        migrations.AlterField(
            model_name='service',
            name='package_type',
            field=models.CharField(blank=True, choices=[('B-F', 'Food/Grocery'), ('A-R', 'Regular Goods'), ('C-B', 'Beauty'), ('D-L', 'Luxury'), ('E-M', 'Mix')], default='', max_length=16, verbose_name='Package Type'),
        ),
        migrations.AlterField(
            model_name='service',
            name='ship_carrier',
            field=models.CharField(blank=True, choices=[('DHL', 'DHL - Regular items'), ('EMS', 'EMS - All kind of items'), ('SF EXPRESS', 'SF EXPRESS - Regular items'), ('Cheapest', 'The cheapest one'), ('Fastest', 'The fastest one')], default='', max_length=100, verbose_name='Select a Carrier'),
        ),
    ]
