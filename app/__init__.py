from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    from app.routes.services import mod as services_mod
    from app.routes.roomTypes import mod as roomType_mod
    from app.routes.rooms import mod as rooms_mod
    from app.routes.bookings import mod as bookings_mod
    from app.routes.revenue import mod as revenue_mod
    from app.routes.auth import mod as auth_mod

    app.register_blueprint(roomType_mod)
    app.register_blueprint(services_mod)
    app.register_blueprint(rooms_mod)
    app.register_blueprint(bookings_mod)
    app.register_blueprint(revenue_mod)
    app.register_blueprint(auth_mod)



    #  # HTTP error handling
    #  @app.errorhandler(404)
    #  def not_found(error):
    #      return render_template('error/404.html'), 404

    #  @app.errorhandler(500)
    #  def internal_server_error(error):
    #      return render_template('error/500.html'), 500

    return app
