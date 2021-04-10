from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail
from flask_login import LoginManager
from config import Configuration



db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
manager = Manager()
manager.add_command('db', MigrateCommand)
login = LoginManager()
login.login_view = 'users.login'
mail = Mail()


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from todolist.users.views import users
    from todolist.main.views import main
    from todolist.todos.views import todos
    from todolist.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(todos)
    app.register_blueprint(errors)

    return app