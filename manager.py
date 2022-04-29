from app import create_app, db
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import sys

sys.dont_write_bytecode = True


if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app('development')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed():
    from generateDb import services, roomTypes,rooms
    services.generate()
    roomTypes.generate()
    rooms.generate()


@manager.command
def dev():
    run_simple('0.0.0.0', 3000, app,
               use_reloader=True, use_debugger=True,
               )


if __name__ == '__main__':
    manager.run()
