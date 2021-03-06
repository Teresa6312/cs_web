# Generated by Django 2.0.7 on 2018-09-09 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_collectionpoint_agreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation Date')),
                ('reward_point_used', models.PositiveIntegerField(default=0, verbose_name='Reward Point Used')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Amount')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Coupon', verbose_name='Coupon')),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='service',
            name='deposit_key',
        ),
        migrations.RemoveField(
            model_name='service',
            name='paid_key',
        ),
        migrations.RemoveField(
            model_name='service',
            name='refund_key',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='service',
            name='order_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.OrderSet', verbose_name='Order Set'),
        ),
    ]
