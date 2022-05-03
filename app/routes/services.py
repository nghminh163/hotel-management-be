import datetime
from flask import Blueprint, jsonify, request
from app.models.booking import Booking
from app.models.service import Service, ServiceOrders
from app import db

mod = Blueprint('services', __name__, url_prefix='/services')


@mod.route('/', methods=['GET'])
def getAllServices():
    services: list[Service] = Service.query.all()
    return jsonify(list(map(lambda service: service.toJSON(), services)))


@mod.route('/<service_id>', methods=['GET'])
def getServiceById(service_id):
    service: Service = Service.query.get(service_id)
    return jsonify(service.toJSON())


@mod.route('/getByDate', methods=['GET'])
def getServiceOrdersByDate():
    date = request.args.get(
        'date', default=datetime.datetime.now().strftime("%Y-%m-%d"))

    serviceOrders: list[ServiceOrders] = ServiceOrders.query.all()
    results = []
    for order in serviceOrders:
        if date in order.created_at.strftime("%Y-%m-%d"):
            results.append(order)
    return jsonify(list(map(lambda o: o.toJSON(), results)))


@mod.route('/createOrder', methods=['POST'])
def createServiceOrder():
    reqData = request.json
    roomNo = reqData['roomNumber']
    booking:Booking = Booking.query.filter_by(roomNumber=roomNo, status=2).first()
    serviceOrder = ServiceOrders(
        booking_id=booking.id, service_id=reqData['serviceId'], note=reqData['note'], status=1)
    db.session.add_all(serviceOrder)
    db.session.commit()


@mod.route('/finish/<order_id>', methods=['PUT'])
def finishOrderService(order_id):
    try:
        serviceOrder: ServiceOrders = ServiceOrders.query.get(order_id)
        if serviceOrder:
            serviceOrder.status = 2
            db.session.commit()
            return jsonify({"isError": False, "data": serviceOrder.toJSON()})
        return jsonify({"isError": True, "msg": "Booking not found"})
    except:
        return jsonify({"isError": True, "msg": "Something went wrong"})


@mod.route('/booking/<booking_id>', methods=['GET'])
def getServiceOrdersByBookingId(booking_id):
    serviceOrders: list[ServiceOrders] = ServiceOrders.query.filter_by(
        booking_id=booking_id).all()
    return jsonify(list(map(lambda o: o.toJSON(), serviceOrders)))


@mod.route('/getToday', methods=['GET'])
def getTodayOrdersByStatus():
    status = request.args.get(
        'status', type=int, default=1)
    serviceOrders: list[ServiceOrders] = ServiceOrders.query.filter_by(
        status=status).all()
    return jsonify(list(map(lambda o: o.toJSON(), serviceOrders)))
# ,
