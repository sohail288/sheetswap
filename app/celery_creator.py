from celery import Celery
from app import create_app

celeryApp = None


def get_or_create_celery(app = create_app()):
    global celeryApp

    if celeryApp is None:
        celery = Celery(app.import_name, include=['util.emailing', 'app.tasks'])
        celery.config_from_object('celeryconfig')
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):

                print("task is ran")
                with app.test_request_context():
                    return super(ContextTask, self).__call__(*args, **kwargs)

        celery.Task = ContextTask
        celeryApp = celery
    return celeryApp

celery = get_or_create_celery()
