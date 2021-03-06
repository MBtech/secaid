import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import create_app, db
from app import blueprint

# Import models
# from app.main.model import user
# from app.main.model import blacklist

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
# app.config.from_object('app.util.keycloak_settings')
app.config.from_envvar('SETTINGS')

app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()