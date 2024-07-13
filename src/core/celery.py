import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.enable_utc = False
app.conf.update(
    timezone="Asia/Kathmandu",
    broker_connection_retry_on_startup=True,
)
app.conf.beat_scheduler = {
    "every-10-seconds": {
        "task": "m",
    },
}
