# ai_post/apps.py

from django.apps import AppConfig
import threading

class AiPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_post'

    # 클래스 변수로 플래그 설정
    scheduler_started = False

    def ready(self):
        if not self.scheduler_started:
            from . import scheduler  # myapp/scheduler.py
            scheduler.start()
            AiPostConfig.scheduler_started = True
            print("[스케줄러] 스케줄러 시작 완료")
