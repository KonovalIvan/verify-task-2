import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security

from apps.auth.models import Role, User
from apps.database import db

load_dotenv()


def create_app():
    app = Flask(__name__)
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
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    # register routes
    import apps.routes as home
    import apps.auth.routes as auth
    app.register_blueprint(home.module)
    app.register_blueprint(auth.module)

    # Migrations
    app.migrate = Migrate(app, db)

    return app
