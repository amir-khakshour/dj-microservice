import os
import sys
from celery import Celery
from kombu.common import Broadcast

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(2, APPS_DIR)

# @todo add expire time to messages
app = Celery('GridScaleWorker')
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_queues = (Broadcast('broadcast_tasks'),)
app.conf.task_routes = {
    'tasks.reload_foreign_key': {
        'queue': 'broadcast_tasks',
        'exchange': 'broadcast_tasks'
    }
}


@app.task(bind=True)
def debug_task(self):
    print(('Request: {0!r}'.format(self.request)))
