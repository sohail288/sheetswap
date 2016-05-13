import os
from celery import Celery

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from config import get_env_config


celery = Celery(__name__, include = ['util.emailing'])
celery.config_from_object('celeryconfig')
bootstrap = Bootstrap()

def create_app(app_settings = None):
    config_obj = get_env_config(app_settings)
    app = Flask(__name__,
                template_folder=config_obj.TEMPLATE_DIR,
                static_folder=config_obj.STATIC_DIR)
    app.config.from_object(config_obj)

    # import blueprints and register them
    from .controllers.site import main_routes
    app.register_blueprint(main_routes)

    from .controllers.sheets import sheets_routes
    app.register_blueprint(sheets_routes)

    from .controllers.auth import auth_routes
    app.register_blueprint(auth_routes)

    from .controllers.items import items_routes
    app.register_blueprint(items_routes)

    from .controllers.trades import trade_routes
    app.register_blueprint(trade_routes)

    if hasattr(config_obj, 'TESTING'):
        from .controllers.testing import tests
        app.register_blueprint(tests)

    bootstrap.init_app(app)

    return app

