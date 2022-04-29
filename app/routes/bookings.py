import datetime
from flask import Blueprint, jsonify, request
from app.models.booking import Booking
from app import db
from app.models.room import Room
mod = Blueprint('bookings', __name__, url_prefix='/bookings')


def validatorCreate(data):
    if 'clientName' not in data:
        return "Missing name's client"
    if 'clientNumber' not in data:
        return "Missing number's client"
    if 'checkInDate' not in data:
        return "Missing check in date"
    if 'checkOutDate' not in data:
        return "Missing check out date"
    if 'roomNumber' not in data:
        return "Missing room number"
    if Room.query.get(data['roomNumber']) is None:
        return 'Invalid room'
    # Handle case number phone + checkin date >= today, check out date > checkin date
    return True


def strToTime(strDate, strTime=""):
    splitStr = list(map(int, strDate.split('-')))
    return datetime.datetime(splitStr[0], splitStr[1], splitStr[2], 12, 0, 0)


@mod.route('/create', methods=["POST"])
def createBooking():
    reqData = request.json
    msg = validatorCreate(reqData)
    if msg is True:
        checkInTime = strToTime(reqData['checkInDate'])
        checkOutTime = strToTime(reqData['checkOutDate'])
        booking = Booking(clientName=reqData['clientName'], clientNumber=reqData['clientNumber'],
                          checkinDate=checkInTime, checkoutDate=checkOutTime, roomNumber=reqData['roomNumber'])
        db.session.add(booking)
        db.session.commit()
        return jsonify({"isError": False, "data": booking.toJSON()})
    return jsonify({"isError": True, "msg": msg})


@mod.route('/<booking_id>', methods=["GET"])
def getBookingById(booking_id):
    try:
        booking: Booking = Booking.query.get(booking_id)
        if booking:
            return jsonify({"isError": False, "data": booking.toJSON()})
        return jsonify({"isError": True, "msg": "Booking not found"})
    except:
        return jsonify({"isError": True, "msg": "Something went wrong"})


@mod.route('/<booking_id>/checkin', methods=["PUT"])
def checkInById(booking_id):
    try:
        booking: Booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 2
            booking.checkinDate = datetime.datetime.now()
            db.session.commit()
            return jsonify({"isError": False, "data": booking.toJSON()})
        return jsonify({"isError": True, "msg": "Booking not found"})
    except:
        return jsonify({"isError": True, "msg": "Something went wrong"})

@mod.route('/<booking_id>/checkout', methods=["PUT"])
def checkOutById(booking_id):
    try:
        booking: Booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 3
            booking.checkoutDate = datetime.datetime.now()
            db.session.commit()
            return jsonify({"isError": False, "data": booking.toJSON()})
        return jsonify({"isError": True, "msg": "Booking not found"})
    except:
        return jsonify({"isError": True, "msg": "Something went wrong"})
