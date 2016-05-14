import os

from celery import Celery
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail

from config import get_env_config


bootstrap = Bootstrap()
mail = Mail()
app = None
celeryApp = None


def create_app(app_settings=None):
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
    mail.init_app(app)

    return app

def get_or_create_app():
    global app
    if not app:
        app = create_app()
    return app

def get_or_create_celery():
    global celeryApp
    app = get_or_create_app()

    if celeryApp is None:
        celery = Celery(app.import_name, include = ['util.emailing', 'app.controllers.items.tasks'])
        celery.config_from_object('celeryconfig')
        TaskBase = celery.Task
        class ContextTask(TaskBase):
            abstract = True
            def __call__(self, *args, **kwargs):
                with app.test_request_context():
                    return super(ContextTask,self).__call__(*args, **kwargs)

        celery.Task = ContextTask
        celeryApp = celery
    return celeryApp


