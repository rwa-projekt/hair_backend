from django.core.management.base import BaseCommand
from django.utils import timezone
from barber_booking.models import HairStyle

class Command(BaseCommand):
    help = 'Create Services'

    def handle(self, *args, **options):
        print("Adding services...")
        services = [
            {
                "name": "Brijanje",
                "avatar": 'uredivanje_brade_1.jpeg',
                "time_needed": 30,
                "price": 8
            },
            {
                "name": "Fade Šišanje",
                "avatar": 'fade_1.jpg',
                "time_needed": 30,
                "price": 15
            },
        ]
        for service in services:
            obj, created = HairStyle.objects.get_or_create(**service)

        print("Services Added.")