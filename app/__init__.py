from flask import Flask

from flask import (
    render_template,
    request,
    g,
    session,
    jsonify,
    Response
)

from flask.ext.bootstrap import Bootstrap

import os


BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR   = os.path.join(BASE_DIR, 'static')


bootstrap = Bootstrap()

def create_app():
    # import blueprints and register them
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    from .controllers.site import main_routes
    app.register_blueprint(main_routes)

    from .controllers.sheets import sheets_routes
    app.register_blueprint(sheets_routes)

    from .controllers.auth import auth_routes
    app.register_blueprint(auth_routes)

    bootstrap.init_app(app)

    app.secret_key = 'bananas'
    return app

