# Generated by Django 3.2.11 on 2022-01-10 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_booking', '0002_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='duration',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
