from flask import Flask


def create_app() -> Flask:
    application_flask = Flask(__name__)

    from triangulator.routes.pointset_routes import pointset_routes
    application_flask.register_blueprint(pointset_routes)

    from triangulator.routes.triangulation_routes import triangulation_routes
    application_flask.register_blueprint(triangulation_routes)

    return application_flask
