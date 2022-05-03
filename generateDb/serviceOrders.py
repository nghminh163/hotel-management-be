import datetime
import json
from random import randint
from app import db
from app.models.service import ServiceOrders


def generate():
    serviceOrdersData = json.load(
        open('generateDb/data/serviceOrders.json'))
    

    serviceOrders = map(lambda serviceOrder: ServiceOrders(
        booking_id=serviceOrder['bookingId'],
        # note=serviceOrder['note'],
        note="",
        service_id=serviceOrder['serviceId'],
        created_at=datetime.datetime.strptime(serviceOrder['createdAt'], "%Y-%m-%dT%H:%M:%S%z"),
        # status=serviceOrder['status'],
        status=randint(1, 2)
    ), serviceOrdersData)
    db.session.add_all(serviceOrders)
    db.session.commit()
