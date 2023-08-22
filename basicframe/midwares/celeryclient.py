from celery import Celery

from basicframe.midwares import celeryconfig

app = Celery('app')

app.config_from_object(celeryconfig)
print(app)