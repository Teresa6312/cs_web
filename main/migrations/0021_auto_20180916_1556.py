# Generated by Django 2.0.7 on 2018-09-16 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20180915_2329'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parentpackage',
            options={'ordering': ['-created_date'], 'verbose_name_plural': 'Parent Package'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-created_date'], 'verbose_name_plural': 'Package/Order'},
        ),
        migrations.AddField(
            model_name='user',
            name='memo',
            field=models.TextField(blank=True, default='', verbose_name='Memo'),
        ),
    ]
