from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import (
    Group,
)

class Command(BaseCommand):
    help = 'Create Main Roles'

    def handle(self, *args, **options):
        print("Adding roles...")
        roles = [
            'Admin',
            'Frizer',
            'Klijent'
        ]
        for role in roles:
            Group.objects.get_or_create(name=role)

        print("Roles Added.")