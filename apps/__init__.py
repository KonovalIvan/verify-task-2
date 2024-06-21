from flask import Flask


def create_app():
    app = Flask(__name__)

    # register routes
    import apps.routes as home
    app.register_blueprint(home.module)

    return app
