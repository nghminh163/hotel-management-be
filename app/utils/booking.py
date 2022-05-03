import datetime
from app.models.booking import Booking
def getBookingByDate(date:str,status = 1) -> dict:
    bookings: list[Booking] = Booking.query.filter_by(status=status).all()
    results = []
    for booking in bookings:
        if date in booking.created_at.strftime("%Y-%m-%d"):
            results.append(booking)
    return results

def getCheckinByDate(date:str,status = 1) -> dict:
    bookings: list[Booking] = Booking.query.filter_by(status=status).all()
    results = []
    for booking in bookings:
        if date in booking.checkinDate:
            results.append(booking)
    return results

def getCheckoutByDate(date:str,status = 1) -> dict:
    bookings: list[Booking] = Booking.query.filter_by(status=status).all()
    results = []
    for booking in bookings:
        if date in booking.checkoutDate:
            results.append(booking)
    return results

def getUpcomingArrivals() -> dict:
    bookings: list[Booking] = Booking.query.filter_by(status=1).all()
    results = []
    for booking in bookings:
        if datetime.datetime.now().strftime("%Y-%m-%d") in booking.checkinDate:
            results.append(booking)
    return results

def getUpcomingDeparture() -> dict:
    bookings: list[Booking] = Booking.query.filter_by(status=2).all()
    results = []
    for booking in bookings:
        if datetime.datetime.now().strftime("%Y-%m-%d") in booking.checkoutDate:
            results.append(booking)
    return results
