# myproject/celery.py (myproject는 Django 프로젝트 이름)

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("django_board")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
