from datetime import datetime
from common.constants import ACTIVE
from .models import *
from .serializers import *

def get_busy_list_orders(barber: int, _dt: datetime):
    print(barber)
    print(_dt)

    objs = Order.objects.filter(start_datetime__contains=_dt, order_items__barber_id=barber, status=Order.ACTIVE).distinct()

    print(objs)

    ser = BusyListOrderSerializer(objs, many=True)
    print(ser.data)

    return ser.data