# Generated by Django 3.2.10 on 2021-12-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barber_booking', 'sql'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hairstyle',
            name='is_active',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]