import hashlib
from flask import Blueprint, jsonify, request
from app.models.user import User
mod = Blueprint('auth', __name__, url_prefix='/auth')


@mod.route('/login', methods=["POST"])
def login():
    reqData = request.json
    username = reqData['username']
    password = reqData['password']
    if username is not None and password is not None:
        user = User.query.filter_by(username=username).first()
        if user is not None and user.password == hashlib.md5(password.encode()).hexdigest():
            return jsonify(user.toJSON())
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    else:
        return jsonify({"isError": True})
