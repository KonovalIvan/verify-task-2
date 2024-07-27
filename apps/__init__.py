import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security

from apps.auth.models import Role, User
from apps.database import db

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
mail = Mail()
security = Security()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
login_manager = LoginManager()


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

    # login manager
    login_manager.init_app(app)

    # register routes
    import apps.routes as home
    import apps.auth.routes as auth
    import apps.admin_panel.routes as admin_panel
    import apps.user_panel.routes as user_panel
    import apps.email.routes as email

    app.register_blueprint(home.module)
    app.register_blueprint(auth.module, url_prefix='/auth')
    app.register_blueprint(admin_panel.module, url_prefix='/admin_panel')
    app.register_blueprint(user_panel.module, url_prefix='/user_panel')
    app.register_blueprint(email.module, url_prefix='/email')

    return app
