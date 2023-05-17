from celery import Celery
from flask import current_app as app

celery = Celery('application jobs')

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)