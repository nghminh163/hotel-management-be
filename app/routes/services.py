from flask import Blueprint, jsonify
from app.models.service import Service

mod = Blueprint('services', __name__, url_prefix='/services')


@mod.route('/', methods=['GET'])
def getAllServices():
    services: list[Service] = Service.query.all()
    return jsonify(list(map(lambda service: service.toJSON(), services)))


@mod.route('/<service_id>', methods=['GET'])
def getServiceById(service_id):
    service: Service = Service.query.get(service_id)
    return jsonify(service.toJSON())
