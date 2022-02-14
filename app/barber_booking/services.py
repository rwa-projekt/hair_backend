from datetime import time, timedelta, datetime
import json
from django.db import transaction

from common.services import DataAbstract
from .models import *
from django.shortcuts import get_object_or_404
from .serializers import *


def get_json_data_from_formdata(formdata):
    data = json.loads(formdata['data'])
    return data


def add_hair_style(formdata, files=None):
    data = get_json_data_from_formdata(formdata)
    print(data)

    file = files[0] if files else None

    hair_style = HairStyle.objects.create(
        avatar = file,
        **data
    )

    return hair_style

class HairStyleService:
    def __init__():
        pass

    @classmethod
    def set_avatar(self, pk, files):
        print("Postavljanje avatara")
        file = files[0] if files else None

        obj = get_object_or_404(HairStyle, id=pk)
        obj.avatar = file
        obj.save()
        return obj


class OrderService:
    def __init__(self):
        pass

    @classmethod
    @transaction.atomic
    def add_order(self, data):
        obj = Order.objects.create(
            start_datetime=data['start_datetime'],
            client_id=data['client']
        )
        obj.duration = 0
        obj.total_price = 0
        oi_arr = []
        for oi in data['order_items']:
            oi_arr.append(
                OrderItems(
                    order=obj,
                    hair_style_id=oi['hair_style'],
                    barber_id=oi['barber']
                )
            )
            try:
                hs_obj = HairStyle.objects.get(id=oi['hair_style'])
                obj.duration += hs_obj.time_needed 
                obj.total_price += hs_obj.price
            except:
                pass
        obj.save()
        obj = Order.objects.get(id=obj.id)
        obj.end_datetime = obj.start_datetime + timedelta(minutes=obj.duration)
        obj.save()
        OrderItems.objects.bulk_create(oi_arr)
        return obj
