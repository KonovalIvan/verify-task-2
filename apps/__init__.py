import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security

from apps.auth.models import Role, User
from apps.database import db

load_dotenv()

app = Flask(__name__, template_folder='apps/templates', static_folder='apps/static')
mail = Mail()
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
    app.config.from_object(os.environ['APP_SETTINGS'])

    # Database
    db.init_app(app)

    with app.test_request_context():
        db.create_all()

        # Create default roles, theoretically server start once in long time, so we can afford one for loop
        for role in ['user', 'admin', 'moderator']:
            if not Role.query.filter_by(name=role).first():
                new_role = Role(name=role)
                db.session.add(new_role)
        db.session.commit()

    # Flask-Security
    security.init_app(app, user_datastore)

    # Migrations
    app.migrate = Migrate(app, db)

    # Email
    app.debug = 0
    mail.init_app(app)

    # register routes
    import apps.routes as home
    import apps.auth.routes as auth
    app.register_blueprint(home.module)
    app.register_blueprint(auth.module, url_prefix='/auth')

    return app
