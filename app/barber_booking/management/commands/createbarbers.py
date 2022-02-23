from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import Account

class Command(BaseCommand):
    help = 'Create Barbers'

    def handle(self, *args, **options):
        print("Adding barbers...")
        barbers = [
            {
                "name": "Alen Duranović",
                "email": "alen.duranovic@email.com",
                "phone_number": "063101202",
                "role_id": 2
            },
            {
                "name": "Nikola Čerkez",
                "email": "nikola.cerkez@email.com",
                "phone_number": "063451201",
                "role_id": 2
            }
        ]
        for barber in barbers:
            obj, created = Account.objects.get_or_create(**barber)
            if created:
                obj.set_password('barbertest123')
                obj.save()

        print("Barbers Added.")