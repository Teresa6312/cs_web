# Generated by Django 2.0.7 on 2018-09-15 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_service_ship_carrier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritewebsite',
            name='web_type',
            field=models.CharField(blank=True, choices=[('Clothing', 'Clothing'), ('Bag', 'Bag'), ('Jewelry', 'Jewelry'), ('Sport', 'Sport'), ('Beauty', 'Beauty'), ('Baby', 'Baby'), ('Other', 'Other')], default='', max_length=50, verbose_name='Category'),
        ),
    ]
