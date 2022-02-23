from django.db import models
from accounts.models import Account

# Create your models here.

class HairStyle(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True, default=None)
    avatar = models.FileField(blank=True, null=True, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True, default=None)
    time_needed = models.IntegerField(blank=True, null=True, default=None) # Minute
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):

    CANCELED = 'canceled'
    ACTIVE = 'active'
    FINISHED = 'finished'

    STATUS_CHOICES = [
        (ACTIVE, 'Aktivna narudzba'),
        (CANCELED, 'Otkazana narudzba'),
        (FINISHED, 'Završena narudzba'),
    ]

    start_datetime = models.DateTimeField(blank=True, null=True, default=None)
    end_datetime = models.DateTimeField(blank=True, null=True, default=None)
    client = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='client')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, blank=True, null=True, default=ACTIVE)
    duration = models.IntegerField(blank=True, null=True, default=None)
    total_price = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True, default=None)

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='order_items')
    hair_style = models.ForeignKey(HairStyle, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    barber = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True, default=None)