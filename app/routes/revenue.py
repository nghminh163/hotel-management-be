import datetime
from flask import Blueprint, jsonify, request
from app import db
from app.models.booking import Booking
from app.models.room import Room, RoomType
from app.models.service import ServiceOrders
mod = Blueprint('revenue', __name__, url_prefix='/revenue')


def getRevenueByBooking(booking_id):
    try:
        booking: Booking = Booking.query.get(booking_id)
        if booking is None:
            return None
        room: Room = booking.room
        roomType: RoomType = room.roomType
        serviceOrders: ServiceOrders = ServiceOrders.query.filter_by(
            booking_id=booking_id).all()
        chargeServices: list[ServiceOrders] = []
        for sOrder in serviceOrders:
            if sOrder.service_id in list(map(lambda x: x.id, roomType.promo)):
                pass
            else:
                chargeServices.append(sOrder)
        checkInDateSpl = list(map(int, booking.checkinDate.split('-')))
        checkOutDateSpl = list(map(int, booking.checkoutDate.split('-')))

        d0 = datetime.date(checkInDateSpl[0],
                           checkInDateSpl[1], checkInDateSpl[2])
        d1 = datetime.date(
            checkOutDateSpl[0], checkOutDateSpl[1], checkOutDateSpl[2])
        delta = d1 - d0

        revenue = {
            "bookingId": booking.id,
            "clientName": booking.clientName,
            "roomNumber": booking.roomNumber,
            "roomFee": roomType.price * delta.days,
            "serviceFee": sum(list(map(lambda x: x.service.price, chargeServices))),
        }
        revenue["totalBill"] = revenue["roomFee"] + revenue["serviceFee"]
        return revenue
    except Exception as e:
        print(e)
        return None


@ mod.route('/booking/<booking_id>', methods=["GET"])
def getRevenueByBID(booking_id):
    rBid = getRevenueByBooking(booking_id)
    if rBid is None:
        return "0"
    return str(rBid['totalBill'])


@ mod.route('/booking', methods=["GET"])
def getRevenueByDate():
    date = request.args.get(
        'date', default=datetime.datetime.now().strftime("%Y-%m-%d"))
    bookings: list[Booking] = Booking.query.filter_by(status=3).all()
    checkoutBook: Booking = []
    for booking in bookings:
        if date in booking.checkoutDate:
            checkoutBook.append(booking)
    revenuesDay = list(map(lambda x: getRevenueByBooking(x.id), checkoutBook))
    return jsonify(revenuesDay)


@ mod.route('/booking/total', methods=["GET"])
def getTotalRevenueByDate():
    date = request.args.get(
        'date', default=datetime.datetime.now().strftime("%Y-%m-%d"))
    bookings: list[Booking] = Booking.query.filter_by(status=3).all()
    checkoutBook: Booking = []
    for booking in bookings:
        if date in booking.checkoutDate:
            checkoutBook.append(booking)
    revenuesDay = list(map(lambda x: getRevenueByBooking(x.id)[
        'totalBill'], checkoutBook))
    return jsonify(sum(revenuesDay))
