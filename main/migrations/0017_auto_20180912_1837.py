# Generated by Django 2.0.7 on 2018-09-12 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20180912_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritewebsite',
            name='rate',
            field=models.PositiveIntegerField(default=1, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='favoritewebsite',
            name='web_name',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Website Name'),
        ),
        migrations.AlterField(
            model_name='favoritewebsite',
            name='web_type',
            field=models.CharField(blank=True, choices=[('Clothing', 'Clothing'), ('Bag', 'Bag'), ('Jewelry', 'Jewelry'), ('Sport', 'Sport'), ('Beauty', 'Beauty'), ('Baby', 'Baby'), ('Other', 'Other')], default='', max_length=50, verbose_name='Website Category'),
        ),
        migrations.AlterField(
            model_name='favoritewebsite',
            name='web_url',
            field=models.URLField(blank=True, default='', max_length=1000, verbose_name='Website url'),
        ),
        migrations.AlterField(
            model_name='location',
            name='country_sortname',
            field=models.CharField(default='', max_length=100, verbose_name='Country Shortname'),
        ),
    ]
