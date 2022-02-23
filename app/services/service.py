from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from barber_booking.models import Order
from datetime import datetime

def check_active_orders():
    print("Provjera proslih termina...")
    obj = Order.objects.filter(end_datetime__lte=datetime.now(tz=timezone('cet'))).update(status=Order.FINISHED)

def start():

    scheduler = BackgroundScheduler()
    print('Servis je OK')

    scheduler.add_job(check_active_orders, 'interval', seconds=10)

    scheduler.start()