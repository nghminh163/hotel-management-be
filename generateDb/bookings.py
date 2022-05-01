from app.models.booking import Booking
import json
from app import db


def generate():
    bookingsData = json.load(
        open('generateDb/data/bookings.json'))
    bookings = map(lambda booking: Booking(
        clientName=booking['clientName'],
        roomNumber=booking['roomNumber'],
        clientNumber=booking['clientNumber'],
        checkinDate=booking['checkinDate'],
        checkoutDate=booking['checkoutDate'],
        checkinTime=booking['checkinTime'],
        checkoutTime=booking['checkoutTime'], status=booking['status']), bookingsData)
    db.session.add_all(bookings)
    db.session.commit()
