# Generated by Django 3.2.11 on 2022-01-10 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barber_booking', 'func_get_all_accounts_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='barber',
        ),
    ]